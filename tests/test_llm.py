from unittest.mock import MagicMock, patch

import pytest
from src.llm import Validator, GameModel

@patch("src.llm.Validator.create_client")
def test_validate_returns_game_model(mock_create_client):
    # Arrange
    fake_response = MagicMock()
    fake_response.output_parsed = GameModel(has_game_today=True)
    fake_client = MagicMock()
    fake_client.responses.parse.return_value = fake_response
    mock_create_client.return_value = fake_client

    # Act
    checker = Validator()
    result = checker.validate()

    # Assert
    assert result.has_game_today is True
    fake_client.responses.parse.assert_called_once_with(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "user",
                "content": "Is Clube Atlético Mineiro going to play at Arena MRV today?",
            },
        ],
        text_format=GameModel,
    )

@patch("src.llm.Validator.create_client")
def test_validate_llm_returns_None(mock_create_client):
    # Arrange
    fake_response = MagicMock()
    fake_response.output_parsed = None
    fake_client = MagicMock()
    fake_client.responses.parse.return_value = fake_response
    mock_create_client.return_value = fake_client

    # Act - Assert
    checker = Validator()
    with pytest.raises(ValueError, match="No value from LLM"):
        checker.validate()

@patch("src.llm.OpenAI")
@patch("src.llm.os.getenv")
def test_create_client(mock_getenv, mock_openai):
    # Arrange
    mock_getenv.return_value = "fake-api-key"

    # Act
    checker = Validator()
    checker.create_client()

    # Assert
    mock_getenv.assert_called_once_with("OPENAI_API_KEY")
    mock_openai.assert_called_once_with(api_key="fake-api-key")
