# Gmail to Telegram Forwarder

This Python script automatically forwards unread Gmail emails to your Telegram chat.

## Features

- Monitors your Gmail inbox for unread emails
- Forwards email details (subject, sender, date, content) to Telegram
- Marks forwarded emails as read in Gmail
- Runs continuously or as a one-time check
- Configurable check intervals
- **Docker support for easy hosting and deployment**

## Quick Start

For quick deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Setup

### Prerequisites

- Python 3.6+
- Gmail account with API access
- Telegram account and bot

### 1. Gmail API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials as `credentials.json` and place it in the project root

### 2. Telegram Bot Setup

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot and get your bot token
3. Message [@userinfobot](https://t.me/userinfobot) to get your chat ID

### 3. Environment Setup

1. Copy `.env.example` to `.env`
2. Fill in your actual `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Script

**One-time check:**
```bash
python email_to_telegram.py --once
```

**Continuous monitoring (default, checks every 5 minutes):**
```bash
python email_to_telegram.py
```

**Continuous monitoring with custom interval:**
```bash
python email_to_telegram.py 10  # checks every 10 minutes
```

## Security Notes

- Never commit `credentials.json`, `token.json`, or `.env` files to version control
- Keep your API keys and tokens secure
- The `.gitignore` file is configured to exclude sensitive files

## How It Works

The script uses Gmail's API to check for unread emails (up to 10 at a time) and forwards their details to Telegram. Successfully forwarded emails are marked as read in Gmail to avoid duplicate forwarding.

## Hosting & Deployment

This application can be hosted and run continuously on any server using Docker.

### Option 1: Docker Compose (Recommended)

Docker Compose is the easiest way to deploy this application in a container.

**Prerequisites:**
- Docker and Docker Compose installed on your server
- Gmail API credentials (`credentials.json`)
- `.env` file with your Telegram configuration

**Steps:**

1. **Prepare your files:**
   ```bash
   # Make sure you have these files in your project directory:
   # - credentials.json (from Gmail API setup)
   # - .env (with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
   # - token.json (will be created on first run after OAuth authentication)
   ```

2. **Build and start the container:**
   ```bash
   docker-compose up -d
   ```

3. **First-time OAuth authentication:**
   - On first run, you'll need to authenticate with Gmail
   - Check the logs to get the authentication URL:
     ```bash
     docker-compose logs -f
     ```
   - Follow the URL, authenticate, and the token will be saved

4. **Manage the service:**
   ```bash
   # View logs
   docker-compose logs -f
   
   # Stop the service
   docker-compose down
   
   # Restart the service
   docker-compose restart
   
   # Update and rebuild
   docker-compose up -d --build
   ```

5. **Custom check interval:**
   - Edit `docker-compose.yml` and uncomment/modify the `command` line:
     ```yaml
     command: ["python", "email_to_telegram.py", "10"]  # Check every 10 minutes
     ```

### Option 2: Docker (Manual)

If you prefer to use Docker without Compose:

**Build the image:**
```bash
docker build -t gmail-to-telegram .
```

**Run the container:**
```bash
docker run -d \
  --name gmail-to-telegram-bot \
  --restart unless-stopped \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  -v $(pwd)/token.json:/app/token.json \
  -v $(pwd)/data:/app/data \
  -e TELEGRAM_BOT_TOKEN="your_token_here" \
  -e TELEGRAM_CHAT_ID="your_chat_id_here" \
  gmail-to-telegram
```

**Custom interval:**
```bash
docker run -d \
  --name gmail-to-telegram-bot \
  --restart unless-stopped \
  -v $(pwd)/credentials.json:/app/credentials.json:ro \
  -v $(pwd)/token.json:/app/token.json \
  -e TELEGRAM_BOT_TOKEN="your_token_here" \
  -e TELEGRAM_CHAT_ID="your_chat_id_here" \
  gmail-to-telegram \
  python email_to_telegram.py 10
```

### Option 3: Cloud Platforms

#### Deploy to Heroku

1. Create a `Procfile` (see below)
2. Set environment variables in Heroku dashboard
3. Deploy using Git:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Deploy to Google Cloud Run / AWS / Azure

The provided Dockerfile is compatible with most cloud container platforms. Follow your platform's specific deployment guide for containers.

### Option 4: Traditional Server

For deploying on a Linux server without Docker:

1. **Install Python and dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   ```

2. **Create a systemd service** (for automatic startup):
   
   Create `/etc/systemd/system/gmail-to-telegram.service`:
   ```ini
   [Unit]
   Description=Gmail to Telegram Forwarder
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/gmail-to-telegram
   ExecStart=/usr/bin/python3 /path/to/gmail-to-telegram/email_to_telegram.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service:**
   ```bash
   sudo systemctl enable gmail-to-telegram
   sudo systemctl start gmail-to-telegram
   sudo systemctl status gmail-to-telegram
   ```

### Monitoring

**Check if the service is running:**
```bash
# Docker Compose
docker-compose ps

# Docker
docker ps | grep gmail-to-telegram

# Systemd
sudo systemctl status gmail-to-telegram
```

**View logs:**
```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f gmail-to-telegram-bot

# Systemd
sudo journalctl -u gmail-to-telegram -f
```