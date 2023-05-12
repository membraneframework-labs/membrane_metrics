from datetime import date, timedelta

import pandas as pd
import plotly.express as px
from dash import dcc, html
from plotly.graph_objects import Figure

from data_logging.mongodb.collection import MongoCollection
from data_logging.mongodb.mongo import MongoDB

DEFAULT_DATE_RANGE: int = 90  # days
DENSIFY_UP_TO: int = 1080  # days
WINDOWS_SIZE: int = 7  # days
DATE_FORMAT: str = "%Y-%m-%d"


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


def update_graph(
    metric_subcategories: list[str], metric_type: str, mongo: MongoDB
) -> Figure:
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

    yesterday =  date.today() - timedelta(days=1)
    daterange_start = yesterday.strftime(DATE_FORMAT)
    daterange_end = (yesterday - timedelta(days=DEFAULT_DATE_RANGE)).strftime(
        DATE_FORMAT
    )

    return px.line(
        final_df,
        x="date",
        y=collection.get_value_field_name(),
        color=collection.get_meta_field_name(),
    ).update_layout(xaxis_range=[daterange_end, daterange_start])


def prepare_static_layout(
    plots_to_display: dict[str, list[str]], mongo: MongoDB, class_name: str
) -> html.Div:
    children = []
    for collection_name in plots_to_display.keys():
        collection = MongoCollection(collection_name)
        (graph_div,) = (
            html.Div(
                className=class_name,
                children=[
                    html.H2(
                        children=collection.get_friendly_name(),
                        style={"text-align": "center"},
                    ),
                    dcc.Graph(
                        figure=update_graph(
                            plots_to_display[collection_name], collection_name, mongo
                        )
                    ),
                ],
            ),
        )
        children.append(graph_div)
    return html.Div(children)
