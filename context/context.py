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
        self.start_date = config['general']['start_date']
        self.end_date = config['general'].get('end_date', date.today())
        self.mongodb_connection_url = config['mongodb']['url']
        self.discord_context = Context.get_discord_context(config)

    @staticmethod
    def get_discord_context(config: dict) -> DiscordContext:
        bot_token = BotToken(config['discord']['bot_token'])
        guild_id = GuildID(config['discord']['guild_id'])
        return DiscordContext(bot_token, guild_id)
