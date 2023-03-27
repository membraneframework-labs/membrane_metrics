from dataclasses import dataclass

from config.app_config import AppConfig
from data_logging.metrics.discord.api_facade.discord_guild import DiscordGuild
from data_logging.metrics.metrics import Metrics
from data_logging.mongodb.collection import MongoCollection
from data_logging.time_series import TimeSeries, TimeSeriesEntry


@dataclass
class DiscordMetrics(Metrics):
    members_at_days: list[TimeSeriesEntry]
    messages_per_channel_per_day: list[TimeSeriesEntry]

    def __init__(self, config: AppConfig) -> None:
        discord_guild = DiscordGuild(config.discord_config)
        self.members_at_days = \
            discord_guild.get_members_at_days(
                config.start_date, config.end_date)
        self.messages_per_channel_per_day = \
            discord_guild.get_messages_per_channel_per_day(
                config.start_date, config.end_date)

    def get_metric_series(self) -> list[TimeSeries]:
        return [
            TimeSeries(MongoCollection.DiscordMembersAtDay,
                       self.members_at_days),
            TimeSeries(MongoCollection.DiscordMessagesPerDayPerChannel,
                       self.messages_per_channel_per_day)
        ]
