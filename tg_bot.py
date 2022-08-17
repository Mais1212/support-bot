import logging
from functools import partial

from dotenv import load_dotenv
from environs import Env
from telegram import ForceReply, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow import get_project_id, process_with_dialogflow
from logging_bot import TgLoggerHandler

load_dotenv()
logger = logging.getLogger(__file__)


def run_tg_bot(bot_token: str, project_id: str) -> None:
    """Start the bot."""
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", _start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, partial(_chat, project_id=project_id)
    ))
    updater.start_polling()
    updater.idle()


def _start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_html(
        f"Здравствуйте.",
        reply_markup=ForceReply(selective=True),
    )


def _chat(update: Update, context: CallbackContext, project_id: str) -> None:
    """Process the user message then answer."""
    try:
        message_text = update.message.text
        user_id = update.message.from_user["id"]

        response = process_with_dialogflow(
            text=message_text,
            session=user_id,
            project_id=project_id
        )

        replay_text = response.query_result.fulfillment_text
    except Exception as error:
        logger.error(error)
        return

    update.message.reply_text(replay_text)


def main() -> None:
    env = Env()
    Env.read_env()
    google_aplication = env('GOOGLE_APPLICATION_CREDENTIALS')
    bot_token = env('TELEGRAM_TOKEN')
    telegram_debug_token = env('TELEGRAM_DEBUG_TOKEN')
    admin_telegram_chat_id = env('ADMIN_TG_CHAT_ID')
    project_id = get_project_id(google_aplication)

    logger.setLevel(logging.WARNING)
    logger.addHandler(
        TgLoggerHandler(
            token=telegram_debug_token,
            chat_id=admin_telegram_chat_id
        )
    )

    run_tg_bot(bot_token, project_id)


if __name__ == "__main__":
    main()
