from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from data_logging.mongodb.collection import MongoCollection


@dataclass
class MongoTimeSeriesEntry:
    date: datetime
    value: float
    meta_field_value: Optional[str]

    def __init__(self, date: datetime, value: float, meta_filed_value: Optional[str] = None):
        self.date = date
        self.value = value
        self.meta_field_value = meta_filed_value


@dataclass
class MongoTimeSeries:
    collection: MongoCollection
    values: list[MongoTimeSeriesEntry]

    def __init__(self, collection_name: MongoCollection, values: list[MongoTimeSeriesEntry]) -> None:
        self.collection = collection_name
        self.values = values

    def to_mongo_format(self) -> list[dict]:
        data_points = []
        for entry in self.values:
            data_point = {"date": entry.date,
                          self.collection.get_value_field_name(): entry.value}
            if entry.meta_field_value is not None:
                data_point[self.collection.get_meta_field_name()] = entry.meta_field_value
            data_points.append(data_point)

        return data_points
