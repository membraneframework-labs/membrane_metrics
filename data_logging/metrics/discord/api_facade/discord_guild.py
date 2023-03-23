import pandas as pd
from context.discord_context import DiscordContext
from collections import Counter
import data_logging.metrics.discord.api_facade.api_facade as discord_api_facade

from pandera.typing import Series
from dataclasses import dataclass
from data_logging.time_series import TimeSeriesEntry
import dateutil.parser as parser
from datetime import date, timedelta

def daterange(start_date: date, end_date: date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

@dataclass
class DiscordGuild:
    members: pd.DataFrame
    channels_messages: dict[str, pd.DataFrame]

    def __init__(self, discord_context: DiscordContext) -> None:
        self.members = discord_api_facade.get_guild_members(
            discord_context.bot_token, discord_context.guild_id)
        self.channels_messages = discord_api_facade.get_guild_messages(discord_context.bot_token, discord_context.guild_id)
        
    def get_members_at_days(self, start_date: date, end_date: date) -> list[TimeSeriesEntry]:
        members_joins = self.members['joined_at']
        members_joins = members_joins.apply(lambda timestamp: parser.parse(timestamp).date())

        members_previous_day = len(members_joins[members_joins <= start_date])
        new_joins = Counter(members_joins)
        
        members_at_days = []
        for day in daterange(start_date, end_date):
            members_at_day = members_previous_day + new_joins[day]
            members_at_days.append((day, members_at_day))
            members_previous_day = members_at_day
            
        return [TimeSeriesEntry(day, members_at_day) for day, members_at_day in members_at_days]
    
    def get_messages_per_channel_per_day(self, start_date: date, end_date: date) -> list[TimeSeriesEntry]:
        time_series_entries = []
        for channel_name, messages in self.channels_messages.items():
            try:
                messages_series = messages['timestamp']
            except KeyError:
                continue
            messages_series = messages_series.apply(lambda timestamp: parser.parse(timestamp).date())
            messages_stats = Counter(messages_series)
            time_series_entries += \
                [TimeSeriesEntry(day, messages_stats[day], channel_name) for day in daterange(start_date, end_date)]
        
        return time_series_entries
    