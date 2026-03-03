import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

# Config - use environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY", "sk-4OlfcBWGTFLTqpst9oKhrZDRDOmyMx2ApVdycUUoG5Us3bIR")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable required")

openai_client = AsyncOpenAI(
    api_key=MOONSHOT_API_KEY,
    base_url="https://api.moonshot.cn/v1"
)

user_context = {}

async def analyze_startup(idea: str, mode: str = "roast") -> str:
    """Analyze a startup idea using Kimi K2.5"""
    
    if mode == "roast":
        prompt = f"""You are a brutally honest venture capitalist. 
        
Analyze this startup idea: "{idea}"

Provide a structured teardown:

What you think you're building: [one line summary]
What you're actually building: [harsh reality]
Why a16z passes: [specific VC rejection reason]
Funding probability: [X.X%]
The one thing that could save this: [strategic pivot]

Tone: sharp, witty, specific."""

    elif mode == "roastmore":
        prompt = f"""Deeper analysis of: "{idea}"

Market Analysis:
- TAM/SAM/SOM breakdown
- 3 key market risks
- Why this market is harder than it looks

Competitor Teardown:
- Who's winning in this space
- What incumbents have that you don't

Be specific."""

    elif mode == "pivotme":
        prompt = f"""The idea "{idea}" isn't fundable. Give 3 ADJACENT ideas that are ACTUALLY more fundable:

For each pivot:
1. [Pivot Name]
   - The insight: [why this works better]
   - The moat: [defensibility]
   - Why VCs care: [venture-backable aspect]

Be creative but realistic."""

    elif mode == "comparps":
        prompt = f"""Find 3 real companies that tried something similar to: "{idea}"

For each:
1. [Company Name] ([year])
   - What they did: [description]
   - Outcome: [acquired/defunct/public - real info]
   - Lesson: [what founders should learn]

IMPORTANT: Real companies only. Say "outcome unclear" if unknown."""

    else:
        return "Invalid mode"
    
    try:
        response = await openai_client.chat.completions.create(
            model="kimi-k2.5",
            messages=[
                {"role": "system", "content": "You are an expert startup analyst. Be brutally honest and specific."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Startup Roast Bot\n\n"
        "Send me any startup idea for a brutal teardown.\n\n"
        "Commands:\n"
        "/roastmore - Deeper analysis\n"
        "/pivotme - 3 better adjacent ideas\n"
        "/comparps - Real companies that tried this"
    )

async def handle_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idea = update.message.text
    user_id = update.effective_user.id
    user_context[user_id] = {"idea": idea}
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = await analyze_startup(idea, mode="roast")
    await update.message.reply_text(response)

async def roastmore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_context:
        await update.message.reply_text("Send me a startup idea first!")
        return
    
    idea = user_context[user_id]["idea"]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = await analyze_startup(idea, mode="roastmore")
    await update.message.reply_text(response)

async def pivotme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_context:
        await update.message.reply_text("Send me a startup idea first!")
        return
    
    idea = user_context[user_id]["idea"]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = await analyze_startup(idea, mode="pivotme")
    await update.message.reply_text(response)

async def comparps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_context:
        await update.message.reply_text("Send me a startup idea first!")
        return
    
    idea = user_context[user_id]["idea"]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = await analyze_startup(idea, mode="comparps")
    await update.message.reply_text(response)

def main():
    """Start the bot"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("roastmore", roastmore))
    application.add_handler(CommandHandler("pivotme", pivotme))
    application.add_handler(CommandHandler("comparps", comparps))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_idea))
    
    print("🚀 Bot starting...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
