import dash
from dash import dcc, html

from config.app_config import AppConfig
from data_logging.mongodb.collection import MongoCollection
from data_logging.mongodb.mongo import MongoDB
from pages.common import update_graph

PLOTS_TO_DISPLAY = {
    "DiscordMembersAtDay": ["Value"],
    "DiscordMessagesPerDayPerChannel": ["Total"],
    "GoogleBounceRatePerDay": ["Value"],
    "HexCumulativePackagesDownloads": ["Value"],
}

config = AppConfig()
mongo = MongoDB(config)

dash.register_page(__name__, path="/screen/")


def _prepare_layout():
    children = []
    for collection_name in PLOTS_TO_DISPLAY.keys():
        collection = MongoCollection(collection_name)
        (graph_div,) = (
            html.Div(
                className="box",
                children=[
                    html.H2(
                        children=collection.get_friendly_name(),
                        style={"text-align": "center"},
                    ),
                    dcc.Graph(
                        figure=update_graph(
                            PLOTS_TO_DISPLAY[collection_name], collection_name, mongo
                        )
                    ),
                ],
            ),
        )
        children.append(graph_div)
    return html.Div(children)


layout = _prepare_layout()
