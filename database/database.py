import motor.motor_asyncio
import base64
from config import DB_URI, DB_NAME
from datetime import datetime, timedelta

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']
channels_collection = database["channels"]
encoded_links_collection = database["links"]
banned_users_collection = database["banned_users"]

async def add_user(user_id: int):
    existing_user = await user_data.find_one({'_id': user_id})
    if existing_user:
        return 
    
    try:
        await user_data.insert_one({'_id': user_id})
    except Exception as e:
        print(f"Error adding user {user_id}: {e}")

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def full_userbase():
    user_docs = user_data.find()
    return [doc['_id'] async for doc in user_docs]

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})

##-------------------------------------------------------------------

async def is_admin(user_id: int):
    return bool(await admins_collection.find_one({'_id': user_id}))

##-------------------------------------------------------------------

async def save_channel(channel_id: int, title: str = None):
    """Save a channel_id to the database with optional custom title."""
    update_data = {"channel_id": channel_id, "invite_link_expiry": None}
    if title:
        update_data["custom_title"] = title
    await channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": update_data}, 
        upsert=True
    )

async def get_channels():
    """Get all channels from the database (No limit)"""
    channels = await channels_collection.find().to_list(None) 
    return [channel["channel_id"] for channel in channels]


async def delete_channel(channel_id: int):
    """Delete a channel from the database"""
    await channels_collection.delete_one({"channel_id": channel_id})

async def get_channel_title(channel_id: int):
    """Get the custom title or channel name for a channel."""
    channel = await channels_collection.find_one({"channel_id": channel_id})
    if channel and channel.get("custom_title"):
        return channel["custom_title"]
    return None

##-------------------------------------------------------------------

async def save_encoded_link(channel_id: int):
    encoded_link = base64.urlsafe_b64encode(str(channel_id).encode()).decode()
    await channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"encoded_link": encoded_link, "status": "active"}},
        upsert=True
    )
    return encoded_link


async def get_channel_by_encoded_link(encoded_link: str):
    channel = await channels_collection.find_one({"encoded_link": encoded_link, "status": "active"})
    return channel["channel_id"] if channel else None

##-------------------------------------------------------------------

async def save_encoded_link2(channel_id: int, encoded_link: str):
    await channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"req_encoded_link": encoded_link, "status": "active"}},
        upsert=True
    )
    return encoded_link

async def get_channel_by_encoded_link2(encoded_link: str):
    channel = await channels_collection.find_one({"req_encoded_link": encoded_link, "status": "active"})
    return channel["channel_id"] if channel else None

async def save_channel_photo(channel_id: int, photo_link: str):
    """Save/Update the photo link for a channel."""
    await channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"photo_link": photo_link}},
        upsert=True
    )

async def get_channel_photo_link(channel_id: int):
    """Return the stored photo link for a channel, if any."""
    channel = await channels_collection.find_one({"channel_id": channel_id})
    if not channel:
        return None
    return channel.get("photo_link")

##-------------------------------------------------------------------

async def ban_user(user_id: int):
    """Ban a user from using the bot."""
    await banned_users_collection.insert_one({"_id": user_id, "banned_at": datetime.now()})

async def unban_user(user_id: int):
    """Unban a user."""
    await banned_users_collection.delete_one({"_id": user_id})

async def is_user_banned(user_id: int):
    """Check if a user is banned."""
    return bool(await banned_users_collection.find_one({"_id": user_id}))

async def get_all_banned_users():
    """Get list of all banned users."""
    banned = await banned_users_collection.find().to_list(None)
    return [doc["_id"] for doc in banned]

async def save_global_shared_link(channel_id: int, link: str, expiry: str):
    """Save a single shared link for all users of a channel."""
    await channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"global_link": link, "global_link_expiry": expiry, "is_request": False}},
        upsert=True
    )

async def save_global_shared_request_link(channel_id: int, link: str, expiry: str):
    """Save a single shared request link for all users of a channel."""
    await channels_collection.update_one(
        {"channel_id": channel_id},
        {"$set": {"global_request_link": link, "global_request_link_expiry": expiry, "is_request": True}},
        upsert=True
    )

async def get_global_shared_link(channel_id: int):
    """Get the current shared link if valid, else None."""
    channel = await channels_collection.find_one({"channel_id": channel_id})
    if not channel:
        return None
    
    global_link = channel.get("global_link")
    expiry = channel.get("global_link_expiry")
    
    if global_link and expiry and datetime.fromisoformat(expiry) > datetime.now():
        return global_link
    return None

async def get_global_shared_request_link(channel_id: int):
    """Get the current shared request link if valid, else None."""
    channel = await channels_collection.find_one({"channel_id": channel_id})
    if not channel:
        return None
    
    request_link = channel.get("global_request_link")
    expiry = channel.get("global_request_link_expiry")
    
    if request_link and expiry and datetime.fromisoformat(expiry) > datetime.now():
        return request_link
    return None
