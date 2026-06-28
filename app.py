from dotenv import load_dotenv
from llm import ask_llm
from notification import send_notification

load_dotenv()

def main():
    response = ask_llm()
    if response.has_game_today:
        send_notification()
    else:
        print("there is no game today")

if __name__ == "__main__":
    print("starting application...")
    main()
    print("finishing application...")
