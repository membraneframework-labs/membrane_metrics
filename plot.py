from datetime import date, timedelta

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure
from dash import Dash, Input, Output, callback, dcc, html

from config.app_config import AppConfig
from data_logging.mongodb.collection import MongoCollection
from data_logging.mongodb.mongo import MongoDB

HOW_MANY_DAYS_BACK = 90

app = Dash(__name__)
server = app.server
config = AppConfig()
mongo = MongoDB(config)

all_metric_types = [e.value for e in MongoCollection]

app.layout = html.Div(
    [
        html.H1(children="Membrane Community Metrics", style={"textAlign": "center"}),
        dcc.Dropdown(
            all_metric_types,
            value="GoogleUsersInTutorialPerDay",
            id="metric-type-selection",
            clearable=False,
        ),
        dcc.Dropdown(
            id="metric-subcategory-selection", value=["Total"], clearable=False
        ),
        dcc.Graph(id="graph-content"),
    ]
)


def _densify(df: pd.DataFrame, collection: MongoCollection) -> pd.DataFrame:
    match collection:
        case MongoCollection.HexCumulativePackagesDownloads:
            pass
        case MongoCollection.DiscordMembersAtDay:
            pass
        case default:
            df.set_index("date", drop=True, inplace=True)
            df.index = pd.to_datetime(df.index)
            idx = pd.date_range(
                date.today() - timedelta(days=HOW_MANY_DAYS_BACK), date.today()
            )
            df = df.reindex(idx)
            df[df[collection.get_value_field_name()].isnull()] = 0
            df["date"] = df.index
    return df


@callback(
    Output("metric-subcategory-selection", "options"),
    Output("metric-subcategory-selection", "value"),
    Output("metric-subcategory-selection", "multi"),
    Output("metric-subcategory-selection", "disabled"),
    Input("metric-type-selection", "value"),
)
def update_checkbox(metric_type: str) -> tuple[list[str], str, bool, bool]:
    collection = MongoCollection(metric_type)
    df = pd.DataFrame(mongo.get_collection(collection))
    if collection.get_meta_field_name() in df:
        options = ["Total"] + list(df[collection.get_meta_field_name()].unique())
        value = [options[0]]
        multi = True
        disabled = False
    else:
        options = ["Value"]
        value = "Value"
        multi = False
        disabled = True

    return options, value, multi, disabled


@callback(
    Output("graph-content", "figure"),
    Input("metric-subcategory-selection", "value"),
    Input("metric-type-selection", "value"),
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
        df_for_subcategory = _densify(df_for_subcategory, collection)
        df_for_subcategory[collection.get_meta_field_name()] = subcategory
        dfs_to_display.append(df_for_subcategory)
    final_df = pd.concat(dfs_to_display)
    return px.line(
        final_df,
        x="date",
        y=collection.get_value_field_name(),
        color=collection.get_meta_field_name(),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
