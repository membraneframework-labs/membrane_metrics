from context.context import Context
from collections import Counter
from datetime import date, timedelta
from data_logging.metrics.metrics import Metrics
from data_logging.discord.api_facade.guild import DiscordGuild
from data_logging.discord.api_facade.channel import DiscordChannel, ChannelType
from data_logging.mongodb.collection import MongoCollection
from data_logging.mongodb.time_series import MongoTimeSeries, MongoTimeSeriesEntry
from dataclasses import dataclass


def daterange(start_date: date, end_date: date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


@dataclass
class DiscordMetrics(Metrics):
    members_at_day: list[MongoTimeSeriesEntry]
    messages_per_channel_per_day: list[MongoTimeSeriesEntry]

    def __init__(self, context: Context) -> None:
        guild = DiscordGuild(context)
        self.messages_per_channel_per_day = self.count_post_per_channel_per_day(
            context.start_date, context.end_date, guild)
        self.members_at_day = self.get_members_at_days(
            guild, context.start_date, context.end_date)

    def count_post_per_channel_per_day(self, start_date: date, end_date: date, guild: DiscordGuild) -> \
            list[MongoTimeSeriesEntry]:
        message_channel_types = [
            ChannelType.GUILD_TEXT, ChannelType.GUILD_FORUM, ChannelType.GUILD_ANNOUNCEMENT]
        messages_per_channel_per_day = []
        for channel in guild.channels:
            if channel.type in message_channel_types:
                channel_messages_per_day = self.get_channel_messages_per_day(
                    channel, start_date, end_date)
                for day, count in channel_messages_per_day:
                    messages_per_channel_per_day.append(
                        MongoTimeSeriesEntry(Metrics.date_to_datetime(day), count, channel.name))
        return messages_per_channel_per_day

    def get_metric_series(self) -> list[MongoTimeSeries]:
        return [self.get_members_per_day_time_series(), self.get_messages_per_channel_per_day_time_series()]

    def get_members_per_day_time_series(self) -> MongoTimeSeries:
        return MongoTimeSeries(MongoCollection.DiscordMembersAtDay, self.members_at_day)

    def get_messages_per_channel_per_day_time_series(self) -> MongoTimeSeries:
        return MongoTimeSeries(MongoCollection.DiscordMessagesPerDayPerChannel, self.messages_per_channel_per_day)

    @staticmethod
    def get_channel_messages_per_day(channel: DiscordChannel, start_date: date, end_date: date) \
            -> list[tuple[date, int]]:
        messages_per_day = Counter([message.timestamp.date()
                                    for message in channel.messages])
        return [(day, messages_per_day[day]) for day in daterange(start_date, end_date)]

    @staticmethod
    def get_members_at_days(guild: DiscordGuild, start_date: date, end_date: date) -> list[MongoTimeSeriesEntry]:
        members_joined_per_day = Counter(
            [member.joined_at for member in guild.members])
        member_count_at_start_date = len(
            list(filter(lambda member: member.joined_at <= start_date, guild.members)))
        members_at_day = [MongoTimeSeriesEntry(
            Metrics.date_to_datetime(start_date), member_count_at_start_date)]
        for day in daterange(start_date + timedelta(1), end_date):
            members_previous_day = members_at_day[-1].value
            members_at_day.append(MongoTimeSeriesEntry(Metrics.date_to_datetime(
                day), members_previous_day + members_joined_per_day[day]))
        return members_at_day
