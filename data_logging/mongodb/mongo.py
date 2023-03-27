from pymongo import MongoClient
from pymongo.database import Database

from context.context import Context
from data_logging.time_series import TimeSeries
from dataclasses import dataclass


@dataclass
class MongoDB:
    client: MongoClient
    db: Database

    def __init__(self, context: Context) -> None:
        database_name = 'Discord'
        self.client = MongoClient(context.mongodb_connection_url)
        self.db = self.client[database_name]

    def write_time_series(self, time_series: TimeSeries) -> None:
        collection = self.db[time_series.collection.name]
        collection_time_stamps = {
            document['date'] for document in collection.find({})}
        filtered_time_series = TimeSeries(
            time_series.collection,
            list(filter(
                lambda data_point: data_point.date not in collection_time_stamps, time_series.values))
        )
        to_insert = filtered_time_series.to_mongo_format()
        if len(to_insert) > 0:
            collection.insert_many(to_insert)
