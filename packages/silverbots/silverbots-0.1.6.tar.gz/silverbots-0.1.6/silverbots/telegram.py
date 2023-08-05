import requests
from .wrapped_dict import wrdict


class Telegram:
    def __init__(self, token):
        self.token = token
        self.web = f"https://api.telegram.org/bot{token}/"
        self.handle_message_funcs = []

    def handle_message(self):
        def wrapped(wrp):
            self.handle_message_funcs.append(wrp)
        return wrapped

    def get_me(self):
        return wrdict(requests.post(self.web + "getMe").json())

    def log_out(self):
        pass

    def close(self):
        pass

    def send_message(self, chat_id, text):
        msg = {
            "chat_id": chat_id,
            "text": text
        }
        requests.post(self.web + "sendMessage", json=msg)

    def run(self, debug=False):
        print("* Starting bot and waiting for updates")
        if debug:
            print("* Debug mod: ENABLED")
        else:
            print("* Debug mod: DISABLED")

        offset = 0
        while True:
            r = requests.post(self.web + f"getUpdates?offset={offset}").json()["result"]
            for x in r:
                if debug:
                    print(x["message"])
                for m in self.handle_message_funcs:
                    m(wrdict(x["message"]))
            if len(r) != 0:
                offset = r[-1]["update_id"] + 1
