import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from embedder import initialize_engine, search

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user_name = update.effective_user.first_name
    
    welcome_text = f"hey, {user_name}!"
    
    await update.message.reply_text(welcome_text, parse_mode="Markdown")
    logger.info(f"user {user_name} started the bot")


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if not context.args:
        await update.message.reply_text("❌ using: /search your query")
        return
    
    query = " ".join(context.args)
    
    await update.message.chat.send_action("typing")
    
    try:
        results = search(query, top_k=3)
        
        response = f"*Search results for:* `{query}`\n\n"
        
        for i, result in enumerate(results, 1):
            response += f"*{i}. {result['title']}*\n"
            response += f"*Relevance:* `{result['score']*100:.1f}%`\n"
        
        await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error during search: {e}")
        await update.message.reply_text("❌ An error occurred during search")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    
    query = update.message.text
    
    await update.message.chat.send_action("typing")
    
    try:
        results = search(query, top_k=3)
        response = f"🔍 *Search results for:* `{query}`\n\n"
        
        for i, result in enumerate(results, 1):
            response += f"*{i}. {result['title']}*\n"
            response += f"*Relevance:* `{result['score']*100:.1f}%`\n"
        
        await update.message.reply_text(response, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error during search: {e}")
        await update.message.reply_text("❌ An error occurred during search")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """Help text here"""
    await update.message.reply_text(help_text)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    logger.error(f"Error: {context.error}")


def main() -> None:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN not found")
    
    initialize_engine() 
    
    application = Application.builder().token(TOKEN).build()
 
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()