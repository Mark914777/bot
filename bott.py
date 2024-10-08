import logging
import shelve
from collections import defaultdict

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    user_name = user.full.name
    pandora = shelve.open("pandora")
    if str(user_id) not in pandora.keys():
        user_data = {
            "user_name": user_name,
            "Subs": "Free",
            "tokens": 0
        }
    pandora[str(user_id)] = user_data
    await update.message.reply_html (rf"Ку {pandora[str(user_id)]["user_name"]}")
    pandora.close()

    async def profile(update: Update) -> None:
        user = update.effective_user
        user_id =str(user.id)
        pandora = shelve.open("pandora")
        subscription_type = pandora[str(user_id)]["subs"]
        tokens = pandora[str(user_id)]['tokens']
        name = pandora[str(user_id)]['user_name']
        profile_text = (
            f"Это ваш профиль. \n"
            f"Имя: "
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Чтобы начать, пиши /start \n"
        "За помощью пиши /help \n"
    )
    """Send a message when the command /help is issued."""
    await update.message.reply_text(help_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    """Echo the user message."""
    await update.message.reply_text(message)




def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7941937010:AAHLKI5TcCzep7S-5zAuuSCYAShjZENALf0").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("profile", profile))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()