import requests

from data_logging.discord.api_facade.channel import DiscordChannel
from data_logging.discord.api_facade.message import DiscordMessage
from data_logging.discord.api_facade.guild_member import DiscordGuildMember
from data_logging.discord.api_facade.types import DiscordGuildID
from context.context import Context
from context.discord_context import BotToken


class BadDiscordAPIResponseError(Exception):
    pass


class NotFoundServerError(Exception):
    pass


class MultipleServersWithSameNameError(Exception):
    pass


class DiscordAPI:
    """
    Facade over discord api
    """

    @staticmethod
    def send_get_request(bot_token: BotToken, endpoint: str, params: dict = {}):
        REQUEST_HEADER = {'Authorization': f'Bot {bot_token}'}
        DISCORD_BASE_URL = 'https://discord.com/api/v10'
        response = requests.get(
            DISCORD_BASE_URL + endpoint, headers=REQUEST_HEADER, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_guild_members(bot_token: BotToken, guild_id: DiscordGuildID) -> dict[str, DiscordMessage]:
        MAX_REQUEST_LIMIT = 1000
        params = {'limit': MAX_REQUEST_LIMIT}
        guild_members_response_objs_list = DiscordAPI.send_get_request(
            bot_token, f'/guilds/{guild_id}/members', params)
        last_response_member_count = len(guild_members_response_objs_list) 
        
        while last_response_member_count == MAX_REQUEST_LIMIT:
            last_response_last_member_id = guild_members_response_objs_list[-1]['user']['id']
            params = {'limit': MAX_REQUEST_LIMIT, 'after': last_response_last_member_id}
            response = DiscordAPI.send_get_request(bot_token, f'/guilds/{guild_id}/members', params)
            last_response_member_count = len(response)
            guild_members_response_objs_list += response
        
        return [DiscordGuildMember(member_response_obj) for member_response_obj in guild_members_response_objs_list]

    @staticmethod
    def get_guild_channels(bot_token: BotToken, guild_id: DiscordGuildID) -> list[DiscordChannel]:
        channel_response_objs_list = DiscordAPI.send_get_request(
            bot_token, f'/guilds/{guild_id}/channels')
        return [DiscordChannel(channel, DiscordAPI.get_channel_messages(bot_token, channel['id'])) for channel in channel_response_objs_list]

    @staticmethod
    def get_channel_messages(bot_token: BotToken, channel_id: str) -> list[DiscordMessage]:
        message_response_objs_list = DiscordAPI.send_get_request(
            bot_token, f'/channels/{channel_id}/messages')
        return [DiscordMessage(message) for message in message_response_objs_list]
