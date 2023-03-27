from abc import abstractmethod

from config.app_config import AppConfig
from data_logging.mongodb.mongo import TimeSeries


class Metrics:
    @abstractmethod
    def __init__(self, config: AppConfig) -> None:
        """
        Initialize / generate metrics.
        """
        pass

    @abstractmethod
    def get_metric_series(self) -> list[TimeSeries]:
        """
        Returns metrics in TimeSeries format
        """
