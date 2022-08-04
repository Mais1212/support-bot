import logging
import os
import random
from urllib import response

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow import get_project_id, process_with_dialogflow

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)


def run_vk_bot(vk_token: str, project_id: str) -> None:
    """Start the bot."""
    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            _chat(event, vk, project_id)


def _chat(event: vk_api.longpoll.Event, vk: vk_api.vk_api.VkApiMethod, project_id: str) -> None:
    """Process the user message then answer."""
    response = process_with_dialogflow(
        session=event.user_id,
        project_id=project_id,
        text=event.text,
    )

    if response.query_result.intent.is_fallback:
        return

    message = response.query_result.fulfillment_text

    vk.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=random.randint(1, 1000)
    )


def main() -> None:
    load_dotenv()

    google_aplication = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    bot_token = os.environ['VK_TOKEN']
    project_id = get_project_id(google_aplication)

    run_vk_bot(bot_token, project_id)


if __name__ == "__main__":
    main()
