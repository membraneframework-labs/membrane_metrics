import dash

from config.app_config import AppConfig
from data_logging.mongodb.mongo import MongoDB
from pages.common import prepare_static_layout

PLOTS_TO_DISPLAY = {
    "DiscordMembersAtDay": ["Value"],
    "DiscordMessagesPerDayPerChannel": ["Total", "🙋help", "📋general"],
}

config = AppConfig()
mongo = MongoDB(config)

dash.register_page(__name__, path="/discord/")

layout = prepare_static_layout(PLOTS_TO_DISPLAY, mongo)
