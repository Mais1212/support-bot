import logging
import os
from functools import partial

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from dialogflow import get_project_id, process_with_dialogflow

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)


def run_tg_bot(bot_token: str, project_id: str) -> None:
    """Start the bot."""
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", _start))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, partial(_chat, project_id=project_id)
    ))

    application.run_polling()


async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_html(
        f"Здравствуйте.",
        reply_markup=ForceReply(selective=True),
    )


async def _chat(update: Update, context: ContextTypes.DEFAULT_TYPE, project_id: str) -> None:
    """Process the user message then answer."""
    message_text = update.message.text
    user_id = update.message.from_user["id"]

    response = process_with_dialogflow(
        text=message_text,
        session=user_id,
        project_id=project_id
    )
    replay_text = response.query_result.fulfillment_text
    await update.message.reply_text(replay_text)


def main() -> None:
    load_dotenv()
    google_aplication = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    bot_token = os.environ['TELEGRAM_TOKEN']
    project_id = get_project_id(google_aplication)

    run_tg_bot(bot_token, project_id)


if __name__ == "__main__":
    main()
