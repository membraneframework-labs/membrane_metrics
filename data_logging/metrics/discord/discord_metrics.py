from context.context import Context
from data_logging.metrics.metrics import Metrics
from data_logging.metrics.discord.api_facade.discord_guild import DiscordGuild
from data_logging.time_series import TimeSeries, TimeSeriesEntry
from dataclasses import dataclass


@dataclass
class DiscordMetrics(Metrics):
    members_at_day: list[TimeSeriesEntry]
    messages_per_channel_per_day: list[TimeSeriesEntry]

    def __init__(self, context: Context) -> None:
        discord_guild = DiscordGuild(context.discord_context)
        self.members_at_day = \
            discord_guild.get_members_at_days(context.start_date, context.end_date)
        self.messages_per_channel_per_day = \
            discord_guild.get_messages_per_channel_per_day(context.start_date, context.end_date)
    
    def get_metric_series(self) -> list[TimeSeries]:
        return [
            self.members_at_day,
            self.messages_per_channel_per_day
        ]
    
