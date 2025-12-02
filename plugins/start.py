import os
import asyncio
import sys
import time
import base64
from collections import defaultdict
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatMemberStatus, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, User
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant, ChatIdInvalid

from datetime import datetime, timedelta
from config import ADMINS, OWNER_ID
from helper_func import encode, decode
from database.database import save_encoded_link, get_channel_by_encoded_link, save_encoded_link2, get_channel_by_encoded_link2
from database.database import add_user, del_user, full_userbase, present_user, is_admin, get_channel_photo_link, is_user_banned, get_channel_title, save_global_shared_link, save_global_shared_request_link, get_global_shared_link, get_global_shared_request_link

#=====================================================================================##

def _escape_md_v2(text: str) -> str:
    # Escape all MDV2 special chars
    if not text:
        return text
    specials = r"_*[]()~`>#+-=|{}.!\\"
    escaped = ""
    for ch in text:
        if ch in specials:
            escaped += f"\\{ch}"
        else:
            escaped += ch
    return escaped

def _escape_md_v2_url(url: str) -> str:
    if not url:
        return url
    # In MarkdownV2 link target, escape backslashes and parentheses only
    return url.replace("\\", "\\\\").replace("(", "\$$").replace(")", "\$$")

async def refresh_global_links_periodically(client: Client):
    """Refresh global shared links at 9-minute intervals."""
    await asyncio.sleep(5)  # Wait for client to initialize
    while True:
        try:
            await asyncio.sleep(540)  # 9 minutes
            channels = await get_channels()
            for channel_id in channels:
                try:
                    expire_at = datetime.now() + timedelta(minutes=10)
                    
                    # Refresh normal link
                    invite = await client.create_chat_invite_link(
                        chat_id=channel_id,
                        expire_date=expire_at,
                        creates_join_request=False
                    )
                    await save_global_shared_link(channel_id, invite.invite_link, expire_at.isoformat())
                    
                    # Refresh request link
                    request_invite = await client.create_chat_invite_link(
                        chat_id=channel_id,
                        expire_date=expire_at,
                        creates_join_request=True
                    )
                    await save_global_shared_request_link(channel_id, request_invite.invite_link, expire_at.isoformat())
                    
                    print(f"[Refresh] Global links renewed for channel {channel_id}")
                except Exception as e:
                    print(f"[Refresh] Error renewing links for {channel_id}: {e}")
        except Exception as e:
            print(f"[Refresh] Global link refresh error: {e}")

async def _get_or_create_link(client: Client, channel_id: int, is_request: bool = False) -> str:
    """Get existing valid link or create new one if expired/missing."""
    if is_request:
        existing = await get_global_shared_request_link(channel_id)
    else:
        existing = await get_global_shared_link(channel_id)
    
    if existing:
        return existing  # Return existing valid link
    
    # Link expired or doesn't exist - create new one
    try:
        expire_at = datetime.now() + timedelta(minutes=10)
        invite = await client.create_chat_invite_link(
            chat_id=channel_id,
            expire_date=expire_at,
            creates_join_request=is_request
        )
        expiry_str = expire_at.isoformat()
        
        if is_request:
            await save_global_shared_request_link(channel_id, invite.invite_link, expiry_str)
        else:
            await save_global_shared_link(channel_id, invite.invite_link, expiry_str)
        
        return invite.invite_link
    except Exception as e:
        print(f"[Link] Error creating link for {channel_id}: {e}")
        return None

