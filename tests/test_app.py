import os
from unittest.mock import patch, Mock
from app import GameModel, main, send_notification

@patch("app.send_notification")
@patch("app.call_llm")
def test_main_sends_notification(mock_call_llm, mock_send_notification):
    """Notification should be sent when has_game_today is true"""
    mock_call_llm.return_value = GameModel(has_game_today=True)

    main()

    mock_send_notification.assert_called_once()

@patch("app.send_notification")
@patch("app.call_llm")
def test_main_does_not_send_notification(mock_call_llm, mock_send_notification):
    """Notification should not be sent when has_game_today is false"""
    mock_call_llm.return_value = GameModel(has_game_today=False)

    main()

    mock_send_notification.assert_not_called()

@patch("app.create_text")
@patch("app.requests.post")
def test_send_notification(mock_post, mock_create_text):
    """Notification should be sent with properly parameters"""
    mock_create_text.return_value = "created text from mock"
    mock_post.return_value = Mock(status_code=204)

    with patch.dict(
        os.environ,
        {"DISCORD_WEBHOOK_URL": "https://example.com/webhook"},
    ): send_notification()

    mock_create_text.assert_called_once()
    mock_post.assert_called_once_with(
        url="https://example.com/webhook",
        json={"content": "created text from mock"},
    )
