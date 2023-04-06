from datetime import date

import tomli

from config.discord_config import DiscordConfig, BotToken, GuildID
from config.google_config import GoogleConfig

class AppConfig:
    start_date: date
    end_date: date
    mongodb_connection_url = str
    discord_config: DiscordConfig
    google_config: GoogleConfig

    def __init__(self):
        with open("config.toml", "rb") as file:
            config = tomli.load(file)
        self.start_date = date.fromisoformat(config["general"]["start_date"])
        self.end_date = AppConfig.get_end_date(config)
        self.mongodb_connection_url = config["mongodb"]["url"]
        self.discord_config = AppConfig.get_discord_config(config)
        self.google_config = AppConfig.get_google_config(config)

    @staticmethod
    def get_discord_config(config: dict) -> DiscordConfig:
        bot_token = BotToken(config["discord"]["bot_token"])
        guild_id = GuildID(config["discord"]["guild_id"])
        return DiscordConfig(bot_token, guild_id)
    
    @staticmethod
    def get_google_config(config: dict) -> GoogleConfig:
        path_to_secrets_file = config["google"]["secrets_file_path"]
        return GoogleConfig(path_to_secrets_file)

    @staticmethod
    def get_end_date(config: dict) -> date:
        match config["general"].get("end_date"):
            case None:
                return date.today()
            case end_date:
                return date.fromisoformat(end_date)
