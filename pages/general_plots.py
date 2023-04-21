import pandas as pd
from dash import MATCH, Input, Output, callback, dcc, html
from plotly.graph_objects import Figure
import dash
# import sys
# import os
# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)
from config.app_config import AppConfig
from data_logging.mongodb.collection import MongoCollection
from data_logging.mongodb.mongo import MongoDB
from plots import update_graph

ALL_METRIC_TYPES = ["Discord", "Google Analytics", "Hex"]

config = AppConfig()
mongo = MongoDB(config)
dash.register_page(__name__, path="/interactive/")
layout = html.Div(
    [
        html.H1(children="Membrane Community Metrics", style={"textAlign": "center"}),
        dcc.Dropdown(
            ALL_METRIC_TYPES,
            value="Discord",
            id="metric-type-selection",
            clearable=False,
            style={"background-color": "#87CCE8"},
        ),
        html.Div([]),
        html.Div([], id="graphs-div"),
    ]
)


@callback(Output("graphs-div", "children"), Input("metric-type-selection", "value"))
def update_div(metric_type: str) -> list[dcc]:
    collections = _get_collections_for_metric_type(metric_type)
    div_children = []
    for i, collection in enumerate(collections):
        div_children.append(_get_graph_div_for_collection(collection, i))
    return div_children



@callback(
    Output({"type": "metric-subcategory-selection", "index": MATCH}, "options"),
    Output({"type": "metric-subcategory-selection", "index": MATCH}, "value"),
    Output({"type": "metric-subcategory-selection", "index": MATCH}, "multi"),
    Output({"type": "metric-subcategory-selection", "index": MATCH}, "disabled"),
    Output({"type": "metric-subcategory-selection", "index": MATCH}, "style"),
    Input({"type": "metric-collection-name", "index": MATCH}, "children"),
)
def update_dropdown(metric_type: str) -> tuple[list[str], str, bool, bool, dict]:
    collection = MongoCollection(metric_type)
    df = pd.DataFrame(mongo.get_collection(collection))
    if collection.get_meta_field_name() in df:
        options = ["Total"] + list(df[collection.get_meta_field_name()].unique())
        value = _get_default_subcategory(collection)
        multi = True
        disabled = False
        style = {}
    else:
        options = ["Value"]
        value = "Value"
        multi = False
        disabled = True
        style = {"visibility": "hidden"}

    return options, value, multi, disabled, style


@callback(
    Output({"type": "graph-content", "index": MATCH}, "figure"),
    Input({"type": "metric-subcategory-selection", "index": MATCH}, "value"),
    Input({"type": "metric-collection-name", "index": MATCH}, "children"),
)
def update_graph_wrapper(metric_subcategories: list[str], metric_type: str) -> Figure:
    return update_graph(metric_subcategories, metric_type)


def _get_collections_for_metric_type(metric_type: str) -> MongoCollection:
    match metric_type:
        case "Discord":
            return [
                MongoCollection.DiscordMembersAtDay,
                MongoCollection.DiscordMessagesPerDayPerChannel,
            ]
        case "Hex":
            return [MongoCollection.HexCumulativePackagesDownloads]
        case "Google Analytics":
            return [
                MongoCollection.GoogleBounceRatePerDay,
                MongoCollection.GoogleTimeSpentPerDay,
                MongoCollection.GoogleUsersFromTrafficSourcePerDay,
                MongoCollection.GoogleUsersInTutorialPerDay,
            ]


def _get_default_subcategory(collection) -> list[str]:
    match collection:
        case MongoCollection.DiscordMessagesPerDayPerChannel:
            return ["Total", "🙋help", "📋general"]
        case MongoCollection.GoogleUsersFromTrafficSourcePerDay:
            return ["Total", "(direct)", "google", "t.co", "github.com"]
        case default:
            return ["Total"]


def _get_graph_div_for_collection(collection: MongoCollection, i: int) -> dcc:
    return html.Div(
        children=[
            html.Div(
                id={"type": "metric-collection-name", "index": i},
                children=collection.name,
                style={"display": "None"},
            ),
            html.Div(
                children=[
                    html.H2(
                        children=collection.get_friendly_name(),
                        style={"float": "left", "width": "50%", "margin-left": "10px"},
                    ),
                    dcc.Loading(
                        children=[
                            dcc.Dropdown(
                                id={"type": "metric-subcategory-selection", "index": i},
                                value=["Total"],
                                clearable=False,
                                style={"width": "97%", "margin-left": "5px"},
                            )
                        ]
                    ),
                ]
            ),
            dcc.Loading(
                children=[
                    dcc.Graph(
                        id={"type": "graph-content", "index": i},
                        config={"showAxisRangeEntryBoxes": True},
                    )
                ]
            ),
        ],
        style={"border-style": "solid"},
    )
