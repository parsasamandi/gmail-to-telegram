# Quick Setup Guide for GitHub Actions

This guide will help you set up the Gmail to Telegram forwarder to run manually on GitHub Actions.

## Prerequisites

You need:
- A Gmail account
- A Telegram account
- A GitHub account (you're here!)

## Step-by-Step Setup

### 1. Set up Gmail API (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download the JSON file (this is your `credentials.json`)

### 2. Set up Telegram Bot (2 minutes)

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the prompts
3. Save your bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
4. Message [@userinfobot](https://t.me/userinfobot) to get your chat ID

### 3. Authenticate Locally (One Time - 3 minutes)

```bash
# Clone this repository
git clone https://github.com/parsasamandi/gmail-to-telegram.git
cd gmail-to-telegram

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
echo "TELEGRAM_CHAT_ID=your_chat_id_here" >> .env

# Add your credentials.json file to the folder

# Run once to authenticate (browser will open)
python email_to_telegram.py --once
```

After successful authentication, you'll have a `token.json` file.

### 4. Add Secrets to GitHub (2 minutes)

Go to: **Your Repository → Settings → Secrets and variables → Actions → New repository secret**

Add these 4 secrets:

| Secret Name | Value |
|------------|-------|
| `GMAIL_CREDENTIALS` | Content of `credentials.json` (entire file) |
| `GMAIL_TOKEN` | Content of `token.json` (entire file) |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID |

💡 **Tip**: Open the JSON files in a text editor and copy the entire content (including all the curly braces).

### 5. Enable the Workflow (1 minute)

1. Go to the **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. Click "Run workflow" to trigger it manually

## That's It! 🎉

Your emails will now be forwarded to Telegram whenever you manually trigger the workflow.

## Verify It's Working

1. Send yourself a test email
2. Go to Actions tab and manually trigger the workflow
3. Check your Telegram for the forwarded message

## Troubleshooting

**Workflow fails?**
- Check that all 4 secrets are set correctly
- Verify the JSON content is valid (no missing braces)
- Look at the workflow logs for specific error messages

**Not receiving emails?**
- Make sure your bot token and chat ID are correct
- Test locally first to verify everything works

**Need help?**
- Check the full [README.md](../README.md) for detailed documentation
- Review workflow logs in the Actions tab
