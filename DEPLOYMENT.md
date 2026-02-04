# Quick Deployment Guide

This guide provides quick-start instructions for deploying the Gmail to Telegram forwarder.

## Prerequisites

Before deploying, ensure you have:
- [ ] Gmail API credentials (`credentials.json`)
- [ ] Telegram bot token (from @BotFather)
- [ ] Telegram chat ID (from @userinfobot)

## Fastest Deployment (Docker Compose)

> **Note:** These examples use `docker compose` (Compose V2 syntax). If you have an older version, use `docker-compose` (with hyphen) instead.

### Step 1: Prepare Environment

Create a `.env` file in the project root:
```bash
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here
```

### Step 2: Add Gmail Credentials

Place your `credentials.json` file (from Google Cloud Console) in the project root.

### Step 3: Deploy

```bash
# Build and start the service
docker compose up -d

# View logs (first-time OAuth authentication will show here)
docker compose logs -f
```

### Step 4: First-Time Authentication

On first run, you'll need to authenticate with Gmail:
1. Check the logs for an authentication URL
2. Visit the URL in your browser
3. Grant permissions to your Google account
4. The `token.json` will be created automatically

### Step 5: Verify

```bash
# Check if service is running
docker compose ps

# View recent logs
docker compose logs --tail=50
```

## Production Tips

### Change Check Interval

Edit `docker compose.yml` and uncomment/modify:
```yaml
command: ["python", "email_to_telegram.py", "10"]  # Check every 10 minutes
```

Then restart:
```bash
docker compose up -d
```

### Monitor Service

```bash
# View live logs
docker compose logs -f

# Check resource usage
docker stats gmail-to-telegram-bot
```

### Restart Service

```bash
# Restart after configuration changes
docker compose restart

# Full rebuild after code changes
docker compose up -d --build
```

### Backup Important Files

Always backup these files:
- `credentials.json` - Gmail API credentials
- `token.json` - OAuth token (created after first authentication)
- `.env` - Environment variables

### Stop Service

```bash
docker compose down
```

## Alternative: Heroku Deployment

For Heroku (free tier available with credit card):

```bash
# Install Heroku CLI, then:
heroku login
heroku create your-app-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TELEGRAM_CHAT_ID=your_chat_id
git push heroku main
```

**Note**: First-time Gmail authentication on Heroku requires additional setup due to the OAuth flow.

## Troubleshooting

### Container won't start
```bash
# Check logs for errors
docker compose logs

# Verify environment variables
docker compose config
```

### Gmail authentication fails
- Ensure `credentials.json` is present and valid
- Check that Gmail API is enabled in Google Cloud Console
- Verify OAuth consent screen is configured

### Telegram messages not sending
- Verify bot token is correct
- Check chat ID is correct
- Ensure bot can send messages (try sending a test message to the bot first)

### Messages not being marked as read
- Check Gmail API permissions (should have 'modify' scope)
- Verify token.json is being persisted (check volumes in docker compose.yml)

## Support

For issues and questions, please visit the [GitHub repository](https://github.com/parsasamandi/gmail-to-telegram/issues).
