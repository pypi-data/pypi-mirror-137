from ..make_request import make_request
import websocket
import json


class DiscordBot:
    def __init__(self,
                 token):
        self.token = token
        self.headers = {"Authorization": f"Bot {token}"}
        self.web = "https://discord.com/api/v9/"
        self.id = self.get_me()["id"]
        self.handle_message_funcs = []

    def handle_message(self):
        def wrapped(wrp):
            self.handle_message_funcs.append(wrp)
        return wrapped

    def get_me(self):
        return make_request(self.web + "users/@me", headers=self.headers, method="GET").json()

    def send_message(self, chat_id, text):
        return make_request(self.web + f"channels/{chat_id}/messages", json={"content": text}, headers=self.headers, method="POST").json()

    def _reconnect(self):
        r = make_request(self.web + "gateway", method="GET")
        ws = websocket.create_connection(f"{r.json()['url']}/?v=9&encoding=json")
        js = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": 513,
                "properties": {
                    "$os": "windows",
                    "$browser": "opera",
                    "$device": "laptop"
                }
            }
        }
        ws.send(json.dumps(js))
        return ws

    def run(self, debug=False):
        print("* Starting bot and waiting for updates: DISCORD")
        if debug:
            print("* Debug mod: ENABLED")
        else:
            print("* Debug mod: DISABLED")

        ws = self._reconnect()
        while True:
            try:
                rc = json.loads(str(ws.recv()))
                if rc != "":
                    if rc["t"] == "MESSAGE_CREATE":
                        if rc["d"]["author"]["id"] != self.id:
                            if debug:
                                print(f"* New message: {json.dumps(rc['d'])}")
                            for f in self.handle_message_funcs:
                                f(rc["d"])
            except websocket._exceptions.WebSocketConnectionClosedException:
                ws = self._reconnect()
            except json.decoder.JSONDecodeError:
                continue
