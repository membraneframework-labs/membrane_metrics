from datetime import date, datetime
from typing import Dict, List, NewType

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

PropertyId = NewType("PropertyID", str)
TrafficSource = NewType("TrafficSource", str)
TutorialName = NewType("TutorialName", str)


class GoogleAPI:
    request_date_format: str = "%Y-%m-%d"
    response_date_format: str = "%Y%m%d"
    property_id: PropertyId = "321354678"

    @staticmethod
    def get_total_time_spent(start_date: date, end_date: date) -> Dict[date, float]:
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{GoogleAPI.property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="averageSessionDuration"), Metric(name="sessions")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        date_result_map = {}
        for row in response.rows:
            average_session_duration = float(row.metric_values[0].value)
            sessions = int(row.metric_values[1].value)
            all_sessions_duration = average_session_duration * sessions  # in seconds
            day = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            date_result_map[day] = all_sessions_duration
        return date_result_map

    @staticmethod
    def get_bounce_rate(start_date: date, end_date: date) -> Dict[date, float]:
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{GoogleAPI.property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="bounceRate")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        date_result_map = {}
        for row in response.rows:
            bounce_rate = float(row.metric_values[0].value)
            day = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            date_result_map[day] = bounce_rate
        return date_result_map

    @staticmethod
    def get_users_source(
        start_date: date, end_date: date
    ) -> Dict[TrafficSource, Dict[date, int]]:
        results_map = {}
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{GoogleAPI.property_id}",
            dimensions=[Dimension(name="date"), Dimension(name="firstUserSource")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        for row in response.rows:
            active_users = int(row.metric_values[0].value)
            day = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            source = row.dimension_values[1].value
            if source not in results_map:
                results_map[source] = {}
            results_map[source][day] = active_users
        return results_map

    @staticmethod
    def get_users_in_tutorial(
        start_date: date, end_date: date
    ) -> Dict[TutorialName, Dict[date, int]]:
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{GoogleAPI.property_id}",
            dimensions=[Dimension(name="date"), Dimension(name="fullPageUrl")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        results_map = {}
        for row in response.rows:
            sessions = int(row.metric_values[0].value)
            day = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            full_page_url = row.dimension_values[1].value
            if GoogleAPI.__is_tutorial_url(full_page_url):
                tutorial_name = GoogleAPI.__get_tutorial_name(full_page_url)
                if tutorial_name not in results_map:
                    results_map[tutorial_name] = {}
                results_map[tutorial_name][day] = sessions
        return results_map

    @staticmethod
    def __is_tutorial_url(url):
        return url.startswith("membrane.stream/learn/")

    @staticmethod
    def __get_tutorial_name(url):
        return url.split("/")[2]
