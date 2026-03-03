# Startup Roast Bot

A Telegram bot that brutally analyzes startup ideas using Kimi K2.5 AI.

## Features

- **Instant Roast**: Send any startup idea, get a structured teardown
- **/roastmore**: Deep market analysis and competitor teardown  
- **/pivotme**: 3 adjacent ideas that are actually more fundable
- **/comparps**: Real companies that tried something similar and what happened

## Quick Deploy (Free Options)

### Option 1: Render.com (Recommended)
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `wum1n912/startup-roast-bot`
4. Set environment variables:
   - `TELEGRAM_TOKEN`: `8772323308:AAG4GIJIYF85yean_yq7oONY6DjdUVqrnEc`
   - `MOONSHOT_API_KEY`: `sk-4OlfcBWGTFLTqpst9oKhrZDRDOmyMx2ApVdycUUoG5Us3bIR`
5. Click "Create Web Service" (Free tier)

### Option 2: Heroku
```bash
# Install Heroku CLI, then:
heroku login
heroku create startup-roast-bot
heroku config:set TELEGRAM_TOKEN=8772323308:AAG4GIJIYF85yean_yq7oONY6DjdUVqrnEc
heroku config:set MOONSHOT_API_KEY=sk-4OlfcBWGTFLTqpst9oKhrZDRDOmyMx2ApVdycUUoG5Us3bIR
git push heroku main
```

### Option 3: PythonAnywhere
1. Go to https://www.pythonanywhere.com
2. Create free account
3. Open Bash console:
```bash
git clone https://github.com/wum1n912/startup-roast-bot.git
cd startup-roast-bot
pip install -r requirements.txt
export TELEGRAM_TOKEN=8772323308:AAG4GIJIYF85yean_yq7oONY6DjdUVqrnEc
export MOONSHOT_API_KEY=sk-4OlfcBWGTFLTqpst9oKhrZDRDOmyMx2ApVdycUUoG5Us3bIR
python bot.py
```

## Local Development

```bash
pip install -r requirements.txt
export TELEGRAM_TOKEN=your_token
export MOONSHOT_API_KEY=your_key
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
