from ..make_request import make_request


class DiscordBot:
    def __init__(self,
                 token):
        self.token = token
        self.headers = {"Authorization": f"Bot {token}"}
        self.web = "https://discord.com/api/v9/"

    def get_me(self):
        return make_request(self.web + f"users/@me", headers=self.headers, method="GET").json()

    def send_message(self, chat_id, text):
        return make_request(self.web + f"channels/{chat_id}/messages", json={"content": text}, headers=self.headers, method="POST").json()
