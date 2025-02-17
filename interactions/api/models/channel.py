from datetime import datetime, timedelta, timezone
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

from ..error import LibraryException
from .attrs_utils import (
    MISSING,
    ClientSerializerMixin,
    DictSerializerMixin,
    convert_list,
    define,
    field,
)
from .misc import File, IDMixin, Overwrite, Snowflake
from .user import User
from .webhook import Webhook

if TYPE_CHECKING:
    from ...client.models.component import ActionRow, Button, SelectMenu
    from .guild import Invite, InviteTargetType
    from .member import Member
    from .message import Attachment, Embed, Message, MessageInteraction, Sticker

__all__ = (
    "ChannelType",
    "Thread",
    "Channel",
    "ThreadMember",
    "ThreadMetadata",
)


class ChannelType(IntEnum):
    """An enumerable object representing the type of channels."""

    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_FORUM = 15


@define()
class ThreadMetadata(DictSerializerMixin):
    """
    A class object representing the metadata of a thread.

    .. note::
        ``invitable`` will only show if the thread can have an invited created with the
        current cached permissions.

    :ivar bool archived: The current thread accessibility state.
    :ivar int auto_archive_duration: The auto-archive time.
    :ivar datetime archive_timestamp: The timestamp that the thread will be/has been closed at.
    :ivar bool locked: The current message state of the thread.
    :ivar Optional[bool] invitable?: The ability to invite users to the thread.
    """

    archived: bool = field()
    auto_archive_duration: int = field()
    archive_timestamp: datetime.timestamp = field(converter=datetime.fromisoformat)
    locked: bool = field()
    invitable: Optional[bool] = field(default=None)


@define()
class ThreadMember(ClientSerializerMixin):
    """
    A class object representing a member in a thread.

    .. note::
        ``id`` only shows if there are active intents involved with the member
        in the thread.

    :ivar Optional[Snowflake] id?: The "ID" or intents of the member.
    :ivar Snowflake user_id: The user ID of the member.
    :ivar datetime join_timestamp: The timestamp of when the member joined the thread.
    :ivar int flags: The bitshift flags for the member in the thread.
    :ivar bool muted: Whether the member is muted or not.
    """

    id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    user_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    join_timestamp: datetime.timestamp = field(converter=datetime.fromisoformat)
    flags: int = field()
    muted: bool = field()
    mute_config: Optional[Any] = field(default=None)  # todo explore this, it isn't in the ddev docs


