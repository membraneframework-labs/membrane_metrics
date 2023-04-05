from collections import Counter
from datetime import date, timedelta

import dateutil.parser as parser
import pandas as pd

import data_logging.metrics.discord.api_facade.api_facade as discord_api_facade
from config.discord_config import DiscordConfig
from data_logging.time_series import TimeSeriesEntry


class DiscordGuild:
    members: pd.DataFrame
    channels_messages: dict[str, pd.DataFrame]

    def __init__(self, discord_config: DiscordConfig) -> None:
        self.members = discord_api_facade.get_guild_members(
            discord_config.bot_token, discord_config.guild_id)
        self.channels_messages = discord_api_facade.get_guild_messages(
            discord_config.bot_token, discord_config.guild_id)

    def get_members_at_days(self, start_date: date, end_date: date) -> list[TimeSeriesEntry]:
        members_joins = self.members['joined_at']
        members_joins = members_joins.apply(
            lambda timestamp: parser.parse(timestamp).date())

        members_previous_day = len(members_joins[members_joins <= start_date])
        new_joins = Counter(members_joins)

        members_at_days = []
        for day in pd.date_range(start_date, end_date, inclusive='left').date:
            members_at_day = members_previous_day + new_joins[day]
            members_at_days.append((day, members_at_day))
            members_previous_day = members_at_day

        return [TimeSeriesEntry(day, members_at_day) for day, members_at_day in members_at_days]

    def get_messages_per_channel_per_day(self, start_date: date, end_date: date) -> list[TimeSeriesEntry]:
        time_series_entries = []
        for channel_name, messages in self.channels_messages.items():
            messages_series = messages['timestamp']
            messages_series = messages_series.apply(
                lambda timestamp: parser.parse(timestamp).date())
            messages_stats = Counter(messages_series)
            time_series_entries += \
                [TimeSeriesEntry(day, messages_stats[day], channel_name)
                 for day in pd.date_range(start_date, end_date, inclusive='left').date]

        return time_series_entries
