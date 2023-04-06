from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from datetime import date, datetime
from typing import Dict, List, NewType

PropertyId = NewType("PropertyID", str)
TrafficSource = NewType("TrafficSource", str)
TutorialName = NewType("TutorialName", str)


class GoogleAPI:
    request_date_format: str = "%Y-%m-%d"
    response_date_format: str = "%Y%m%d"

    @staticmethod
    def get_total_time_spent(
        property_id: PropertyId, start_date: date, end_date: date
    ) -> Dict[date, float]:
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="averageSessionDuration"), Metric(name="sessions")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        date_result_map = {}
        for row in response.rows:
            average_session_duration = float(row.metric_values[0].value)
            sessions = int(row.metric_values[1].value)
            all_sessions_duration = avarage_session_duration * sessions  # in seconds
            date = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            date_result_map[date] = all_sessions_duration
        return date_result_map

    @staticmethod
    def get_bounce_rate(
        property_id: PropertyId, start_date: date, end_date: date
    ) -> Dict[date, float]:
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="bounceRate")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        date_result_map = {}
        for row in response.rows:
            bounce_rate = float(row.metric_values[0].value)
            date = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            date_result_map[date] = bounce_rate
        return date_result_map

    @staticmethod
    def get_users_source(
        property_id, start_date: date, end_date: date
    ) -> Dict[TrafficSource, Dict[date, int]]:
        results_map = {}
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date"), Dimension(name="firstUserSource")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        for row in response.rows:
            active_users = int(row.metric_values[0].value)
            date = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            source = row.dimension_values[1].value
            if source not in results_map:
                results_map[source] = {}
            results_map[source][date] = active_users
        return results_map

    @staticmethod
    def get_unique_users_in_tutorial(
        property_id: PropertyId, start_date: date, end_date: date
    ) -> Dict[TutorialName, Dict[date, int]]:
        client = BetaAnalyticsDataClient()
        start_date_str = start_date.strftime(GoogleAPI.request_date_format)
        end_date_str = end_date.strftime(GoogleAPI.request_date_format)
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date"), Dimension(name="fullPageUrl")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[DateRange(start_date=start_date_str, end_date=end_date_str)],
        )
        response = client.run_report(request)
        results_map = {}
        for row in response.rows:
            sessions = int(row.metric_values[0].value)
            date = datetime.strptime(
                row.dimension_values[0].value, GoogleAPI.response_date_format
            ).date()
            full_page_url = row.dimension_values[1].value
            if full_page_url.startswith("membrane.stream/learn/"):
                tutorial_name = full_page_url.split("/")[2]
                if tutorial_name not in results_map:
                    results_map[tutorial_name] = {}
                results_map[tutorial_name][date] = sessions
        return results_map
