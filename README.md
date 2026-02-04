# Gmail to Telegram Forwarder

This Python script automatically forwards unread Gmail emails to your Telegram chat.

## Features

- Monitors your Gmail inbox for unread emails
- Forwards email details (subject, sender, date, content) to Telegram
- Marks forwarded emails as read in Gmail
- Runs continuously or as a one-time check
- Configurable check intervals

## Setup Options

You can run this forwarder in two ways:
- **Option A**: Run on GitHub Actions (recommended - no local setup needed)
- **Option B**: Run locally on your machine

---

## Option A: Run on GitHub Actions (Recommended)

This option runs the email forwarder automatically on GitHub's servers every 5 minutes. No local setup required!

### Prerequisites

- GitHub account
- Gmail account with API access
- Telegram account and bot

### 1. Gmail API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID)
   - Set application type to "Desktop app"
5. Download the credentials JSON file

### 2. Telegram Bot Setup

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot` command and get your bot token
3. Message [@userinfobot](https://t.me/userinfobot) to get your chat ID

### 3. Initial Authentication (One-time, run locally)

Before running on GitHub, you need to authenticate with Gmail once to generate the `token.json` file:

```bash
# Clone this repository
git clone https://github.com/parsasamandi/gmail-to-telegram.git
cd gmail-to-telegram

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID

# Place your downloaded credentials.json in the project root

# Run once to authenticate
python email_to_telegram.py --once
```

This will open a browser window for Gmail authentication. After successful authentication, a `token.json` file will be created.

### 4. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

1. **GMAIL_CREDENTIALS**: Copy the entire content of your `credentials.json` file
2. **GMAIL_TOKEN**: Copy the entire content of the generated `token.json` file
3. **TELEGRAM_BOT_TOKEN**: Your Telegram bot token from BotFather
4. **TELEGRAM_CHAT_ID**: Your Telegram chat ID from userinfobot

### 5. Enable GitHub Actions

1. Go to the "Actions" tab in your GitHub repository
2. Enable workflows if prompted
3. The workflow will automatically run every 5 minutes
4. You can also manually trigger it using the "Run workflow" button

### 6. Monitor Execution

- Go to Actions tab to see workflow runs
- Check your Telegram chat for forwarded emails
- View logs for any issues

---

## Option B: Run Locally

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
- When using GitHub Actions, store all credentials in GitHub Secrets (never in code)

## Troubleshooting

### GitHub Actions Issues

**Authentication errors:**
- Ensure all secrets are properly set in GitHub repository settings
- Verify that GMAIL_CREDENTIALS and GMAIL_TOKEN contain valid JSON
- Check that TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are correct

**Token expiration:**
- Gmail tokens can expire. If authentication fails, regenerate `token.json` locally and update the GMAIL_TOKEN secret

**Rate limits:**
- The default schedule runs every 5 minutes. Adjust the cron schedule in `.github/workflows/email-forwarder.yml` if needed
- Gmail API has rate limits. The workflow processes up to 5 unread emails per run

### Local Run Issues

**Authentication fails:**
- Ensure `credentials.json` is in the project root
- Delete `token.json` and run again to re-authenticate
- Check that Gmail API is enabled in Google Cloud Console

## How It Works

The script uses Gmail's API to check for unread emails (up to 10 at a time) and forwards their details to Telegram. Successfully forwarded emails are marked as read in Gmail to avoid duplicate forwarding.