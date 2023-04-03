from datetime import date
from data_logging.metrics.metrics import Metrics
from config.app_config import AppConfig
from data_logging.time_series import TimeSeries, TimeSeriesEntry
import data_logging.metrics.hex.hex_api as HexAPI
from data_logging.mongodb.collection import MongoCollection


class HexMetrics(Metrics):
    organization_name: str = "membraneframework"

    def __init__(self, app_config: AppConfig):
        cumulative_downloads = _get_cumulative_downloads()
        current_date = date.today()
        self.cumulative_downloads_entries = [
            TimeSeriesEntry(current_date, cumulative_downloads)
        ]

    def get_metric_series(self) -> list[TimeSeries]:
        return [
            TimeSeries(
                MongoCollection.HexCumulativePackagesDownloads,
                self.cumulative_downloads_entries,
            )
        ]


def _get_cumulative_downloads() -> int:
    packages = HexAPI.get_user_owned_packages(HexMetrics.organization_name)
    cumulative_downloads = 0
    for package in packages:
        how_many_downloads = HexAPI.get_number_of_all_downloads(package)
        cumulative_downloads += how_many_downloads
    return cumulative_downloads
