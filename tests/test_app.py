from unittest.mock import patch
from app import main
from llm import GameModel

@patch("app.send_notification")
@patch("app.ask_llm")
def test_main_sends_notification(mock_ask_llm, mock_send_notification):
    # Arrange
    mock_ask_llm.return_value = GameModel(has_game_today=True)

    # Act
    main()

    # Assert
    mock_send_notification.assert_called_once()

@patch("app.send_notification")
@patch("app.ask_llm")
def test_main_does_not_send_notification(mock_ask_llm, mock_send_notification):
    # Arrange
    mock_ask_llm.return_value = GameModel(has_game_today=False)

    # Act
    main()

    # Assert
    mock_send_notification.assert_not_called()
