import os
import smtplib
from src.text import create_text
from email.message import EmailMessage

def send_notification():
    print("sending notification")
    message = build_message()
    try:
        with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:
            smtp.login(
                os.getenv("EMAIL_SENDER"),
                os.getenv("EMAIL_PASSWORD")
            )
            smtp.send_message(message)
        print("notification succesfully sent")
    except Exception as e:
        print(f"failed to send notification. error: {e}")

def build_message():
    message = EmailMessage()
    message["Subject"] = "Jogo hoje!!!"
    message["From"] = os.getenv("EMAIL_SENDER")
    message["To"] = os.getenv("EMAIL_RECEIVER")
    text = create_text()
    message.set_content(text)
    return message
