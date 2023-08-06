from .first_type import TelegramType


class User(TelegramType):
    def __init__(self,
                 id,
                 is_bot,
                 first_name,
                 last_name=None,
                 username=None,
                 language_code=None,
                 can_join_groups=None,
                 can_read_all_group_messages=None,
                 supports_inline_queries=None):
        super().__init__(list(locals().items())[1:])


class Chat(TelegramType):
    def __init__(self,
                 id,
                 type,
                 title=None,
                 username=None,
                 first_name=None,
                 last_name=None,
                 photo=None,
                 bio=None,
                 has_private_forwards=None,
                 description=None,
                 invite_link=None,
                 pinned_message=None,
                 permissions=None,
                 slow_mode_delay=None,
                 message_auto_delete_time=None,
                 has_protected_content=None,
                 sticker_set_name=None,
                 can_set_sticker_set=None,
                 linked_chat_id=None,
                 location=None):
        super().__init__(list(locals().items())[1:])


class Message(TelegramType):
    def __init__(self,
                 message_id,
                 date,
                 chat,
                 from_=None,
                 sender_chat=None,
                 forward_from=None,
                 forward_from_chat=None,
                 forward_from_message_id=None,
                 forward_signature=None,
                 forward_sender_name=None,
                 forward_date=None,
                 is_automatic_forward=None,
                 reply_to_message=None,
                 via_bot=None,
                 edit_date=None,
                 has_protected_content=None,
                 media_group_id=None,
                 author_signature=None,
                 text=None,
                 entities=None,
                 animation=None,
                 audio=None,
                 document=None,
                 photo=None,
                 sticker=None,
                 video=None,
                 video_note=None,
                 voice=None,
                 caption=None,
                 caption_entities=None,
                 contact=None,
                 dice=None,
                 game=None,
                 poll=None,
                 venue=None,
                 location=None,
                 new_chat_members=None,
                 left_chat_member=None,
                 new_chat_title=None,
                 new_chat_photo=None,
                 delete_chat_photo=None,
                 group_chat_created=None,
                 supergroup_chat_created=None,
                 channel_chat_created=None,
                 message_auto_delete_timer_changed=None,
                 migrate_to_chat_id=None,
                 migrate_from_chat_id=None,
                 pinned_message=None,
                 invoice=None,
                 successful_payment=None,
                 connected_website=None,
                 passport_data=None,
                 proximity_alert_triggered=None,
                 voice_chat_scheduled=None,
                 voice_chat_started=None,
                 voice_chat_ended=None,
                 voice_chat_participants_invited=None,
                 reply_markup=None):
        super().__init__(list(locals().items())[1:])


class MessageId(TelegramType):
    def __init__(self,
                 message_id):
        super().__init__(list(locals().items())[1:])


class MessageEntity(TelegramType):
    def __init__(self,
                 type,
                 offset,
                 length,
                 url=None,
                 user=None,
                 language=None):
        super().__init__(list(locals().items())[1:])


class PhotoSize(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 width,
                 height,
                 file_size=None):
        super().__init__(list(locals().items())[1:])


class Animation(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 width,
                 height,
                 duration,
                 thumb=None,
                 file_name=None,
                 mime_type=None,
                 file_size=None):
        super().__init__(list(locals().items())[1:])


class Audio(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 duration,
                 performer=None,
                 title=None,
                 file_name=None,
                 mime_type=None,
                 file_size=None,
                 thumb=None):
        super().__init__(list(locals().items())[1:])


class Document(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 thumb=None,
                 file_name=None,
                 mime_type=None,
                 file_size=None):
        super().__init__(list(locals().items())[1:])


class Video(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 width,
                 height,
                 duration,
                 thumb=None,
                 file_name=None,
                 mime_type=None,
                 file_size=None):
        super().__init__(list(locals().items())[1:])


class VideoNote(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 length,
                 duration,
                 thumb=None,
                 file_size=None):
        super().__init__(list(locals().items())[1:])


class Voice(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 duration,
                 mime_type=None,
                 file_size=None):
        super().__init__(list(locals().items())[1:])


class Contact(TelegramType):
    def __init__(self,
                 phone_number,
                 first_name,
                 last_name=None,
                 user_id=None,
                 vcard=None):
        super().__init__(list(locals().items())[1:])


