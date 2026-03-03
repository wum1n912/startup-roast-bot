import os
import json
import re
import time
import asyncio
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

# Config
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8772323308:AAG4GIJIYF85yean_yq7oONY6DjdUVqrnEc")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY", "sk-4OlfcBWGTFLTqpst9oKhrZDRDOmyMx2ApVdycUUoG5Us3bIR")

# Proxy settings for VPN
PROXY_URL = "socks5://127.0.0.1:1080"

# Initialize clients
openai_client = AsyncOpenAI(
    api_key=MOONSHOT_API_KEY,
    base_url="https://api.moonshot.cn/v1"
)

# Store conversation context for follow-ups
user_context = {}

async def analyze_startup(idea: str, mode: str = "roast") -> str:
    """Analyze a startup idea using Kimi K2.5"""
    
    if mode == "roast":
        prompt = f"""You are a brutally honest venture capitalist who gives startup teardowns. 
        
Analyze this startup idea: "{idea}"

Provide a structured teardown with these exact sections:

What you think you're building: [one line summary of their pitch]
What you're actually building: [the harsh reality of what it really is]
Why a16z passes: [specific reason VCs would reject, be witty and reference startup tropes]
Funding probability: [X.X% - be realistic, usually low]
The one thing that could save this: [actual strategic pivot or moat suggestion]

Tone: sharp, witty, specific to the input. No generic responses. Reference specific details from their idea."""

    elif mode == "roastmore":
        prompt = f"""You already roasted this startup idea: "{idea}"

Now provide DEEPER analysis:

Market Analysis:
- TAM/SAM/SOM breakdown with realistic numbers
- 3 key market risks most founders miss
- Why this market is harder than it looks

Competitor Teardown:
- Who's actually winning in this space
- What the incumbent has that the founder doesn't
- Why "we're different" usually isn't enough

The Real Business Model:
- What their actual unit economics probably look like
- Customer acquisition reality check
- Why their pricing is probably wrong

Be specific, use real market knowledge, don't hold back."""

    elif mode == "pivotme":
        prompt = f"""The user pitched: "{idea}" 

It's not fundable as-is. Give them 3 ADJACENT ideas that are ACTUALLY more fundable:

For each pivot:
1. [Pivot Name]
   - The insight: [why this adjacent space works better]
   - The moat: [what creates defensibility here]
   - Why VCs care: [what makes this venture-backable]
   - The risk: [honest downside]

All 3 pivots should leverage their existing skills/domain but fix the fatal flaw in their original idea.
Be creative but realistic."""

    elif mode == "comparps":
        prompt = f"""Find real companies that tried something similar to: "{idea}"

Return exactly 3 companies with:

1. [Company Name] ([founded year])
   - What they did: [specific description]
   - Outcome: [acquired/defunct/public/operating - be specific with year and price if known]
   - Lesson: [what founders should learn from this]

2. [Company Name] ([founded year])
   [same format]

3. [Company Name] ([founded year])
   [same format]

IMPORTANT: These must be REAL companies. If you don't know exact outcomes, say "outcome unclear" rather than hallucinating. Include real years and acquisition prices where known."""

    else:
        return "Invalid mode"
    
    try:
        response = await openai_client.chat.completions.create(
            model="kimi-k2.5",
            messages=[
                {"role": "system", "content": "You are an expert startup analyst and venture capitalist. You give brutally honest, specific, witty feedback. Never use generic responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🚀 Startup Roast Bot\n\n"
        "Send me any startup idea and I'll give you the brutal truth.\n\n"
        "Commands:\n"
        "/roastmore - Deeper market analysis\n"
        "/pivotme - 3 better adjacent ideas\n"
        "/comparps - Real companies that tried this\n\n"
        "Just send your idea as text to get started!"
    )

async def handle_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle startup idea text"""
    idea = update.message.text
    user_id = update.effective_user.id
    
    # Store for follow-up commands
    user_context[user_id] = {"idea": idea, "timestamp": datetime.now()}
    
    # Send "typing" indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Get analysis
    response = await analyze_startup(idea, mode="roast")
    
    await update.message.reply_text(response, parse_mode="HTML")

async def roastmore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /roastmore command"""
    user_id = update.effective_user.id
    
    if user_id not in user_context:
        await update.message.reply_text("Send me a startup idea first!")
        return
    
    idea = user_context[user_id]["idea"]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    response = await analyze_startup(idea, mode="roastmore")
    await update.message.reply_text(response, parse_mode="HTML")

async def pivotme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pivotme command"""
    user_id = update.effective_user.id
    
    if user_id not in user_context:
        await update.message.reply_text("Send me a startup idea first!")
        return
    
    idea = user_context[user_id]["idea"]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    response = await analyze_startup(idea, mode="pivotme")
    await update.message.reply_text(response, parse_mode="HTML")

async def comparps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /comparps command"""
    user_id = update.effective_user.id
    
    if user_id not in user_context:
        await update.message.reply_text("Send me a startup idea first!")
        return
    
    idea = user_context[user_id]["idea"]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    response = await analyze_startup(idea, mode="comparps")
    await update.message.reply_text(response, parse_mode="HTML")

async def main():
    """Start the bot"""
    from telegram.request import HTTPXRequest
    
    # Use SOCKS5 proxy
    request = HTTPXRequest(proxy=PROXY_URL)
    application = Application.builder().token(TELEGRAM_TOKEN).request(request).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("roastmore", roastmore))
    application.add_handler(CommandHandler("pivotme", pivotme))
    application.add_handler(CommandHandler("comparps", comparps))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_idea))
    
    print("🚀 Bot starting...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    
    # Keep running
    print("✅ Bot is running! Press Ctrl+C to stop.")
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
