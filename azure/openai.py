import os
import requests
from auth.auth import get_token

OPENAI_MODEL = 'gpt-35-turbo-blue'
OPENAI_MODEL_4 = "gpt-4-32k-blue"


class Convo:
    def __init__(self, max_tokens: int, prompt: str):
        # Set the URL for the OpenAI API endpoint, including the deployment
        # model and API version
        self.url = (
            f'https://cog-sandbox-dev-eastus2-001.openai.azure.com/openai/dep'
            f'loyments/{OPENAI_MODEL}/chat/completions?api-version=2023-05-15'
        )

        # Set the headers
        self.headers = {
            'Authorization': 'Bearer ' + get_token(),
            'Content-Type': 'application/json'
        }

        self.prompt = get_prompt(prompt)

        # Set the initial data for the API request
        self.data = {
            "messages": [
                {
                    "role": "system",
                    "content": self.prompt
                    # Modify system message to change the assistant's behavior
                    # in the prompt.txt file
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "max_tokens": max_tokens,
            "stop": None
        }

    def send_message(self, user_message: str):
        # Append the user's message to the messages list
        self.data['messages'].append({
            "role": "user",
            "content": user_message
        })

        # Send a POST request to the API with the current data
        response = requests.post(
            self.url,
            headers=self.headers,
            json=self.data
        )

        # Check for errors in the response
        if response.status_code != 200:
            print(response.json())
            raise Exception("Error in response")

        # Extract the assistant's message from the response
        ai_message = response.json()["choices"][0]["message"]["content"]

        # Append the assistant's message to the messages list
        self.data['messages'].append({
            "role": "assistant",
            "content": ai_message
        })

        # Return the assistant's message
        return ai_message


def get_prompt(prompt: str):
    current_dir = os.path.dirname(__file__)

    with open(f'{current_dir}/{prompt}', 'r') as file:
        return file.read()
