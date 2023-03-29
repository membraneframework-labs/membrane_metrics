from pymongo import MongoClient
from pymongo.database import Database

from config.app_config import AppConfig
from data_logging.time_series import TimeSeries


class MongoDB:
    client: MongoClient
    db: Database

    def __init__(self, config: AppConfig) -> None:
        database_name = 'Discord'
        self.client = MongoClient(config.mongodb_connection_url)
        self.db = self.client[database_name]

    def write_time_series(self, time_series: TimeSeries) -> None:
        db_collection = self.db[time_series.collection.name]
        collection_time_series = {
            (document['date'], document.get(time_series.collection.get_meta_field_name(), None)) for document in db_collection.find({})}
        filtered_time_series = TimeSeries(
            time_series.collection,
            list(filter(
                lambda data_point: (data_point.date, data_point.meta_field_value) not in collection_time_series, time_series.values))
        )
        to_insert = filtered_time_series.to_mongo_format()
        if len(to_insert) > 0:
            db_collection.insert_many(to_insert)
