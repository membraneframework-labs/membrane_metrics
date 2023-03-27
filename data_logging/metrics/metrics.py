from abc import abstractmethod

from context.context import Context
from data_logging.mongodb.mongo import TimeSeries


class Metrics:
    @abstractmethod
    def __init__(self, context: Context) -> None:
        """
        Initialize / generate metrics.
        """
        pass

    @abstractmethod
    def get_metric_series(self) -> list[TimeSeries]:
        """
        Returns metrics in TimeSeries format
        """
