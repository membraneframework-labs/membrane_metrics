from data_logging.metrics.metrics import Metrics
from config.app_config import AppConfig
from data_logging.metrics.google.google_api import GoogleAPI, PropertyId
from data_logging.time_series import TimeSeries, TimeSeriesEntry
from data_logging.mongodb.collection import MongoCollection
import os
from typing import List


class GoogleMetrics(Metrics):
    property_id: PropertyId = "321354678"

    def __init__(self, app_config: AppConfig):
        self.start_date = app_config.start_date
        self.end_date = app_config.end_date
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = app_config.google_config.path_to_secrets_file

    def get_metric_series(self) -> list[TimeSeries]:
        return (
            [self.__get_time_spent(), self.__get_bounce_rate()]
            + self.__get_unique_users_in_tutorials()
            + self.__get_unique_users_in_tutorials()
        )

    def __get_time_spent(self) -> TimeSeries:
        total_time_spent_per_day = GoogleAPI.get_total_time_spent(
            GoogleMetrics.property_id, self.start_date, self.end_date
        )
        entries = [
            TimeSeriesEntry(day, total_time_spent_per_day[day])
            for day in total_time_spent_per_day.keys()
        ]
        series = TimeSeries(MongoCollection.GoogleTimeSpentPerDay, entries)
        return series

    def __get_unique_users_in_tutorials(self) -> List[TimeSeries]:
        unique_users_in_tutorial_per_day = GoogleAPI.get_unique_users_in_tutorial(
            GoogleMetrics.property_id, self.start_date, self.end_date
        )
        series_for_all_tutorials = []
        for tutorial_name in unique_users_in_tutorial_per_day.keys():
            entries = [
                TimeSeriesEntry(day, value, meta_filed_value=tutorial_name)
                for day, value in unique_users_in_tutorial_per_day[
                    tutorial_name
                ].items()
            ]
            series = TimeSeries(
                MongoCollection.GoogleUniqueUsersInTutorialPerDay, entries
            )
            series_for_all_tutorials.append(series)
        return series_for_all_tutorials

    def __get_unique_users_in_tutorials(self) -> List[TimeSeries]:
        number_of_users_from_source_pers_day = GoogleAPI.get_users_source(
            GoogleMetrics.property_id, self.start_date, self.end_date
        )
        series_for_all_sources = []
        for source in number_of_users_from_source_pers_day.keys():
            entries = [
                TimeSeriesEntry(day, value, meta_filed_value=source)
                for day, value in number_of_users_from_source_pers_day[source].items()
            ]
            series = TimeSeries(
                MongoCollection.GoogleUsersFromTrafficSourcePerDay, entries
            )
            series_for_all_sources.append(series)
        return series_for_all_sources

    def __get_bounce_rate(self) -> TimeSeries:
        bounce_rate_per_day = GoogleAPI.get_bounce_rate(
            GoogleMetrics.property_id, self.start_date, self.end_date
        )
        entries = [
            TimeSeriesEntry(day, bounce_rate_per_day[day])
            for day in bounce_rate_per_day.keys()
        ]
        series = TimeSeries(MongoCollection.GoogleBounceRatePerDay, entries)
        return series
