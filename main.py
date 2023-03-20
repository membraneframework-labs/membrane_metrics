from context.context import Context
from data_logging.metrics.discord.discord_metrics import DiscordMetrics


def main():
    context = Context()
    discord_metrics = DiscordMetrics(context)
    # db = MongoDB(context)


if __name__ == '__main__':
    main()
