from datetime import date, timedelta

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from dash import Dash, Input, Output, callback, dcc, html, MATCH

from config.app_config import AppConfig
from data_logging.mongodb.collection import MongoCollection
from data_logging.mongodb.mongo import MongoDB


DEFAULT_DATE_RANGE: int = 90  # days
DENSIFY_UP_TO: int = 360  # days
WINDOWS_SIZE: int = 30  # days
DATE_FORMAT: str = "%Y-%m-%d"
ALL_METRIC_TYPES = ["Discord", "Hex", "Google Analytics"]

app = Dash(__name__)
server = app.server
config = AppConfig()
mongo = MongoDB(config)
app.layout = html.Div(
    [
        html.H1(children="Membrane Community Metrics", style={"textAlign": "center"}),
        dcc.Dropdown(
            ALL_METRIC_TYPES,
            value="Discord",
            id="metric-type-selection",
            clearable=False,
            style={"background-color": "#C0C0F0"},
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
    Input({"type": "metric-collection-name", "index": MATCH}, "children"),
)
def update_dropdown(metric_type: str) -> tuple[list[str], str, bool, bool]:
    collection = MongoCollection(metric_type)
    df = pd.DataFrame(mongo.get_collection(collection))
    if collection.get_meta_field_name() in df:
        options = ["Total"] + list(df[collection.get_meta_field_name()].unique())
        value = _get_default_subcategory(collection)
        multi = True
        disabled = False
    else:
        options = ["Value"]
        value = "Value"
        multi = False
        disabled = True

    return options, value, multi, disabled


@callback(
    Output({"type": "graph-content", "index": MATCH}, "figure"),
    Input({"type": "metric-subcategory-selection", "index": MATCH}, "value"),
    Input({"type": "metric-collection-name", "index": MATCH}, "children"),
)
def update_graph(metric_subcategories: list[str], metric_type: str) -> Figure:
    collection = MongoCollection(metric_type)
    dfs_to_display = []
    if not isinstance(metric_subcategories, list):
        metric_subcategories = [metric_subcategories]
    for subcategory in metric_subcategories:
        if subcategory == "Total":
            df_for_subcategory = (
                pd.DataFrame(mongo.get_collection(collection))
                .drop(["_id", collection.get_meta_field_name()], axis=1)
                .groupby("date")
                .sum()
                .reset_index()
            )
        elif subcategory == "Value":
            df_for_subcategory = pd.DataFrame(mongo.get_collection(collection))
        else:
            df_for_subcategory = pd.DataFrame(
                mongo.get_collection(
                    collection, {collection.get_meta_field_name(): subcategory}
                )
            )
        df_for_subcategory = _densify(df_for_subcategory, collection, DENSIFY_UP_TO)
        df_for_subcategory[collection.get_meta_field_name()] = subcategory
        dfs_to_display.append(df_for_subcategory)
    final_df = pd.concat(dfs_to_display)

    daterange_start = date.today().strftime(DATE_FORMAT)
    daterange_end = (date.today() - timedelta(days=DEFAULT_DATE_RANGE)).strftime(
        DATE_FORMAT
    )

    return px.line(
        final_df,
        x="date",
        y=collection.get_value_field_name(),
        color=collection.get_meta_field_name(),
    ).update_layout(xaxis_range=[daterange_end, daterange_start])


def _transform(df: pd.DataFrame, collection: MongoCollection) -> pd.DataFrame:
    match collection:
        case MongoCollection.GoogleBounceRatePerDay:
            df[collection.get_value_field_name()] = (
                df.drop(["_id", "date"], axis=1).rolling(window=WINDOWS_SIZE).mean()
            )
    return df


def _densify(
    df: pd.DataFrame, collection: MongoCollection, how_many_days_back: int
) -> pd.DataFrame:
    match collection:
        case MongoCollection.HexCumulativePackagesDownloads:
            pass
        case MongoCollection.DiscordMembersAtDay:
            pass
        case default:
            df.set_index("date", drop=True, inplace=True)
            df.index = pd.to_datetime(df.index)
            idx = pd.date_range(
                date.today() - timedelta(days=how_many_days_back), date.today()
            )
            df = df.reindex(idx)
            df[df[collection.get_value_field_name()].isnull()] = 0
            df["date"] = df.index
            df = _transform(df, collection)
    return df


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


if __name__ == "__main__":
    app.run_server(debug=True)
