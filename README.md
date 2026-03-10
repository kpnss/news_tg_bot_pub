# 📰 Telegram RSS Bot

A simple Python bot that checks a list of RSS feeds and sends new articles to a Telegram chat. It keeps track of already-sent links using a SQLite database to avoid duplicates.

## How it works

1. The bot fetches all RSS feeds from a user-defined list
2. Each article is checked against the local database
3. If the article hasn't been sent yet, it's forwarded to the specified Telegram chat
4. The database is updated with the new entries

## Configuration

The bot requires three variables to work:

| Variable | Description |
|---|---|
| `TELEGRAM_TOKEN` | Your Telegram bot token from @BotFather |
| `CHAT_ID` | The Telegram chat ID where articles will be sent |
| `CHOSEN_URLS` | Comma-separated list of RSS feed URLs |

## Running with GitHub Actions (recommended)

The repository includes a workflow that runs the bot every 8 hours automatically. The SQLite database is committed back to the repo after each run to ensure persistence across executions.

1. Fork the repository
2. Go to **Settings → Secrets and variables → Actions**
3. Add the three variables above as repository secrets
4. Enable **Read and write permissions** under **Settings → Actions → General → Workflow permissions**
5. Trigger the workflow manually from the **Actions** tab to test it

## Running with Docker

A `Dockerfile` is also available for local use or alternative deployments.

1. Create a `.env` file in the root of the project:
```
TELEGRAM_TOKEN=your_token
CHAT_ID=your_chat_id
CHOSEN_URLS=https://feed1.com,https://feed2.com
```

2. Build and run:
```bash
docker build -t tg-rss-bot .
docker run --env-file .env tg-rss-bot
```

> Note: with Docker, the database is not persistent between runs unless you mount a volume.