from dotenv import load_dotenv
from src import llm, notification

load_dotenv()

def main():
    # response = llm.ask_llm()
    # if response.has_game_today:
    notification.send_notification()
    # else:
    #     print("there is no game today")

if __name__ == "__main__":
    print("starting application...")
    main()
    print("finishing application...")
