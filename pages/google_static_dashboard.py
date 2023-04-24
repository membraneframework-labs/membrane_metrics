import dash

from config.app_config import AppConfig
from data_logging.mongodb.mongo import MongoDB
from pages.common import prepare_static_layout

PLOTS_TO_DISPLAY = {
    "GoogleTimeSpentPerDay": ["Value"],
    "GoogleUsersInTutorialPerDay": ["Total"],
    "GoogleBounceRatePerDay": ["Value"],
    "GoogleUsersFromTrafficSourcePerDay": ["Total"],
}

config = AppConfig()
mongo = MongoDB(config)

dash.register_page(__name__, path="/google/")

layout = prepare_static_layout(PLOTS_TO_DISPLAY, mongo, "box")
