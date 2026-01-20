# Gmail to Telegram Forwarder

This Python script automatically forwards unread Gmail emails to your Telegram chat.

## Features

- Monitors your Gmail inbox for unread emails
- Forwards email details (subject, sender, date, content) to Telegram
- Marks forwarded emails as read in Gmail
- Runs continuously or as a one-time check
- Configurable check intervals

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