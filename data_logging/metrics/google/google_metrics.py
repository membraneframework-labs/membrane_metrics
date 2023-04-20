import os
from datetime import date
from typing import List

from config.app_config import AppConfig
from data_logging.metrics.google.google_api import GoogleAPI
from data_logging.metrics.metrics import Metrics
from data_logging.mongodb.collection import MongoCollection
from data_logging.time_series import TimeSeries, TimeSeriesEntry


class GoogleMetrics(Metrics):
    def __init__(self, app_config: AppConfig):
        self.start_date: date = app_config.start_date
        self.end_date: date = app_config.end_date
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = app_config.google_config.path_to_secrets_file
        self.time_spent_per_day_entries: list[
            TimeSeriesEntry
        ] = self.__get_time_spent_per_day()
        self.users_in_tutorials_per_day: list[
            TimeSeriesEntry
        ] = self.__get_users_in_tutorials_per_day()
        self.users_from_traffic_source_per_day: list[
            TimeSeriesEntry
        ] = self.__get_users_from_traffic_source_per_day()
        self.bounce_rate_per_day: list[
            TimeSeriesEntry
        ] = self.__get_bounce_rate_per_day()

    def get_metric_series(self) -> list[TimeSeries]:
        return [
            TimeSeries(
                MongoCollection.GoogleTimeSpentPerDay,
                self.time_spent_per_day_entries,
            ),
            TimeSeries(
                MongoCollection.GoogleBounceRatePerDay, self.bounce_rate_per_day
            ),
            TimeSeries(
                MongoCollection.GoogleUsersInTutorialPerDay,
                self.users_in_tutorials_per_day,
            ),
            TimeSeries(
                MongoCollection.GoogleUsersFromTrafficSourcePerDay,
                self.users_from_traffic_source_per_day,
            ),
        ]

    def __get_time_spent_per_day(self) -> List[TimeSeriesEntry]:
        average_user_enganement_duration_per_day = GoogleAPI.get_average_user_enganement_duration(
            self.start_date, self.end_date
        )
        entries = [
            TimeSeriesEntry(day, average_user_enganement_duration_per_day[day])
            for day in average_user_enganement_duration_per_day.keys()
        ]
        return entries

    def __get_users_in_tutorials_per_day(self) -> List[TimeSeriesEntry]:
        users_in_tutorial_per_day = GoogleAPI.get_users_in_tutorial(
            self.start_date, self.end_date
        )
        cumulated_entries = []
        for tutorial_name in users_in_tutorial_per_day.keys():
            entries = [
                TimeSeriesEntry(day, value, meta_filed_value=tutorial_name)
                for day, value in users_in_tutorial_per_day[tutorial_name].items()
            ]
            cumulated_entries.extend(entries)
        return cumulated_entries

    def __get_users_from_traffic_source_per_day(
        self,
    ) -> List[TimeSeriesEntry]:
        number_of_users_from_source_pers_day = GoogleAPI.get_users_source(
            self.start_date, self.end_date
        )

        cumulated_entries = []
        for source in number_of_users_from_source_pers_day.keys():
            entries = [
                TimeSeriesEntry(day, value, meta_filed_value=source)
                for day, value in number_of_users_from_source_pers_day[source].items()
            ]
            cumulated_entries.extend(entries)
        return cumulated_entries

    def __get_bounce_rate_per_day(self) -> List[TimeSeriesEntry]:
        bounce_rate_per_day = GoogleAPI.get_bounce_rate(self.start_date, self.end_date)
        entries = [
            TimeSeriesEntry(day, bounce_rate_per_day[day])
            for day in bounce_rate_per_day.keys()
        ]
        return entries
