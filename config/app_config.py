from dataclasses import dataclass
from datetime import date
import tomli
from config.discord_config import DiscordConfig, BotToken, GuildID
from config.twitter_config import TwitterConfig


@dataclass
class AppConfig:
    start_date: date
    end_date: date
    mongodb_connection_url = str
    discord_config: DiscordConfig
    twitter_config: TwitterConfig

    def __init__(self):
        with open('config.toml', "rb") as file:
            config = tomli.load(file)
        self.start_date = date.fromisoformat(config['general']['start_date'])
        self.end_date = AppConfig.get_end_date(config)
        self.mongodb_connection_url = config['mongodb']['url']
        self.discord_config = AppConfig.get_discord_config(config)
        self.twitter_config = AppConfig.get_twitter_config(config)

    @staticmethod
    def get_discord_config(config: dict) -> DiscordConfig:
        bot_token = BotToken(config['discord']['bot_token'])
        guild_id = GuildID(config['discord']['guild_id'])
        return DiscordConfig(bot_token, guild_id)
    
    @staticmethod
    def get_twitter_config(config: dict) -> TwitterConfig:
        bearer_token = config["twitter"]["bearer_token"]
        return TwitterConfig(bearer_token)
    
    @staticmethod
    def get_end_date(config: dict) -> date:
        match config['general'].get('end_date'):
            case None:
                return date.today()
            case end_date:
                return date.fromisoformat(end_date)
