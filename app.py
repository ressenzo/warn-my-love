from dotenv import load_dotenv
from src import llm, notification

load_dotenv()
validator = llm.Validator()
email_notification = notification.EmailNotification()

def main():
    response = validator.validate()
    if response.has_game_today:
        email_notification.notify()
    else:
        print("there is no game today")

if __name__ == "__main__":
    print("starting application...")
    main()
    print("finishing application...")
