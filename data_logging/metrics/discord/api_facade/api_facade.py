import requests
import pandas as pd

from context.discord_context import BotToken, GuildID
from enum import Enum

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
        return self in [ChannelType.GUILD_TEXT, ChannelType.GUILD_FORUM, ChannelType.GUILD_ANNOUNCEMENT]
    


def send_get_request(bot_token: BotToken, endpoint: str, params: dict = {}):
    REQUEST_HEADER = {'Authorization': f'Bot {bot_token}'}
    DISCORD_BASE_URL = 'https://discord.com/api/v10'
    response = requests.get(
        DISCORD_BASE_URL + endpoint, headers=REQUEST_HEADER, params=params)
    response.raise_for_status()
    return response.json()

def get_guild_members(bot_token: BotToken, guild_id: GuildID) -> pd.DataFrame:
    MAX_REQUEST_LIMIT = 1000
    params = {'limit': MAX_REQUEST_LIMIT}
    guild_members_objects = send_get_request(
        bot_token, f'/guilds/{guild_id}/members', params) 

    while len(guild_members_objects) % MAX_REQUEST_LIMIT == 0:
        params = {'limit': MAX_REQUEST_LIMIT, 'after': guild_members_objects[-1]['user']['id']}
        guild_members_objects += send_get_request(bot_token, f'/guilds/{guild_id}/members', params)
    
    return pd.json_normalize(guild_members_objects)

def get_guild_messages(bot_token: BotToken, guild_id: GuildID) -> dict[str, pd.DataFrame]:
    """
    Returns dict channel name -> channel messages
    """
    guild_channels_objects = send_get_request(bot_token, f'/guilds/{guild_id}/channels')
    
    messages = {}
    for channel in guild_channels_objects:
        if ChannelType(channel['type']).is_message_channel():
            channel_id = channel['id']
            channel_name = channel['name']
            channel_messages = send_get_request(bot_token, f'/channels/{channel_id}/messages')
            messages[channel_name] = pd.DataFrame.from_dict(channel_messages)
    return messages
            