class Dice(TelegramType):
    def __init__(self,
                 emoji,
                 value):
        super().__init__(list(locals().items())[1:])


class PollOption(TelegramType):
    def __init__(self,
                 text,
                 voter_count):
        super().__init__(list(locals().items())[1:])


class PollAnswer(TelegramType):
    def __init__(self,
                 poll_id,
                 user,
                 option_ids):
        super().__init__(list(locals().items())[1:])


class Poll(TelegramType):
    def __init__(self,
                 id,
                 question,
                 options,
                 total_voter_count,
                 is_closed,
                 is_anonymous,
                 type,
                 allows_multiple_answers,
                 correct_option_id=None,
                 explanation=None,
                 explanation_entities=None,
                 open_period=None,
                 close_date=None):
        super().__init__(list(locals().items())[1:])


class Location(TelegramType):
    def __init__(self,
                 longitude,
                 latitude,
                 horizontal_accuracy=None,
                 live_period=None,
                 heading=None,
                 proximity_alert_radius=None):
        super().__init__(list(locals().items())[1:])


class Venue(TelegramType):
    def __init__(self,
                 location,
                 title,
                 address,
                 foursquare_id=None,
                 foursquare_type=None,
                 google_place_id=None,
                 google_place_type=None):
        super().__init__(list(locals().items())[1:])


class ProximityAlertTriggered(TelegramType):
    def __init__(self,
                 traveler,
                 watcher,
                 distance):
        super().__init__(list(locals().items())[1:])


class MessageAutoDeleteTimerChanged(TelegramType):
    def __init__(self,
                 message_auto_delete_time):
        super().__init__(list(locals().items())[1:])


class VoiceChatScheduled(TelegramType):
    def __init__(self,
                 start_date):
        super().__init__(list(locals().items())[1:])


class VoiceChatStarted(TelegramType):
    pass


class VoiceChatEnded(TelegramType):
    def __init__(self,
                 duration):
        super().__init__(list(locals().items())[1:])


class VoiceChatParticipantsInvited(TelegramType):
    def __init__(self,
                 users=None):
        super().__init__(list(locals().items())[1:])


class UserProfilePhotos(TelegramType):
    def __init__(self,
                 total_count,
                 photos):
        super().__init__(list(locals().items())[1:])


class File(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 file_size=None,
                 file_path=None):
        super().__init__(list(locals().items())[1:])


class ReplyKeyboardMarkup(TelegramType):
    def __init__(self,
                 keyboard,
                 resize_keyboard=None,
                 one_time_keyboard=None,
                 input_field_placeholder=None,
                 selective=None):
        super().__init__(list(locals().items())[1:])


class KeyboardButton(TelegramType):
    def __init__(self,
                 text,
                 request_contact=None,
                 request_location=None,
                 request_poll=None):
        super().__init__(list(locals().items())[1:])


class KeyboardButtonPollType(TelegramType):
    def __init__(self,
                 type=None):
        super().__init__(list(locals().items())[1:])


class ReplyKeyboardRemove(TelegramType):
    def __init__(self,
                 remove_keyboard,
                 selective=None):
        super().__init__(list(locals().items())[1:])


class InlineKeyboardMarkup(TelegramType):
    def __init__(self,
                 inline_keyboard):
        super().__init__(list(locals().items())[1:])


class InlineKeyboardButton(TelegramType):
    def __init__(self,
                 text,
                 url=None,
                 login_url=None,
                 callback_data=None,
                 switch_inline_query=None,
                 switch_inline_query_current_chat=None,
                 callback_game=None,
                 pay=None):
        super().__init__(list(locals().items())[1:])


class LoginUrl(TelegramType):
    def __init__(self,
                 url,
                 forward_text=None,
                 bot_username=None,
                 request_write_access=None):
        super().__init__(list(locals().items())[1:])


class CallbackQuery(TelegramType):
    def __init__(self,
                 id,
                 from_,
                 message=None,
                 inline_message_id=None,
                 chat_instance=None,
                 data=None,
                 game_short_name=None):
        super().__init__(list(locals().items())[1:])


class ForceReply(TelegramType):
    def __init__(self,
                 force_reply,
                 input_field_placeholder=None,
                 selective=None):
        super().__init__(list(locals().items())[1:])


class ChatPhoto(TelegramType):
    def __init__(self,
                 small_file_id,
                 small_file_unique_id,
                 big_file_id,
                 big_file_unique_id):
        super().__init__(list(locals().items())[1:])


class ChatInviteLink(TelegramType):
    def __init__(self,
                 invite_link,
                 creator,
                 creates_join_request,
                 is_primary,
                 is_revoked,
                 name=None,
                 expire_date=None,
                 member_limit=None,
                 pending_join_request_count=None):
        super().__init__(list(locals().items())[1:])


class ChatMember(TelegramType):
    pass


class ChatMemberOwner(TelegramType):
    def __init__(self,
                 status,
                 user,
                 is_anonymous,
                 custom_title=None):
        super().__init__(list(locals().items())[1:])


class ChatMemberAdministrator(TelegramType):
    def __init__(self,
                 status,
                 user,
                 can_be_edited,
                 is_anonymous,
                 can_manage_chat,
                 can_delete_messages,
                 can_manage_voice_chats,
                 can_restrict_members,
                 can_promote_members,
                 can_change_info,
                 can_invite_users,
                 can_post_messages=None,
                 can_edit_messages=None,
                 can_pin_messages=None,
                 custom_title=None):
        super().__init__(list(locals().items())[1:])


class ChatMemberMember(TelegramType):
    def __init__(self,
                 status,
                 user):
        super().__init__(list(locals().items())[1:])


class ChatMemberRestricted(TelegramType):
    def __init__(self,
                 status,
                 user,
                 is_member,
                 can_change_info,
                 can_invite_users,
                 can_pin_messages,
                 can_send_messages,
                 can_send_media_messages,
                 can_send_polls,
                 can_send_other_messages,
                 can_add_web_page_previews,
                 until_date):
        super().__init__(list(locals().items())[1:])


class ChatMemberLeft(TelegramType):
    def __init__(self,
                 status,
                 user):
        super().__init__(list(locals().items())[1:])


class ChatMemberBanned(TelegramType):
    def __init__(self,
                 status,
                 user,
                 until_date):
        super().__init__(list(locals().items())[1:])


class ChatMemberUpdated(TelegramType):
    def __init__(self,
                 chat,
                 from_,
                 date,
                 old_chat_member,
                 new_chat_member,
                 invite_link=None):
        super().__init__(list(locals().items())[1:])


class ChatJoinRequest(TelegramType):
    def __init__(self,
                 chat,
                 from_,
                 date,
                 bio=None,
                 invite_link=None):
        super().__init__(list(locals().items())[1:])


class ChatPermissions(TelegramType):
    def __init__(self,
                 can_send_messages=None,
                 can_send_media_messages=None,
                 can_send_polls=None,
                 can_send_other_messages=None,
                 can_add_web_page_previews=None,
                 can_change_info=None,
                 can_invite_users=None,
                 can_pin_messages=None):
        super().__init__(list(locals().items())[1:])


class ChatLocation(TelegramType):
    def __init__(self,
                 location,
                 address):
        super().__init__(list(locals().items())[1:])


class BotCommand(TelegramType):
    def __init__(self,
                 command,
                 description):
        super().__init__(list(locals().items())[1:])


class BotCommandScope(TelegramType):
    pass


class BotCommandScopeDefault(TelegramType):
    def __init__(self,
                 type):
        super().__init__(list(locals().items())[1:])


class BotCommandScopeAllPrivateChats(TelegramType):
    def __init__(self,
                 type):
        super().__init__(list(locals().items())[1:])


class BotCommandScopeAllGroupChats(TelegramType):
    def __init__(self,
                 type):
        super().__init__(list(locals().items())[1:])


class BotCommandScopeAllChatAdministrators(TelegramType):
    def __init__(self,
                 type):
        super().__init__(list(locals().items())[1:])


class BotCommandScopeChat(TelegramType):
    def __init__(self,
                 type,
                 chat_id):
        super().__init__(list(locals().items())[1:])


class BotCommandScopeChatAdministrators(TelegramType):
    def __init__(self,
                 type,
                 chat_id):
        super().__init__(list(locals().items())[1:])


class BotCommandScopeChatMember(TelegramType):
    def __init__(self,
                 type,
                 chat_id,
                 user_id):
        super().__init__(list(locals().items())[1:])


class ResponseParameters(TelegramType):
    def __init__(self,
                 migrate_to_chat_id=None,
                 retry_after=None):
        super().__init__(list(locals().items())[1:])


class InputMedia(TelegramType):
    pass


class InputMediaPhoto(TelegramType):
    def __init__(self,
                 type,
                 media,
                 caption=None,
                 parse_mode=None,
                 caption_entities=None):
        super().__init__(list(locals().items())[1:])


class InputMediaVideo(TelegramType):
    def __init__(self,
                 type,
                 media,
                 thumb=None,
                 caption=None,
                 parse_mode=None,
                 caption_entities=None,
                 width=None,
                 height=None,
                 duration=None,
                 supports_streaming=None):
        super().__init__(list(locals().items())[1:])


class InputMediaAnimation(TelegramType):
    def __init__(self,
                 type,
                 media,
                 thumb=None,
                 caption=None,
                 parse_mode=None,
                 caption_entities=None,
                 width=None,
                 height=None,
                 duration=None):
        super().__init__(list(locals().items())[1:])


class InputMediaAudio(TelegramType):
    def __init__(self,
                 type,
                 media,
                 thumb=None,
                 caption=None,
                 parse_mode=None,
                 caption_entities=None,
                 duration=None,
                 performer=None,
                 title=None):
        super().__init__(list(locals().items())[1:])


class InputMediaDocument(TelegramType):
    def __init__(self,
                 type,
                 media,
                 thumb=None,
                 caption=None,
                 parse_mode=None,
                 caption_entities=None,
                 disable_content_type_detection=None):
        super().__init__(list(locals().items())[1:])


class InputFile(TelegramType):
    pass


# Add this classes to convert_helper
class Sticker(TelegramType):
    def __init__(self,
                 file_id,
                 file_unique_id,
                 width,
                 height,
                 is_animated,
                 is_video,
                 thumb=None,
                 emoji=None,
                 set_name=None,
                 mask_position=None,
                 file_size=None):
        super().__init__(list(locals().items())[1:])


class StickerSet(TelegramType):
    def __init__(self,
                 name,
                 title,
                 is_animated,
                 is_video,
                 contains_masks,
                 stickers,
                 thumb=None):
        super().__init__(list(locals().items())[1:])


class MaskPosition(TelegramType):
    def __init__(self,
                 point,
                 x_shift,
                 y_shift,
                 scale):
        super().__init__(list(locals().items())[1:])


class LabeledPrice(TelegramType):
    def __init__(self,
                 label,
                 amount):
        super().__init__(list(locals().items())[1:])


class Invoice(TelegramType):
    def __init__(self,
                 title,
                 description,
                 start_parameter,
                 currency,
                 total_amount):
        super().__init__(list(locals().items())[1:])


class ShippingAddress(TelegramType):
    def __init__(self,
                 country_code,
                 state,
                 city,
                 street_line1,
                 street_line2,
                 post_code):
        super().__init__(list(locals().items())[1:])


class OrderInfo(TelegramType):
    def __init__(self,
                 name=None,
                 phone_number=None,
                 email=None,
                 shipping_address=None):
        super().__init__(list(locals().items())[1:])


class ShippingOption(TelegramType):
    def __init__(self,
                 id,
                 title,
                 prices):
        super().__init__(list(locals().items())[1:])


class SuccessfulPayment(TelegramType):
    def __init__(self,
                 currency,
                 total_amount,
                 invoice_payload,
                 telegram_payment_charge_id,
                 provider_payment_charge_id,
                 shipping_option_id=None,
                 order_info=None):
        super().__init__(list(locals().items())[1:])


class ShippingQuery(TelegramType):
    def __init__(self,
                 id,
                 from_,
                 invoice_payload,
                 shipping_address):
        super().__init__(list(locals().items())[1:])


class PreCheckoutQuery(TelegramType):
    def __init__(self,
                 id,
                 from_,
                 currency,
                 total_amount,
                 invoice_payload,
                 shipping_option_id=None,
                 order_info=None):
        super().__init__(list(locals().items())[1:])


class Game(TelegramType):
    def __init__(self,
                 title,
                 description,
                 photo,
                 text=None,
                 text_entities=None,
                 animation=None):
        super().__init__(list(locals().items())[1:])


class CallbackGame(TelegramType):
    pass


class GameHighScore(TelegramType):
    def __init__(self,
                 position,
                 user,
                 score):
        super().__init__(list(locals().items())[1:])


class PassportData(TelegramType):
    pass
