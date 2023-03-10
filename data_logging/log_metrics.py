from context.context import Context
from data_logging.mongodb.mongo import MongoDB


class LogMetrics:
    def log(self, context: Context, db: MongoDB) -> None:
        """
        Logs metrics into database.
        """
