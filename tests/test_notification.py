from unittest.mock import MagicMock, patch

import pytest
from src.notification import EmailNotification

@patch("src.notification.EmailNotification.build_message")
@patch("src.notification.os.getenv")
@patch("src.notification.smtplib.SMTP_SSL")
def test_notify(mock_smtp, mock_getenv, mock_build_message):
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
    email_notification = EmailNotification()
    email_notification.notify()

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
    email_notification = EmailNotification()
    message = email_notification.build_message()

    # Assert
    assert message["Subject"] == "Jogo hoje!!!"
    assert message["From"] == "sender@email.com"
    assert message["To"] == "receiver@email.com"
    assert "Game today" in message.get_content()


@patch("builtins.print")
@patch("src.notification.smtplib.SMTP_SSL")
def test_notify_prints_error(mock_smtp, mock_print):
    # Arrange
    mock_smtp.side_effect = Exception("SMTP failed")

    # Act
    email_notification = EmailNotification()
    email_notification.notify()

    # Assert
    mock_print.assert_any_call(
        "failed to send notification. error: SMTP failed"
    )

@patch("src.notification.os.getenv")
def test_get_email_sender(mock_getenv):
    # Arrange
    mock_getenv.side_effect = lambda key: {
        "EMAIL_SENDER": ""
    }[key]

    # Act - Assert
    with pytest.raises(ValueError, match="EMAIL_SENDER was not found"):
        email_notification = EmailNotification()
        email_notification.get_email_sender()

@patch("src.notification.os.getenv")
def test_get_email_password(mock_getenv):
    # Arrange
    mock_getenv.side_effect = lambda key: {
        "EMAIL_PASSWORD": ""
    }[key]

    # Act - Assert
    with pytest.raises(ValueError, match="EMAIL_PASSWORD was not found"):
        email_notification = EmailNotification()
        email_notification.get_email_password()
