from context.context import Context
from data_logging.discord.discord import LogDiscordMetrics
from data_logging.mongodb.mongo import MongoDB


def main():
    context = Context()
    db = MongoDB(context)
    LogDiscordMetrics.log(context, db)


if __name__ == '__main__':
    main()
