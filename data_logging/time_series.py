from dataclasses import dataclass
from datetime import date as datetime_date
from datetime import datetime
from typing import Optional

from data_logging.mongodb.collection import MongoCollection


def date_to_datetime(day: datetime_date) -> datetime:
    return datetime.combine(day, datetime.min.time())


@dataclass
class TimeSeriesEntry:
    date: datetime
    value: float
    meta_field_value: Optional[str]

    def __init__(self, date: datetime or datetime_date, value: float, meta_filed_value: Optional[str] = None):
        if isinstance(date, datetime_date):
            self.date = date_to_datetime(date)
        else:
            self.date = date
        self.value = value
        self.meta_field_value = meta_filed_value


@dataclass
class TimeSeries:
    collection: MongoCollection
    values: list[TimeSeriesEntry]

    def to_mongo_format(self) -> list[dict]:
        data_points = []
        for entry in self.values:
            data_point = {"date": entry.date,
                          self.collection.get_value_field_name(): entry.value}
            if entry.meta_field_value is not None:
                data_point[self.collection.get_meta_field_name()
                ] = entry.meta_field_value
            data_points.append(data_point)

        return data_points
