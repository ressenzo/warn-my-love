import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from text import create_text

class GameModel(BaseModel):
    has_game_today: bool

load_dotenv()

def main():
    response = call_llm()
    if response.has_game_today:
        send_notification()
    else:
        print("there is no game today")

def call_llm() -> GameModel:
    print("asking to llm")
    client = create_client()
    llm_response = client.responses.parse(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": "Is Clube Atlético Mineiro going to play at Arena MRV today?",
            },
        ],
        text_format=GameModel,
    )
    print(llm_response.output_text)
    return llm_response.output_parsed

def create_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

def send_notification():
    print("sending notification")
    url = os.getenv("DISCORD_WEBHOOK_URL")
    text = create_text()
    payload = {
        "content": text
    }
    response = requests.post(
        url=url,
        json=payload,
        timeout=5
    )
    print(f"notification result: {response.status_code == 204}")

if __name__ == "__main__":
    main()
