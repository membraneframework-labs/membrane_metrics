from itertools import chain

from config.app_config import AppConfig
from data_logging.metrics.discord.discord_metrics import DiscordMetrics
from data_logging.metrics.metrics import Metrics
from data_logging.metrics.hex.hex_metrics import HexMetrics
from data_logging.mongodb.mongo import MongoDB


def main():
    config = AppConfig()
    # Metrics collection
    source_metrics: list[Metrics] = [DiscordMetrics(config), HexMetrics(config)]

    # Creating db connection
    db = MongoDB(config)

    # Logging metrics to db
    metrics_time_series = list(chain(*[metrics.get_metric_series() for metrics in source_metrics]))
    for single_series in metrics_time_series:
        db.write_time_series(single_series)


if __name__ == "__main__":
    main()
