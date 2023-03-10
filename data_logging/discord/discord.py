from context.context import Context
from data_logging.metrics.discord_metrics import DiscordMetrics
from data_logging.log_metrics import LogMetrics
from data_logging.mongodb.mongo import MongoDB


class LogDiscordMetrics(LogMetrics):
    @staticmethod
    def log(context: Context, db: MongoDB) -> None:
        discord_metrics = DiscordMetrics(context)
        for metric_series in discord_metrics.get_metric_series():
            db.write_time_series(metric_series)
