import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def get_project_id(file_name: str) -> str:
    """ Fetch project id from json file. """
    with open(file_name) as file:
        json_data = json.load(file)
    project_id = json_data["project_id"]

    return project_id


def process_with_dialogflow(text: str, project_id: str, session: str) -> str:
    """Return processed text from dialogflow."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session)

    text_input = dialogflow.TextInput(text=text, language_code="ru")

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    fulfillment_text = response.query_result.fulfillment_text

    return fulfillment_text
