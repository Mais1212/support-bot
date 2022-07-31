import os

from dotenv import load_dotenv
from dialogflow import get_project_id

from tg_bot import run_bot


def main() -> None:
    load_dotenv()
    google_aplication = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    bot_token = os.environ['TELEGRAM_TOKEN']
    project_id = get_project_id(google_aplication)

    run_bot(bot_token, project_id)


if __name__ == "__main__":
    main()
