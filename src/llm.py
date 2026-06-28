import os
from pydantic import BaseModel
from openai import OpenAI

class GameModel(BaseModel):
    has_game_today: bool

def ask_llm() -> GameModel:
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