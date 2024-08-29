from google.cloud import dialogflow_v2beta1 as dialogflow

def run_sample():
#projects/udemychatbox/locations/us-central1/agents/508132a4-f095-4aa5-a701-ff2dcd567723
    project_id = "udemychatbox"
    # For more information about regionalization see https://cloud.google.com/dialogflow/cx/docs/how/region
    location_id = "us-central1"
    # For more info on agents see https://cloud.google.com/dialogflow/cx/docs/concept/agent
    agent_id = "508132a4-f095-4aa5-a701-ff2dcd567723"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    # For more information on sessions see https://cloud.google.com/dialogflow/cx/docs/concept/session
    session_id = "fdc68e-e68-e88-bb4-07e6a27a3"
    texts = ["Hello"]
    # For more supported languages see https://cloud.google.com/dialogflow/es/docs/reference/language
    language_code = "en-us"

    detect_intent_texts(agent, session_id, texts, language_code)
    #detect_intent_texts(agent, texts, language_code)


def detect_intent_texts(agent, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")
    client_options = None
    #agent_components = dialogflow.AgentsClient.parse_agent_path(agent)
    # agent_components = dialogflow.AgentsClient.parse_agent_path(agent)
    # location_id = agent_components["location"]
    # if location_id != "global":
    #     api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
    #     print(f"API Endpoint: {api_endpoint}\n")
    #     client_options = {"api_endpoint": api_endpoint}
    session_client = dialogflow.SessionsClient(client_options=client_options)

    for text in texts:
        text_input = dialogflow.TextInput(text=text)
        query_input = dialogflow.QueryInput(text=text_input)
        request = dialogflow.DetectIntentRequest(
            session=session_path, query_input=query_input
        )
        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")


if __name__ == '__main__':
    # app.run(port=5000)
    run_sample()
