import websocket
import json
import datetime
from ..make_request import make_request
from silverbots.discord.types import *


def convert_date(date):
    return int(datetime.datetime.strptime(date.split(".")[0], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp())


def convert_helper(req, to_class):
    if to_class == User:
        if "bot" in req:
            is_bot = req["bot"]
        else:
            is_bot = False
        return User(id=req["id"], is_bot=is_bot, first_name=req["username"])
    elif to_class == Chat:
        return Chat(id=req["channel_id"], type="channel")
    elif to_class == Message:
        return Message(message_id=req["id"], date=convert_date(req["timestamp"]), chat=Chat(id=req["channel_id"], type="channel"), from_=convert_helper(req["author"], User), text=req["content"])


class DiscordBot:
    def __init__(self,
                 token):
        self.token = token
        self.headers = {"Authorization": f"Bot {token}"}
        self.web = "https://discord.com/api/v9/"
        self.id = self.get_me().id
        self.handle_message_funcs = []

    def handle_message(self):
        def wrapped(wrp):
            self.handle_message_funcs.append(wrp)
        return wrapped

    def get_me(self) -> User:
        return convert_helper(make_request(self.web + "users/@me", headers=self.headers, method="GET").json(), User)

    def send_message(self, chat_id, text) -> Message:
        return convert_helper(make_request(self.web + f"channels/{chat_id}/messages", json={"content": text}, headers=self.headers, method="POST").json(), Message)

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
                                print(f"* New message: {convert_helper(rc['d'], Message)}")
                            for f in self.handle_message_funcs:
                                f(convert_helper(rc["d"], Message))
            except BaseException:
                ws = self._reconnect()
                continue
