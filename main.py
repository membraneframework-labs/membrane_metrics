from config.app_config import AppConfig
from data_logging.metrics.discord.discord_metrics import DiscordMetrics
from data_logging.metrics.twitter.twitter_metrics import TwitterMetrics
from data_logging.mongodb.mongo import MongoDB

def main():
    config = AppConfig()
    # Metrics collection
    metrics = [
        DiscordMetrics(config),
        TwitterMetrics(config)
    ]
    # Creating db connection
    db = MongoDB(config)

    # Logging metrics to db
    for metric in metrics:
        all_series = metric.get_metric_series()
        for single_seriee in all_series:
            db.write_time_series(single_seriee)


if __name__ == '__main__':
    main()
