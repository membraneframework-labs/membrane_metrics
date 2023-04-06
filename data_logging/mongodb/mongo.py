from pymongo import MongoClient
from data_logging.mongodb.collection import MongoCollection
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

    def get_collection_with_query(self, collection: MongoCollection, query=""):
        results = [result for result in self.db[collection.name].find(query).sort("date", 1)]
        return results
        
        