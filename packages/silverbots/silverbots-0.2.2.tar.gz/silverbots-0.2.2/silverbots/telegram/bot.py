from ..make_request import make_request
from silverbots.telegram.types import *


def get_json(lc):
    del lc["self"]
    ans = []
    for x in lc:
        if lc[x] is None:
            ans.append(x)
    for x in ans:
        del lc[x]
    return lc


def convert_helper(req, to_class):
    p, d, h = {}, {}, {}
    if to_class == Chat:
        p = {
            "photo": ChatPhoto,
            "pinned_message": Message,
            "permissions": ChatPermissions,
            "location": ChatLocation
        }
    elif to_class == Message:
        p = {
            "from": User,
            "sender_chat": Chat,
            "chat": Chat,
            "forward_from": User,
            "forward_from_chat": Chat,
            "reply_to_message": Message,
            "via_bot": User,
            "animation": Animation,
            "audio": Audio,
            "document": Document,
            "sticker": Sticker,
            "video": Video,
            "voice": Voice,
            "contact": Contact,
            "dice": Dice,
            "game": Game,
            "poll": Poll,
            "venue": Venue,
            "location": Location,
            "left_chat_member": User,
            "message_auto_delete_timer_changed": MessageAutoDeleteTimerChanged,
            "pinned_message": Message,
            "invoice": Invoice,
            "successful_payment": SuccessfulPayment,
            "passport_data": PassportData,
            "proximity_alert_triggered": ProximityAlertTriggered,
            "voice_chat_scheduled": VoiceChatScheduled,
            "voice_chat_started": VoiceChatStarted,
            "voice_chat_ended": VoiceChatEnded,
            "voice_chat_participants_invited": VoiceChatParticipantsInvited,
            "reply_markup": InlineKeyboardMarkup
        }
        d = {
            "entities": MessageEntity,
            "photo": PhotoSize,
            "caption_entities": MessageEntity,
            "new_chat_members": User,
            "new_chat_photo": PhotoSize
        }
    elif to_class == MessageEntity:
        p = {
            "user": User
        }
    elif to_class == Animation:
        p = {
            "thumb": PhotoSize
        }
    elif to_class == Audio:
        p = {
            "thumb": PhotoSize
        }
    elif to_class == Document:
        p = {
            "thumb": PhotoSize
        }
    elif to_class == Video:
        p = {
            "thumb": PhotoSize
        }
    elif to_class == VideoNote:
        p = {
            "thumb": PhotoSize
        }
    elif to_class == PollAnswer:
        p = {
            "user": User
        }
    elif to_class == Poll:
        d = {
            "options": PollOption,
            "explanation_entities": MessageEntity
        }
    elif to_class == Venue:
        p = {
            "location": Location
        }
    elif to_class == ProximityAlertTriggered:
        p = {
            "traveler": User,
            "watcher": User
        }
    elif to_class == VoiceChatParticipantsInvited:
        d = {
            "users": User
        }
    elif to_class == KeyboardButton:
        p = {
            "request_poll": KeyboardButtonPollType
        }
    elif to_class == InlineKeyboardButton:
        p = {
            "login_url": LoginUrl,
            "callback_game": CallbackGame
        }
    elif to_class == CallbackQuery:
        p = {
            "from": User,
            "message": Message
        }
    elif to_class == ChatInviteLink:
        p = {
            "creator": User
        }
    elif to_class == ChatMemberOwner:
        p = {
            "user": User
        }
    elif to_class == ChatMemberAdministrator:
        p = {
            "user": User
        }
    elif to_class == ChatMemberMember:
        p = {
            "user": User
        }
    elif to_class == ChatMemberRestricted:
        p = {
            "user": User
        }
    elif to_class == ChatMemberLeft:
        p = {
            "user": User
        }
    elif to_class == ChatMemberBanned:
        p = {
            "user": User
        }
    elif to_class == ChatMemberUpdated:
        p = {
            "chat": Chat,
            "from": User,
            "old_chat_member": ChatMember,
            "new_chat_member": ChatMember,
            "invite_link": ChatInviteLink
        }
    elif to_class == ChatJoinRequest:
        p = {
            "chat": Chat,
            "from": User,
            "invite_link": ChatInviteLink
        }
    elif to_class == ChatLocation:
        p = {
            "location": Location
        }
    elif to_class == InputMediaPhoto:
        d = {
            "caption_entities": MessageEntity
        }
    elif to_class == InputMediaVideo:
        d = {
            "caption_entities": MessageEntity
        }
        h = {
            "thumb": InputFile
        }
    elif to_class == InputMediaAnimation:
        d = {
            "caption_entities": MessageEntity
        }
        h = {
            "thumb": InputFile
        }
    elif to_class == InputMediaAudio:
        d = {
            "caption_entities": MessageEntity
        }
        h = {
            "thumb": InputFile
        }
    elif to_class == InputMediaDocument:
        d = {
            "caption_entities": MessageEntity
        }
        h = {
            "thumb": InputFile
        }
    elif to_class == UserProfilePhotos:
        h = {
            "photos": PhotoSize
        }
    elif to_class == ReplyKeyboardMarkup:
        h = {
            "keyboard": KeyboardButton
        }
    elif to_class == InlineKeyboardMarkup:
        h = {
            "inline_keyboard": InlineKeyboardButton
        }
    for x in p:
        if x in req:
            req[x] = convert_helper(req[x], p[x])
    for x in d:
        if x in req:
            ans = []
            for y in req[x]:
                ans.append(convert_helper(y, d[x]))
            req[x] = ans
    for x in h:
        if x in req:
            ans = []
            for y in req[x]:
                row = []
                for z in y:
                    row.append(convert_helper(z, h[x]))
                ans.append(row)
            req[x] = ans
    if "from" in req:
        req["from_"] = req["from"]
        del req["from"]
    return to_class(**req)


