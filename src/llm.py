from abc import ABC, abstractmethod
import os
from pydantic import BaseModel
from openai import OpenAI

class GameModel(BaseModel):
    has_game_today: bool

class ValidatorBase(ABC):
    @abstractmethod
    def validate(self):
        pass # pragma: no cover

class Validator(ValidatorBase):
    def validate(self) -> GameModel:
        question = "Is Clube Atlético Mineiro going to play at Arena MRV today?"
        print(f"asking to llm: {question}")
        client = self.create_client()
        llm_response = client.responses.parse(
            model="gpt-5.4-mini",
            input=[
                {
                    "role": "user",
                    "content": question,
                },
            ],
            text_format=GameModel,
        )
        if not llm_response or not llm_response.output_parsed:
            raise ValueError("No value from LLM")
        print(llm_response.output_text)
        return llm_response.output_parsed

    def create_client(self) -> OpenAI:
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )