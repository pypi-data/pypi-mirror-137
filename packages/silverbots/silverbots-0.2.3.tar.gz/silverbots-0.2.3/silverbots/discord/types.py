class BaseType:
    def __init__(self, scopes):
        for x in scopes:
            self.__setattr__(x[0], x[1])
        self._view = self.__dict__.copy()

    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{x[0]}={x[1]}" for x in self._view.items() if x[1] is not None]) + ")"


class User(BaseType):
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


class Chat(BaseType):
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


class Message(BaseType):
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

