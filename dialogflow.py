import argparse
import json
from dataclasses import dataclass

from environs import Env
from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types.session import DetectIntentResponse


@dataclass(frozen=True)
class Intent:
    """Intent model for dialogflow."""
    name: str
    training_phrases: list
    answers: list


def create_parser() -> argparse.ArgumentParser:
    """Create parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "json_name",
        type=str,
        help="Введите название файла."
    )
    return parser


def _fetch_and_create_intents(json_name: str, project_id: str) -> None:
    """Fetch intents from json and create them."""
    intents = _fetch_intents_from_json(json_name)
    for intent in intents:
        _create_intent(project_id, intent)


def _fetch_intents_from_json(json_name: str) -> list:
    "Load intents from json file."
    intents = []
    with open(json_name, "r", encoding="utf-8") as file:
        json_data = json.load(file)
    dict_keys = json_data.keys()

    for dict_key in dict_keys:

        answers = json_data[dict_key]["answer"]
        if type(answers) is str:
            answers = [answers]
        training_phrases = json_data[dict_key]["questions"]

        intent = Intent(
            name=dict_key,
            training_phrases=training_phrases,
            answers=answers
        )
        intents.append(intent)

    return intents


def _create_intent(project_id: str, intent: Intent) -> None:
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in intent.training_phrases:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=intent.answers)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=intent.name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def get_project_id(json_name: str) -> str:
    """Fetch project id from json file."""
    with open(json_name, "r") as file:
        json_data = json.load(file)
    project_id = json_data["project_id"]

    return project_id


def process_with_dialogflow(text: str, project_id: str, session: str) -> DetectIntentResponse:
    """Return processed text from dialogflow."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session)

    text_input = dialogflow.TextInput(text=text, language_code="ru")

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response


if __name__ == '__main__':
    env = Env()
    Env.read_env()
    parser = create_parser()
    namespace = parser.parse_args()
    google_aplication = env('GOOGLE_APPLICATION_CREDENTIALS')

    project_id = get_project_id(google_aplication)
    _fetch_and_create_intents(namespace.json_name, project_id)
