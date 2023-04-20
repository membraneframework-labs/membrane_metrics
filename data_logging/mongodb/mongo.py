from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from config.app_config import AppConfig
from data_logging.time_series import TimeSeries
from data_logging.mongodb.collection import MongoCollection

DATABASE_NAME = 'Discord'


class MongoDB:
    def __init__(self, config: AppConfig) -> None:
        self.client: MongoClient = MongoClient(config.mongodb_connection_url)
        self.db: Database = self.client[DATABASE_NAME]

    def write_time_series(self, time_series: TimeSeries) -> None:
        db_collection = self.db[time_series.collection.name]

        time_series.filter_default_value()
        filtered_time_series = MongoDB.__filter_previously_logged_entries(time_series, db_collection)

        to_insert = filtered_time_series.to_mongo_format()
        if len(to_insert) > 0:
            db_collection.insert_many(to_insert)

    def get_collection(self, collection: MongoCollection, query={}):
        db_collection = self.db[collection.name]
        return db_collection.find(query).sort("date", 1)

    @staticmethod
    def __filter_previously_logged_entries(time_series: TimeSeries, db_collection: Collection) -> TimeSeries:
        previously_logged_entries = {
            (document['date'], document.get(time_series.collection.get_meta_field_name(), None))
            for document in db_collection.find({})}

        return TimeSeries(
            time_series.collection,
            list(filter(lambda entry: (entry.date, entry.meta_field_value) not in previously_logged_entries,
                        time_series.entries))
        )