@Client.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is banned
    if await is_user_banned(user_id):
        return  # Silently ignore banned users, no response

    # Proceed with the original functionality if the user is not banned
    text = message.text
    await add_user(user_id)  # Add user to DB
    
    placeholder = None
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    except Exception:
        pass

    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1].strip()
            is_request = base64_string.startswith("req_")
            
            if is_request:
                base64_string = base64_string[4:]
                channel_id = await get_channel_by_encoded_link2(base64_string)
            else:
                channel_id = await get_channel_by_encoded_link(base64_string)
            
            if not channel_id:
                if placeholder:
                    try: await placeholder.delete()
                    except Exception: pass
                return await message.reply_text("⚠️ Invalid or expired invite link.")

            invite_link = await _get_or_create_link(client, channel_id, is_request)
            if not invite_link:
                return await message.reply_text("⚠️ Unable to generate link. Try again later.")

            button_text = "🛎️ Request to Join" if is_request else "🔗 Join Channel"
            button = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, url=invite_link)]])

            # If a photo_link is available, send a photo with a MarkdownV2 caption; else fallback to text
            photo_link = await get_channel_photo_link(channel_id)
            if photo_link:
                # Fetch channel name or custom title
                custom_title = await get_channel_title(channel_id)
                chat = await client.get_chat(channel_id)
                display_title = custom_title if custom_title else (chat.title or "Channel")
                channel_handle = f"@{getattr(chat, 'username', None)}" if getattr(chat, "username", None) else display_title
                
                # Build caption in MarkdownV2
                linked_title = "[" + _escape_md_v2("Title'-") + f"]({_escape_md_v2_url(photo_link)})"
                expire_seconds = 600
                caption = (
                    f"{linked_title}{_escape_md_v2(channel_handle)}"
                    f"{_escape_md_v2('𝖳𝗁𝗂𝗌 𝗅𝗂𝗇𝗄 𝗐𝗂𝗅𝗅 𝖾𝗑𝗉𝗂𝗋𝖾 𝗂𝗇 ')}{_escape_md_v2(str(expire_seconds))}"
                    f"{_escape_md_v2(' seconds.')}"
                )
                try:
                    await message.reply_photo(
                        photo=photo_link,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN_V2,
                        reply_markup=button
                    )
                except Exception as e:
                    print(f"[start] send_photo markdown failed: {e}")
                    fallback_caption = f"Title'- {channel_handle} This link will expire in 600 seconds."
                    await message.reply_photo(
                        photo=photo_link,
                        caption=fallback_caption,
                        reply_markup=button
                    )
            else:
                # Fallback to previous text behavior
                await message.reply_text("Here is your link! Click below to proceed:", reply_markup=button)

        except Exception as e:
            # Ensure placeholder is removed on errors to avoid clutter
            if placeholder:
                try: await placeholder.delete()
                except Exception: pass
            await message.reply_text("⚠️ Invalid or expired link.")
            print(f"Decoding error: {e}")
    else:
        # Remove any stray placeholder in no-payload branch
        if placeholder:
            try: await placeholder.delete()
            except Exception: pass
        inline_buttons = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("About Me", callback_data="help"),
                 InlineKeyboardButton("Close", callback_data="close")]
            ]
        )
        
        await message.reply_text(
            "<b><i>Welcome to the advanced links sharing bot.\nWith this bot, you can share links and keep your channels safe from copyright issues</i></b>",
            reply_markup=inline_buttons
        )
        
#=====================================================================================##

WAIT_MSG = """"<b>Processing ....</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message with out any spaces.</code>"""

#=====================================================================================##

@Client.on_message(filters.command('users') & filters.user(OWNER_ID))
async def get_users(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


#=====================================================================================##

@Client.on_message(filters.private & filters.command('broadcast') & filters.user(OWNER_ID))
async def send_text(client: Client, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time </i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

#=====================================================================================##

@Client.on_callback_query(filters.regex("help"))
async def help_callback(client: Client, callback_query):
    # Define the inline keyboard with the "Close" button
    inline_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Close", callback_data="close")]
        ]
    )
    
    
    await callback_query.answer()
    await callback_query.message.edit_text("<b><i>About Us..\n\n‣ Made for : @Anime_X_Hunters\n‣ Owned by : @Okabe_xRintarou\n‣ Developer : @The_Seishiro_Nagi\n\n Adios !!</i></b>", reply_markup=inline_buttons)

@Client.on_callback_query(filters.regex("close"))
async def close_callback(client: Client, callback_query):
    await callback_query.answer()
    await callback_query.message.delete()

#=====================================================================================##


user_message_count = {}
user_banned_until = {}

MAX_MESSAGES = 3
TIME_WINDOW = timedelta(seconds=10)  # Capturing frames
BAN_DURATION = timedelta(hours=1)  # User ko ban rakhne ka time. hours ko minutes karlena

@Client.on_message(filters.private)
async def monitor_messages(client: Client, message: Message):
    user_id = message.from_user.id
    now = datetime.now()

    if user_id in ADMINS:
        return 

    
    if user_id in user_banned_until and now < user_banned_until[user_id]:
        await message.reply_text("⚠️ You are temporarily banned from using commands due to spamming. Try again later.")
        return

    if user_id not in user_message_count:
        user_message_count[user_id] = []

    user_message_count[user_id].append(now)

    user_message_count[user_id] = [time for time in user_message_count[user_id] if now - time <= TIME_WINDOW]

    if len(user_message_count[user_id]) > MAX_MESSAGES:
        user_banned_until[user_id] = now + BAN_DURATION
        await message.reply_text("🚫 You have been temporarily banned for spamming. Try again in 1 hour.")
        return

# Function to get channels (dummy implementation)
async def get_channels():
    # This should be replaced with actual logic to fetch channels
    return [123456789, 987654321]
