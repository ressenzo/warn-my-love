from unittest.mock import MagicMock, Mock, patch
from src.notification import send_notification, build_message

@patch("src.notification.build_message")
@patch("src.notification.os.getenv")
@patch("src.notification.smtplib.SMTP_SSL")
def test_send_notification(mock_smtp, mock_getenv, mock_build_message):
    # Arrange
    mock_getenv.side_effect = lambda key: {
        "EMAIL_SENDER": "sender@email.com",
        "EMAIL_RECEIVER": "receiver@email.com",
        "EMAIL_PASSWORD": "password123",
    }[key]
    fake_message = MagicMock()
    mock_build_message.return_value = fake_message
    smtp = MagicMock()
    mock_smtp.return_value.__enter__.return_value = smtp
    
    # Act
    send_notification()

    # Assert
    mock_build_message.assert_called_once()
    smtp.login.assert_called_once_with(
        "sender@email.com",
        "password123"
    )
    smtp.send_message.assert_called_once_with(fake_message)

@patch("src.notification.create_text")
@patch("src.notification.os.getenv")
def test_build_message(mock_getenv, mock_create_text):
    # Arrange
    mock_getenv.side_effect = lambda key: {
        "EMAIL_SENDER": "sender@email.com",
        "EMAIL_RECEIVER": "receiver@email.com",
        "EMAIL_PASSWORD": "password123",
    }[key]
    mock_create_text.return_value = "Game today"

    # Act
    message = build_message()

    # Assert
    assert message["Subject"] == "Jogo hoje!!!"
    assert message["From"] == "sender@email.com"
    assert message["To"] == "receiver@email.com"
    assert "Game today" in message.get_content()


@patch("builtins.print")
@patch("src.notification.smtplib.SMTP_SSL")
def test_send_notification_prints_error(mock_smtp, mock_print):
    # Arrange
    mock_smtp.side_effect = Exception("SMTP failed")

    # Act
    send_notification()

    # Assert
    mock_print.assert_any_call(
        "failed to send notification. error: SMTP failed"
    )