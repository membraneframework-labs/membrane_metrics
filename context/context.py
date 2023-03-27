import tomli
from context.discord_context import DiscordContext, BotToken, GuildID
from datetime import date
from dataclasses import dataclass


@dataclass
class Context:
    start_date: date
    end_date: date
    mongodb_connection_url = str
    discord_context: DiscordContext

    def __init__(self):
        with open('config.toml', "rb") as file:
            config = tomli.load(file)
        self.start_date = Context.get_start_date(config)
        self.end_date = date.today()
        self.mongodb_connection_url = Context.get_mongodb_connection_url(config)
        self.discord_context = Context.get_discord_context(config)

    @staticmethod
    def get_start_date(config: dict) -> date:
        return date.fromisoformat(config['general']['start_date'])

    @staticmethod
    def get_mongodb_connection_url(config: dict) -> str:
        return config['mongodb']['url']

    @staticmethod
    def get_discord_context(config: dict) -> DiscordContext:
        bot_token = BotToken(config['discord']['bot_token'])
        guild_id = GuildID(config['discord']['guild_id'])
        return DiscordContext(bot_token, guild_id)
