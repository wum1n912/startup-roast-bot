# Startup Roast Bot

A Telegram bot that brutally analyzes startup ideas using AI.

## Features

- **Instant Roast**: Send any startup idea, get a structured teardown
- **/roastmore**: Deep market analysis and competitor teardown  
- **/pivotme**: 3 adjacent ideas that are actually more fundable
- **/comparps**: Real companies that tried something similar and what happened

## Setup

```bash
pip install -r requirements.txt
export TELEGRAM_TOKEN="your_bot_token"
export MOONSHOT_API_KEY="your_kimi_api_key"
python bot.py
```

## How it works

1. Send any startup idea as text
2. Bot analyzes using Kimi K2.5
3. Get structured feedback:
   - What you think you're building
   - What you're actually building  
   - Why a16z passes
   - Funding probability
   - The one thing that could save it

## Tech Stack

- python-telegram-bot
- Moonshot AI (Kimi K2.5)

## License

MIT
