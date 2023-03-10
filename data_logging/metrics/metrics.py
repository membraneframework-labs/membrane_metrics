from datetime import date, datetime

from context.context import Context
from data_logging.mongodb.mongo import MongoTimeSeries


class Metrics:
    def __init__(self, context: Context) -> None:
        """
        Initialize / generate metrics.
        """
        pass

    def get_metric_series(self) -> list[MongoTimeSeries]:
        """
        Returns dict with metrics names as keys and 
        list of DataPoints representing metric value in different timestamps
        """

    @staticmethod
    def date_to_datetime(day: date) -> datetime:
        return datetime.combine(day, datetime.min.time())
