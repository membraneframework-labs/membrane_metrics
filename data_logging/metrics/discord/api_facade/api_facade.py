from enum import Enum

import pandas as pd
import requests

from config.discord_config import BotToken, GuildID

DISCORD_BASE_URL = 'https://discord.com/api/v10'
MAX_MEMBERS_REQUEST_LIMIT = 1000
MAX_SEARCH_REQUEST_LIMIT = 25
REQUEST_PER_SECOND_LIMIT = 50


class ChannelType(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GUILD_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15

    def is_message_channel(self) -> bool:
        return self in [ChannelType.GUILD_TEXT, ChannelType.GUILD_ANNOUNCEMENT]


def send_get_request(token: BotToken, endpoint: str, params: dict = {}):
    request_header = {'Authorization': f'Bot {token}'}
    response = requests.get(
        DISCORD_BASE_URL + endpoint, headers=request_header, params=params)
    response.raise_for_status()
    return response.json()


def get_guild_members(bot_token: BotToken, guild_id: GuildID) -> pd.DataFrame:
    params = {'limit': MAX_MEMBERS_REQUEST_LIMIT}
    guild_members_objects = send_get_request(
        bot_token, f'/guilds/{guild_id}/members', params)

    last_response_len = len(guild_members_objects)

    while last_response_len == MAX_MEMBERS_REQUEST_LIMIT:
        params = {'limit': MAX_MEMBERS_REQUEST_LIMIT,
                  'after': guild_members_objects[-1]['user']['id']}
        members_chunk = send_get_request(
            bot_token, f'/guilds/{guild_id}/members', params)
        last_response_len = len(members_chunk)
        guild_members_objects += members_chunk

    return pd.json_normalize(guild_members_objects)


def get_guild_messages(bot_token: BotToken, guild_id: GuildID) -> dict[str, pd.DataFrame]:
    """
    Returns dict channel name -> channel messages
    """

    guild_channels_objects = send_get_request(
        bot_token, f'/guilds/{guild_id}/channels')

    messages = {}
    for channel in guild_channels_objects:
        match _get_channel_messages(bot_token, guild_id, channel):
            case None:
                continue
            case channel_messages:
                messages[channel['name']] = channel_messages

    return messages


def _get_channel_messages(bot_token: BotToken, guild_id: GuildID, channel_object: dict) -> pd.DataFrame or None:
    channel_type = ChannelType(channel_object['type'])
    if channel_type == ChannelType.GUILD_FORUM:
        return pd.DataFrame.from_dict(_get_guild_forum_messages(bot_token, guild_id, channel_object['id']))
    elif channel_type.is_message_channel():
        return pd.DataFrame.from_dict(_get_message_channel_messages(bot_token, channel_object['id']))
    else:
        return None


def _get_guild_forum_messages(bot_token: BotToken, guild_id: GuildID, guild_forum_channel_id: str) -> pd.DataFrame:
    threads = []

    all_active_threads = send_get_request(
        bot_token, f'/guilds/{guild_id}/threads/active')['threads']
    threads += list(filter(lambda thread: thread['parent_id']
                                          == guild_forum_channel_id, all_active_threads))

    threads += send_get_request(
        bot_token, f'/channels/{guild_forum_channel_id}/threads/archived/public')['threads']

    messages = []
    for thread in threads:
        thread_id = thread['id']
        messages += send_get_request(bot_token,
                                     f'/channels/{thread_id}/messages')
    return pd.DataFrame.from_dict(messages)


def _get_message_channel_messages(bot_token: BotToken, channel_id: str) -> pd.DataFrame:
    channel_messages = send_get_request(
        bot_token, f'/channels/{channel_id}/messages')
    return pd.DataFrame.from_dict(channel_messages)
