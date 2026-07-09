from abc import ABC, abstractmethod
import os
import smtplib
from src.text import create_text
from email.message import EmailMessage

class Notification(ABC):
    @abstractmethod
    def notify(self):
        pass # pragma: no cover

class EmailNotification(Notification):
    def notify(self):
        print("sending notification")
        message = self.build_message()
        try:
            email_sender = self.get_email_sender()
            email_password = self.get_email_password()
            with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as smtp:
                smtp.login(
                    email_sender,
                    email_password
                )
                smtp.send_message(message)
            print("notification succesfully sent")
        except Exception as e:
            print(f"failed to send notification. error: {e}")

    def build_message(self):
        message = EmailMessage()
        message["Subject"] = "Jogo hoje!!!"
        message["From"] = self.get_email_sender()
        message["To"] = self.get_email_receiver()
        text = create_text()
        message.set_content(text)
        return message
    
    def get_email_sender(self) -> str:
        email_sender = os.getenv("EMAIL_SENDER")
        if not email_sender:
            raise ValueError("EMAIL_SENDER was not found")
        return email_sender
    
    def get_email_password(self) -> str:
        email_password = os.getenv("EMAIL_PASSWORD")
        if not email_password:
            raise ValueError("EMAIL_PASSWORD was not found")
        return email_password
    
    def get_email_receiver(self) -> str:
        email_receiver = os.getenv("EMAIL_RECEIVER")
        if not email_receiver:
            raise ValueError("EMAIL_RECEIVER was not found")
        return email_receiver
