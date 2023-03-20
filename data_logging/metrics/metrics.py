from datetime import date, datetime

from context.context import Context
from data_logging.mongodb.mongo import TimeSeries


class Metrics:
    def __init__(self, context: Context) -> None:
        """
        Initialize / generate metrics.
        """
        pass

    def get_metric_series(self) -> list[TimeSeries]:
        """
        Returns metrics in TimeSeries format
        """
    