@define()
class Channel(ClientSerializerMixin, IDMixin):
    """
    A class object representing all types of channels.

    .. note::
        The purpose of this model is to be used as a base class, and
        is never needed to be used directly.

    :ivar Snowflake id: The (snowflake) ID of the channel.
    :ivar ChannelType type: The type of channel.
    :ivar Optional[Snowflake] guild_id?: The ID of the guild if it is not a DM channel.
    :ivar Optional[int] position?: The position of the channel.
    :ivar List[Overwrite] permission_overwrites: The non-synced permissions of the channel.
    :ivar str name: The name of the channel.
    :ivar Optional[str] topic?: The description of the channel.
    :ivar Optional[bool] nsfw?: Whether the channel is NSFW.
    :ivar Snowflake last_message_id: The ID of the last message sent.
    :ivar Optional[int] bitrate?: The audio bitrate of the channel.
    :ivar Optional[int] user_limit?: The maximum amount of users allowed in the channel.
    :ivar Optional[int] rate_limit_per_user?: The concurrent ratelimit for users in the channel.
    :ivar Optional[List[User]] recipients?: The recipients of the channel.
    :ivar Optional[str] icon?: The icon of the channel.
    :ivar Optional[Snowflake] owner_id?: The owner of the channel.
    :ivar Optional[Snowflake] application_id?: The application of the channel.
    :ivar Optional[Snowflake] parent_id?: The ID of the "parent"/main channel.
    :ivar Optional[datetime] last_pin_timestamp?: The timestamp of the last pinned message in the channel.
    :ivar Optional[str] rtc_region?: The region of the WebRTC connection for the channel.
    :ivar Optional[int] video_quality_mode?: The set quality mode for video streaming in the channel.
    :ivar int message_count: The amount of messages in the channel.
    :ivar Optional[int] member_count?: The amount of members in the channel.
    :ivar Optional[ThreadMetadata] thread_metadata?: The thread metadata of the channel.
    :ivar Optional[ThreadMember] member?: The member of the thread in the channel.
    :ivar Optional[int] default_auto_archive_duration?: The set auto-archive time for all threads to naturally follow in the channel.
    :ivar Optional[str] permissions?: The permissions of the channel.
    :ivar Optional[int] flags?: The flags of the channel.
    :ivar Optional[int] total_message_sent?: Number of messages ever sent in a thread.
    """

    __slots__ = (
        # TODO: Document banner when Discord officially documents them.
        "banner",
        "guild_hashes",
    )

    type: ChannelType = field(converter=ChannelType)
    id: Snowflake = field(converter=Snowflake)
    guild_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    position: Optional[int] = field(default=None)
    permission_overwrites: Optional[List[Overwrite]] = field(
        converter=convert_list(Overwrite), factory=list
    )
    name: str = field(factory=str)
    topic: Optional[str] = field(default=None)
    nsfw: Optional[bool] = field(default=None)
    last_message_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    bitrate: Optional[int] = field(default=None)
    user_limit: Optional[int] = field(default=None)
    rate_limit_per_user: Optional[int] = field(default=None)
    recipients: Optional[List[User]] = field(converter=convert_list(User), default=None)
    icon: Optional[str] = field(default=None)
    owner_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    application_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    parent_id: Optional[Snowflake] = field(converter=Snowflake, default=None)
    last_pin_timestamp: Optional[datetime] = field(converter=datetime.fromisoformat, default=None)
    rtc_region: Optional[str] = field(default=None)
    video_quality_mode: Optional[int] = field(default=None)
    message_count: Optional[int] = field(default=None)
    member_count: Optional[int] = field(default=None)
    thread_metadata: Optional[ThreadMetadata] = field(converter=ThreadMetadata, default=None)
    member: Optional[ThreadMember] = field(converter=ThreadMember, default=None, add_client=True)
    default_auto_archive_duration: Optional[int] = field(default=None)
    permissions: Optional[str] = field(default=None)
    flags: Optional[int] = field(default=None)
    total_message_sent: Optional[int] = field(default=None)

    def __attrs_post_init__(self):  # sourcery skip: last-if-guard
        if self._client:
            if channel := self._client.cache[Channel].get(self.id):
                if not self.recipients:
                    self.recipients = channel.recipients

    def __repr__(self) -> str:
        return self.name

    @property
    def mention(self) -> str:
        """
        Returns a string that allows you to mention the given channel.

        :return: The string of the mentioned channel.
        :rtype: str
        """
        return f"<#{self.id}>"

    async def send(
        self,
        content: Optional[str] = MISSING,
        *,
        tts: Optional[bool] = MISSING,
        attachments: Optional[List["Attachment"]] = MISSING,
        files: Optional[Union[File, List[File]]] = MISSING,
        embeds: Optional[Union["Embed", List["Embed"]]] = MISSING,
        allowed_mentions: Optional["MessageInteraction"] = MISSING,
        stickers: Optional[List["Sticker"]] = MISSING,
        components: Optional[
            Union[
                "ActionRow",
                "Button",
                "SelectMenu",
                List["ActionRow"],
                List["Button"],
                List["SelectMenu"],
            ]
        ] = MISSING,
    ) -> "Message":  # noqa  # sourcery skip: dict-assign-update-to-union
        """
        Sends a message in the channel.

        :param content?: The contents of the message as a string or string-converted value.
        :type content?: Optional[str]
        :param tts?: Whether the message utilizes the text-to-speech Discord programme or not.
        :type tts?: Optional[bool]
        :param files?: A file or list of files to be attached to the message.
        :type files?: Optional[Union[File, List[File]]]
        :param attachments?: The attachments to attach to the message. Needs to be uploaded to the CDN first
        :type attachments?: Optional[List[Attachment]]
        :param embeds?: An embed, or list of embeds for the message.
        :type embeds?: Optional[Union[Embed, List[Embed]]]
        :param allowed_mentions?: The message interactions/mention limits that the message can refer to.
        :type allowed_mentions?: Optional[MessageInteraction]
        :param stickers?: A list of stickers to send with your message. You can send up to 3 stickers per message.
        :type stickers?: Optional[List[Sticker]]
        :param components?: A component, or list of components for the message.
        :type components?: Optional[Union[ActionRow, Button, SelectMenu, List[Actionrow], List[Button], List[SelectMenu]]]
        :return: The sent message as an object.
        :rtype: Message
        """
        if not self._client:
            raise LibraryException(code=13)
        from ...client.models.component import _build_components
        from .message import Message

        _content: str = "" if content is MISSING else content
        _tts: bool = False if tts is MISSING else tts
        _attachments = [] if attachments is MISSING else [a._json for a in attachments]
        _allowed_mentions: dict = {} if allowed_mentions is MISSING else allowed_mentions
        _sticker_ids: list = (
            [] if stickers is MISSING else [str(sticker.id) for sticker in stickers]
        )
        if not embeds or embeds is MISSING:
            _embeds: list = []
        elif isinstance(embeds, list):
            _embeds = [embed._json for embed in embeds]
        else:
            _embeds = [embeds._json]

        if not components or components is MISSING:
            _components = []
        else:
            _components = _build_components(components=components)

        if not files or files is MISSING:
            _files = []
        elif isinstance(files, list):
            _files = [file._json_payload(id) for id, file in enumerate(files)]
        else:
            _files = [files._json_payload(0)]
            files = [files]

        _files.extend(_attachments)

        payload = dict(
            content=_content,
            tts=_tts,
            attachments=_files,
            embeds=_embeds,
            allowed_mentions=_allowed_mentions,
            components=_components,
            sticker_ids=_sticker_ids,
        )

        res = await self._client.create_message(
            channel_id=int(self.id), payload=payload, files=files
        )

        # dumb hack, discord doesn't send the full author data
        author = {"id": None, "username": None, "discriminator": None}
        author.update(res["author"])
        res["author"] = author

        return Message(**res, _client=self._client)

    async def delete(self) -> None:
        """
        Deletes the channel.
        """
        if not self._client:
            raise LibraryException(code=13)
        await self._client.delete_channel(channel_id=int(self.id))

    async def modify(
        self,
        name: Optional[str] = MISSING,
        topic: Optional[str] = MISSING,
        bitrate: Optional[int] = MISSING,
        user_limit: Optional[int] = MISSING,
        rate_limit_per_user: Optional[int] = MISSING,
        position: Optional[int] = MISSING,
        permission_overwrites: Optional[List[Overwrite]] = MISSING,
        parent_id: Optional[int] = MISSING,
        nsfw: Optional[bool] = MISSING,
        archived: Optional[bool] = MISSING,
        auto_archive_duration: Optional[int] = MISSING,
        locked: Optional[bool] = MISSING,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Edits the channel.

        .. note::
            The fields `archived`, `auto_archive_duration` and `locked` require the provided channel to be a thread.

        :param name?: The name of the channel, defaults to the current value of the channel
        :type name?: str
        :param topic?: The topic of that channel, defaults to the current value of the channel
        :type topic?: Optional[str]
        :param bitrate?: (voice channel only) The bitrate (in bits) of the voice channel, defaults to the current value of the channel
        :type bitrate?: Optional[int]
        :param user_limit?: (voice channel only) Maximum amount of users in the channel, defaults to the current value of the channel
        :type user_limit?: Optional[int]
        :param rate_limit_per_use?: Amount of seconds a user has to wait before sending another message (0-21600), defaults to the current value of the channel
        :type rate_limit_per_user: Optional[int]
        :param position?: Sorting position of the channel, defaults to the current value of the channel
        :type position?: Optional[int]
        :param parent_id?: The id of the parent category for a channel, defaults to the current value of the channel
        :type parent_id?: Optional[int]
        :param nsfw?: Whether the channel is nsfw or not, defaults to the current value of the channel
        :type nsfw?: Optional[bool]
        :param permission_overwrites?: The permission overwrites, if any
        :type permission_overwrites?: Optional[List[Overwrite]]
        :param archived?: Whether the thread is archived
        :type archived?: Optional[bool]
        :param auto_archive_duration?: The time after the thread is automatically archived. One of 60, 1440, 4320, 10080
        :type auto_archive_duration?: Optional[int]
        :param locked?: Whether the thread is locked
        :type locked?: Optional[bool]
        :param reason?: The reason for the edit
        :type reason?: Optional[str]
        :return: The modified channel as new object
        :rtype: Channel
        """
        if not self._client:
            raise LibraryException(code=13)
        _name = self.name if name is MISSING else name
        _topic = self.topic if topic is MISSING else topic
        _bitrate = self.bitrate if bitrate is MISSING else bitrate
        _user_limit = self.user_limit if user_limit is MISSING else user_limit
        _rate_limit_per_user = (
            self.rate_limit_per_user if rate_limit_per_user is MISSING else rate_limit_per_user
        )
        _position = self.position if position is MISSING else position
        _parent_id = (
            (int(self.parent_id) if self.parent_id else None)
            if parent_id is MISSING
            else int(parent_id)
        )
        _nsfw = self.nsfw if nsfw is MISSING else nsfw
        _permission_overwrites = (
            [overwrite._json for overwrite in self.permission_overwrites]
            if self.permission_overwrites
            else None
            if permission_overwrites is MISSING
            else [overwrite._json for overwrite in permission_overwrites]
        )
        _type = self.type

        payload = dict(
            name=_name,
            type=_type,
            topic=_topic,
            bitrate=_bitrate,
            user_limit=_user_limit,
            rate_limit_per_user=_rate_limit_per_user,
            position=_position,
            parent_id=_parent_id,
            nsfw=_nsfw,
            permission_overwrites=_permission_overwrites,
        )

        if (
            archived is not MISSING or auto_archive_duration is not MISSING or locked is not MISSING
        ) and not self.thread_metadata:
            raise LibraryException(message="The specified channel is not a Thread!", code=12)

        if archived is not MISSING:
            payload["archived"] = archived
        if auto_archive_duration is not MISSING:
            payload["auto_archive_duration"] = auto_archive_duration
        if locked is not MISSING:
            payload["locked"] = locked

        res = await self._client.modify_channel(
            channel_id=int(self.id),
            reason=reason,
            payload=payload,
        )

        self.update(res)

        return self

    async def set_name(
        self,
        name: str,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the name of the channel.

        :param name: The new name of the channel
        :type name: str
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(name=name, reason=reason)

    async def set_topic(
        self,
        topic: str,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the topic of the channel.

        :param topic: The new topic of the channel
        :type topic: str
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(topic=topic, reason=reason)

    async def set_bitrate(
        self,
        bitrate: int,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the bitrate of the channel.

        :param bitrate: The new bitrate of the channel
        :type bitrate: int
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        if self.type != ChannelType.GUILD_VOICE:
            raise LibraryException(message="Bitrate is only available for VoiceChannels", code=12)

        return await self.modify(bitrate=bitrate, reason=reason)

    async def set_user_limit(
        self,
        user_limit: int,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the user_limit of the channel.

        :param user_limit: The new user limit of the channel
        :type user_limit: int
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        if self.type != ChannelType.GUILD_VOICE:
            raise LibraryException(
                message="user_limit is only available for VoiceChannels", code=12
            )

        return await self.modify(user_limit=user_limit, reason=reason)

    async def set_rate_limit_per_user(
        self,
        rate_limit_per_user: int,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the amount of seconds a user has to wait before sending another message.

        :param rate_limit_per_user: The new rate_limit_per_user of the channel (0-21600)
        :type rate_limit_per_user: int
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(rate_limit_per_user=rate_limit_per_user, reason=reason)

    async def set_position(
        self,
        position: int,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the position of the channel.

        :param position: The new position of the channel
        :type position: int
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(position=position, reason=reason)

    async def set_parent_id(
        self,
        parent_id: int,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the parent_id of the channel.

        :param parent_id: The new parent_id of the channel
        :type parent_id: int
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(parent_id=parent_id, reason=reason)

    async def set_nsfw(
        self,
        nsfw: bool,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the nsfw-flag of the channel.

        :param nsfw: The new nsfw-flag of the channel
        :type nsfw: bool
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(nsfw=nsfw, reason=reason)

    async def archive(
        self,
        archived: bool = True,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the archived state of the thread.

        :param archived: Whether the Thread is archived, defaults to True
        :type archived: bool
        :param reason?: The reason of the archiving
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(archived=archived, reason=reason)

    async def set_auto_archive_duration(
        self,
        auto_archive_duration: int,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the time after the thread is automatically archived.

        :param auto_archive_duration: The time after the thread is automatically archived. One of 60, 1440, 4320, 10080
        :type auto_archive_duration: int
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(auto_archive_duration=auto_archive_duration, reason=reason)

    async def lock(
        self,
        locked: bool = True,
        *,
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Sets the locked state of the thread.

        :param locked: Whether the Thread is locked, defaults to True
        :type locked: bool
        :param reason?: The reason of the edit
        :type reason?: Optional[str]
        :return: The edited channel
        :rtype: Channel
        """

        return await self.modify(locked=locked, reason=reason)

    async def add_member(
        self,
        member_id: Union[int, Snowflake, "Member"],
    ) -> None:
        """
        This adds a member to the channel, if the channel is a thread.

        :param member_id: The id of the member to add to the channel
        :type member_id: int
        """
        if not self._client:
            raise LibraryException(code=13)
        if not self.thread_metadata:
            raise LibraryException(message="The Channel you specified is not a thread!", code=12)

        _member_id = (
            int(member_id) if isinstance(member_id, (int, Snowflake)) else int(member_id.id)
        )

        await self._client.add_member_to_thread(thread_id=int(self.id), user_id=_member_id)

    async def remove_member(
        self,
        member_id: Union[int, Snowflake, "Member"],
    ) -> None:
        """
        This removes a member of the channel, if the channel is a thread.

        :param member_id: The id of the member to remove of the channel
        :type member_id: int
        """
        if not self._client:
            raise LibraryException(code=13)
        if not self.thread_metadata:
            raise LibraryException(message="The Channel you specified is not a thread!", code=12)

        _member_id = (
            int(member_id) if isinstance(member_id, (int, Snowflake)) else int(member_id.id)
        )

        await self._client.remove_member_from_thread(thread_id=int(self.id), user_id=_member_id)

    async def pin_message(
        self,
        message_id: Union[int, Snowflake, "Message"],
    ) -> None:
        """
        Pins a message to the channel.

        :param message_id: The id of the message to pin
        :type message_id: Union[int, Snowflake, "Message"]
        """
        if not self._client:
            raise LibraryException(code=13)

        _message_id = (
            int(message_id) if isinstance(message_id, (int, Snowflake)) else int(message_id.id)
        )

        await self._client.pin_message(channel_id=int(self.id), message_id=_message_id)

    async def unpin_message(
        self,
        message_id: Union[int, Snowflake, "Message"],
    ) -> None:
        """
        Unpins a message from the channel.

        :param message_id: The id of the message to unpin
        :type message_id: Union[int, Snowflake, "Message"]
        """
        if not self._client:
            raise LibraryException(code=13)

        _message_id = (
            int(message_id) if isinstance(message_id, (int, Snowflake)) else int(message_id.id)
        )

        await self._client.unpin_message(channel_id=int(self.id), message_id=_message_id)

    async def publish_message(
        self,
        message_id: Union[int, Snowflake, "Message"],
    ) -> "Message":
        """Publishes (API calls it crossposts) a message in the channel to any that is followed by.

        :param message_id: The id of the message to publish
        :type message_id: Union[int, Snowflake, "Message"]
        :return: The message published
        :rtype: Message
        """
        if not self._client:
            raise LibraryException(code=13)
        from .message import Message

        _message_id = (
            int(message_id) if isinstance(message_id, (int, Snowflake)) else int(message_id.id)
        )

        res = await self._client.publish_message(channel_id=int(self.id), message_id=_message_id)

        return Message(**res, _client=self._client)

    async def get_pinned_messages(self) -> List["Message"]:
        """
        Get all pinned messages from the channel.

        :return: A list of pinned message objects.
        :rtype: List[Message]
        """
        if not self._client:
            raise LibraryException(code=13)
        from .message import Message

        res = await self._client.get_pinned_messages(int(self.id))
        return [Message(**message, _client=self._client) for message in res]

    async def get_message(
        self,
        message_id: Union[int, Snowflake],
    ) -> "Message":
        """
        Gets a message sent in that channel.

        :param message_id: The ID of the message to get
        :type message_id: Union[int, Snowflake]
        :return: The message as object
        :rtype: Message
        """
        res = await self._client.get_message(
            channel_id=int(self.id),
            message_id=int(message_id),
        )
        from .message import Message

        return Message(**res, _client=self._client)

    async def purge(
        self,
        amount: int,
        check: Callable[[Any], bool] = MISSING,
        before: Optional[int] = MISSING,
        reason: Optional[str] = None,
        bulk: Optional[bool] = True,
    ) -> List["Message"]:  # noqa  # sourcery skip: low-code-quality
        """
        Purges a given amount of messages from a channel. You can specify a check function to exclude specific messages.

        .. warning:: Calling this method can lead to rate-limits when purging higher amounts of messages.

        .. code-block:: python

            def check_pinned(message):
                return not message.pinned  # This returns `True` only if the message is the message is not pinned
            await channel.purge(100, check=check_pinned)  # This will delete the newest 100 messages that are not pinned in that channel

        :param amount: The amount of messages to delete
        :type amount: int
        :param check?: The function used to check if a message should be deleted. The message is only deleted if the check returns `True`
        :type check?: Callable[[Message], bool]
        :param before?: An id of a message to purge only messages before that message
        :type before?: Optional[int]
        :param bulk?: Whether to bulk delete the messages (you cannot delete messages older than 14 days, default) or to delete every message seperately
        :param bulk: Optional[bool]
        :param reason?: The reason of the deletes
        :type reason?: Optional[str]
        :return: A list of the deleted messages
        :rtype: List[Message]
        """
        if not self._client:
            raise LibraryException(code=13)
        from .message import Message

        _before = None if before is MISSING else before
        _all = []
        if bulk:
            _allowed_time = datetime.now(tz=timezone.utc) - timedelta(days=14)
            _stop = False
            while amount > 100:

                messages = [
                    Message(**res)
                    for res in await self._client.get_channel_messages(
                        channel_id=int(self.id),
                        limit=100,
                        before=_before,
                    )
                ]
                messages2 = messages.copy()
                for message in messages2:
                    if datetime.fromisoformat(str(message.timestamp)) < _allowed_time:
                        messages.remove(message)
                        _stop = True
                messages2 = messages.copy()
                for message in messages2:
                    if message.flags == (1 << 7):
                        messages.remove(message)
                        amount += 1
                        _before = int(message.id)
                    elif check is not MISSING:
                        _check = check(message)
                        if not _check:
                            messages.remove(message)
                            amount += 1
                            _before = int(message.id)
                _all += messages
                if len(messages) > 1:
                    await self._client.delete_messages(
                        channel_id=int(self.id),
                        message_ids=[int(message.id) for message in messages],
                        reason=reason,
                    )
                elif len(messages) == 1:
                    await self._client.delete_message(
                        channel_id=int(self.id),
                        message_id=int(messages[0].id),
                        reason=reason,
                    )
                elif _stop:
                    return _all
                else:
                    continue
                if _stop:
                    return _all

                amount -= 100

            while amount > 1:
                messages = [
                    Message(**res)
                    for res in await self._client.get_channel_messages(
                        channel_id=int(self.id),
                        limit=amount,
                        before=_before,
                    )
                ]
                messages2 = messages.copy()
                for message in messages2:
                    if datetime.fromisoformat(str(message.timestamp)) < _allowed_time:
                        messages.remove(message)
                        _stop = True
                amount -= amount
                messages2 = messages.copy()
                for message in messages2:
                    if message.flags == (1 << 7):
                        messages.remove(message)
                        amount += 1
                        _before = int(message.id)
                    elif check is not MISSING:
                        _check = check(message)
                        if not _check:
                            messages.remove(message)
                            amount += 1
                            _before = int(message.id)
                _all += messages
                if len(messages) > 1:
                    await self._client.delete_messages(
                        channel_id=int(self.id),
                        message_ids=[int(message.id) for message in messages],
                        reason=reason,
                    )
                elif len(messages) == 1:
                    await self._client.delete_message(
                        channel_id=int(self.id),
                        message_id=int(messages[0].id),
                        reason=reason,
                    )
                elif _stop:
                    return _all
                else:
                    continue
                if _stop:
                    return _all
            while amount == 1:
                messages = [
                    Message(**res)
                    for res in await self._client.get_channel_messages(
                        channel_id=int(self.id),
                        limit=amount,
                        before=_before,
                    )
                ]
                amount -= 1
                messages2 = messages.copy()
                for message in messages2:
                    if message.flags == (1 << 7):
                        messages.remove(message)
                        amount += 1
                        _before = int(message.id)
                    elif check is not MISSING:
                        _check = check(message)
                        if not _check:
                            messages.remove(message)
                            amount += 1
                            _before = int(message.id)
                _all += messages
                if not messages:
                    continue
                await self._client.delete_message(
                    channel_id=int(self.id),
                    message_id=int(messages[0].id),
                    reason=reason,
                )

        else:
            while amount > 0:
                messages = [
                    Message(**res)
                    for res in await self._client.get_channel_messages(
                        channel_id=int(self.id),
                        limit=min(amount, 100),
                        before=_before,
                    )
                ]

                amount -= min(amount, 100)
                messages2 = messages.copy()
                for message in messages2:
                    if message.flags == (1 << 7):
                        messages.remove(message)
                        amount += 1
                        _before = int(message.id)
                    elif check is not MISSING:
                        _check = check(message)
                        if not _check:
                            messages.remove(message)
                            amount += 1
                            _before = int(message.id)
                _all += messages

            for message in _all:
                await self._client.delete_message(
                    channel_id=int(self.id),
                    message_id=int(message.id),
                    reason=reason,
                )

        return _all

    async def create_thread(
        self,
        name: str,
        type: Optional[ChannelType] = ChannelType.GUILD_PUBLIC_THREAD,
        auto_archive_duration: Optional[int] = MISSING,
        invitable: Optional[bool] = MISSING,
        message_id: Optional[Union[int, Snowflake, "Message"]] = MISSING,  # noqa
        reason: Optional[str] = None,
    ) -> "Channel":
        """
        Creates a thread in the Channel.

        :param name: The name of the thread
        :type name: str
        :param auto_archive_duration?: duration in minutes to automatically archive the thread after recent activity,
            can be set to: 60, 1440, 4320, 10080
        :type auto_archive_duration?: Optional[int]
        :param type?: The type of thread, defaults to public. ignored if creating thread from a message
        :type type?: Optional[ChannelType]
        :param invitable?: Boolean to display if the Thread is open to join or private.
        :type invitable?: Optional[bool]
        :param message_id?: An optional message to create a thread from.
        :type message_id?: Optional[Union[int, Snowflake, "Message"]]
        :param reason?: An optional reason for the audit log
        :type reason?: Optional[str]
        :return: The created thread
        :rtype: Channel
        """
        if not self._client:
            raise LibraryException(code=13)
        if type not in [
            ChannelType.GUILD_NEWS_THREAD,
            ChannelType.GUILD_PUBLIC_THREAD,
            ChannelType.GUILD_PRIVATE_THREAD,
        ]:
            raise LibraryException(message="type must be a thread type!", code=12)

        _auto_archive_duration = None if auto_archive_duration is MISSING else auto_archive_duration
        _invitable = None if invitable is MISSING else invitable
        _message_id = (
            None
            if message_id is MISSING
            else (
                int(message_id) if isinstance(message_id, (int, Snowflake)) else int(message_id.id)
            )
        )
        res = await self._client.create_thread(
            channel_id=int(self.id),
            thread_type=type.value,
            name=name,
            auto_archive_duration=_auto_archive_duration,
            invitable=_invitable,
            message_id=_message_id,
            reason=reason,
        )

        return Channel(**res, _client=self._client)

    @property
    def url(self) -> str:
        _guild_id = self.guild_id if isinstance(self.guild_id, int) else "@me"
        return f"https://discord.com/channels/{_guild_id}/{self.id}"

    async def create_invite(
        self,
        max_age: Optional[int] = 86400,
        max_uses: Optional[int] = 0,
        temporary: Optional[bool] = False,
        unique: Optional[bool] = False,
        target_type: Optional["InviteTargetType"] = MISSING,
        target_user_id: Optional[int] = MISSING,
        target_application_id: Optional[int] = MISSING,
        reason: Optional[str] = None,
    ) -> "Invite":
        """
        Creates an invite for the channel

        :param max_age?: Duration of invite in seconds before expiry, or 0 for never. between 0 and 604800 (7 days). Default 86400 (24h)
        :type max_age?: Optional[int]
        :param max_uses?: Max number of uses or 0 for unlimited. between 0 and 100. Default 0
        :type max_uses?: Optional[int]
        :param temporary?: Whether this invite only grants temporary membership. Default False
        :type temporary?: Optional[bool]
        :param unique?: If true, don't try to reuse a similar invite (useful for creating many unique one time use invites). Default False
        :type unique?: Optional[bool]
        :param target_type?: The type of target for this voice channel invite
        :type target_type?: Optional["InviteTargetType"]
        :param target_user_id?: The id of the user whose stream to display for this invite, required if target_type is STREAM, the user must be streaming in the channel
        :type target_user_id?: Optional[int]
        :param target_application_id?: The id of the embedded application to open for this invite, required if target_type is EMBEDDED_APPLICATION, the application must have the EMBEDDED flag
        :type target_application_id?: Optional[int]
        :param reason?: The reason for the creation of the invite
        :type reason?: Optional[str]
        """

        if not self._client:
            raise LibraryException(code=13)

        payload = {
            "max_age": max_age,
            "max_uses": max_uses,
            "temporary": temporary,
            "unique": unique,
        }

        if (target_user_id is not MISSING and target_user_id) and (
            target_application_id is not MISSING and target_application_id
        ):
            raise LibraryException(
                message="target user id and target application are mutually exclusive!", code=12
            )

        elif (
            (target_user_id is not MISSING and target_user_id)
            or (target_application_id is not MISSING and target_application_id)
        ) and not target_type:
            raise LibraryException(
                message="you have to specify a target_type if you specify target_user-/target_application_id",
                code=12,
            )

        if target_user_id is not MISSING:
            payload["target_type"] = (
                target_type if isinstance(target_type, int) else target_type.value
            )
            payload["target_user_id"] = target_user_id

        if target_application_id is not MISSING:
            payload["target_type"] = (
                target_type if isinstance(target_type, int) else target_type.value
            )
            payload["target_application_id"] = target_application_id

        res = await self._client.create_channel_invite(
            channel_id=int(self.id),
            payload=payload,
            reason=reason,
        )

        from .guild import Invite

        return Invite(**res, _client=self._client)

    async def get_history(self, limit: int = 100) -> Optional[List["Message"]]:
        """
        Gets messages from the channel's history.

        :param limit?: The amount of messages to get. Default 100
        :type limit?: int
        :return: A list of messages
        :rtype: List[Message]
        """

        if not self._client:
            raise LibraryException(code=13)

        from .message import Message

        _messages: List[Message] = []
        _before: Optional[int] = None
        while limit > 100:
            _msgs = [
                Message(**res, _client=self._client)
                for res in await self._client.get_channel_messages(
                    channel_id=int(self.id),
                    limit=100,
                    before=_before,
                )
            ]
            limit -= 100
            if not _msgs:
                return _messages
            _before = int(_msgs[-1].id)

            for msg in _msgs:
                if msg in _messages:
                    return _messages
                else:
                    _messages.append(msg)

        if limit > 0:
            _msgs = [
                Message(**res, _client=self._client)
                for res in await self._client.get_channel_messages(
                    channel_id=int(self.id), limit=limit, before=_before
                )
            ]
            if not _msgs:
                return _messages
            for msg in _msgs:
                if msg in _messages:
                    return _messages
                else:
                    _messages.append(msg)

        return _messages

    async def get_webhooks(self) -> List[Webhook]:
        """
        Gets a list of webhooks of that channel
        """

        if not self._client:
            raise LibraryException(code=13)

        res = await self._client.get_channel_webhooks(int(self.id))
        return [Webhook(**_, _client=self._client) for _ in res]

    async def get_members(self) -> List[ThreadMember]:
        """
        Gets the list of thread members

        :return: The members of the thread.
        :rtype: List[ThreadMember]
        """
        if not self._client:
            raise LibraryException(code=13)
        if not self.thread_metadata:
            raise LibraryException(message="The Channel you specified is not a thread!", code=12)

        res = await self._client.list_thread_members(int(self.id))
        return [ThreadMember(**member, _client=self._client) for member in res]

    async def leave(self) -> None:
        """
        Removes the bot from the thread
        """
        if not self._client:
            raise LibraryException(code=13)
        if not self.thread_metadata:
            raise LibraryException(message="The Channel you specified is not a thread!", code=12)

        await self._client.leave_thread(int(self.id))

    async def join(self) -> None:
        """
        Add the bot to the thread
        """
        if not self._client:
            raise LibraryException(code=13)
        if not self.thread_metadata:
            raise LibraryException(message="The Channel you specified is not a thread!", code=12)

        await self._client.join_thread(int(self.id))


@define()
class Thread(Channel):
    """An object representing a thread.

    .. note::
        This is a derivation of the base Channel, since a
        thread can be its own event.
    """

    ...