class TelegramBot:
    def __init__(self,
                 token):
        self.token = token
        self.web = f"https://api.telegram.org/bot{token}/"
        self.handle_message_funcs = []
        self.handle_poll_answer_funcs = []

    def handle_message(self):
        def wrapped(wrp):
            self.handle_message_funcs.append(wrp)
        return wrapped

    def handle_poll_answer(self):
        def wrapped(wrp):
            self.handle_poll_answer_funcs.append(wrp)
        return wrapped

    def get_me(self) -> User:
        r = make_request(self.web + "getMe", method="POST")
        return convert_helper(list(r.json().values())[1], User)

    def send_message(self,
                     chat_id,
                     text,
                     parse_mode=None,
                     entities=None,
                     disable_web_page_preview=None,
                     disable_notification=None,
                     protect_content=None,
                     reply_to_message_id=None,
                     allow_sending_without_reply=None,
                     reply_markup=None,
                     timeout=None) -> Message:
        r = make_request(self.web + "sendMessage", json=get_json(locals()), method="POST")
        return convert_helper(list(r.json().values())[1], Message)

    def send_poll(self,
                  chat_id,
                  question,
                  options,
                  is_anonymous=None,
                  type=None,
                  allows_multiple_answers=None,
                  correct_option_id=None,
                  explanation=None,
                  explanation_parse_mode=None,
                  explanation_entities=None,
                  open_period=None,
                  close_date=None,
                  is_closed=None,
                  disable_notification=None,
                  protect_content=None,
                  reply_to_message_id=None,
                  allow_sending_without_reply=None,
                  reply_markup=None):
        r = make_request(self.web + "sendPoll", json=get_json(locals()), method="POST")
        return convert_helper(list(r.json().values())[1], Message)

    def run(self, debug=False):
        print("* Starting bot and waiting for updates: TELEGRAM")
        if debug:
            print("* Debug mod: ENABLED")
        else:
            print("* Debug mod: DISABLED")

        offset = 0
        while True:
            r = make_request(self.web + f"getUpdates?offset={offset}", method="POST").json()["result"]
            for x in r:
                if "message" in x and len(self.handle_message_funcs) != 0:
                    message = convert_helper(x["message"], Message)
                    if debug:
                        print("* New message: " + str(message))
                    for f in self.handle_message_funcs:
                        f(message)
                if "poll_answer" in x and len(self.handle_poll_answer_funcs) != 0:
                    poll = convert_helper(x["poll_answer"], PollAnswer)
                    if debug:
                        print("* New answer on poll: " + str(poll))
                    for f in self.handle_poll_answer_funcs:
                        f(poll)
            if len(r) != 0:
                offset = r[-1]["update_id"] + 1
