from config.app_config import AppConfig
from data_logging.metrics.discord.discord_metrics import DiscordMetrics
from data_logging.mongodb.mongo import MongoDB


def main():
    config = AppConfig()
    # Metrics collection
    discord_metrics = DiscordMetrics(config)

    # Creating db connection
    db = MongoDB(config)

    # Logging metrics to db
    all_discord_series = discord_metrics.get_metric_series()
    for single_discord_series in all_discord_series:
        db.write_time_series(single_discord_series)


if __name__ == '__main__':
    main()
