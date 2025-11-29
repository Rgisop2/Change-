# Use updated, supported & stable base image
FROM python:3.10-slim

# Install git ONLY if your requirements have git+ dependencies
# Comment this line out if not needed (saves RAM)
RUN apt update && apt install -y git && apt clean

# Set working directory
WORKDIR /app

# Copy requirements first (better docker caching)
COPY requirements.txt .

# Install python libraries
RUN pip3 install --no-cache-dir -U pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Start the bot
CMD ["python3", "main.py"]
