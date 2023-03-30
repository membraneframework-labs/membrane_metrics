from datetime import date
from data_logging.metrics.metrics import Metrics
from config.app_config import AppConfig
from data_logging.time_series import TimeSeries, TimeSeriesEntry
from data_logging.metrics.hex.hex_api import HexAPI
from data_logging.mongodb.collection import MongoCollection


class HexMetrics(Metrics):
    organization_name: str = "membraneframework"

    def __init__(self, app_config: AppConfig):
        pass

    def get_metric_series(self) -> list[TimeSeries]:
        cumulative_downloads = _get_cumulative_downloads()
        current_date = date.today()
        entry = TimeSeriesEntry(current_date, cumulative_downloads)
        cumulative_downloads_time_seriee = TimeSeries(
            MongoCollection.HexCumulativePackagesDownloads, [entry]
        )
        return [cumulative_downloads_time_seriee]


def _get_cumulative_downloads() -> int:
    packages = HexAPI.get_user_owned_packages(HexMetrics.organization_name)
    cumulative_downloads = 0
    for package in packages:
        how_many_downloads = HexAPI.get_number_of_all_downloads(package)
        cumulative_downloads += how_many_downloads
    return cumulative_downloads
