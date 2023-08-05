import requests
from wrapped_dict import wrdict


class Telegram:
    def __init__(self, token):
        self.token = token
        self.web = f"https://api.telegram.org/bot{token}/"

    def get_me(self):
        pass

    def send_message(self, chat_id, text):
        msg = {
            "chat_id": chat_id,
            "text": text
        }
        requests.post(self.web + "sendMessage", json=msg)

    def run(self, debug=False, handle_function=None):
        print("* Starting bot and waiting for updates")
        if debug:
            print("* Debug mod: ENABLED")
        else:
            print("* Debug mod: DISABLED")
        print()

        offset = 0
        while True:
            r = requests.post(self.web + f"getUpdates?offset={offset}").json()["result"]
            for x in r:
                if debug:
                    print(x["message"])
                handle_function(wrdict(x["message"]))
            if len(r) != 0:
                offset = r[-1]["update_id"] + 1
