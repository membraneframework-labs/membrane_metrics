from data_logging.mongodb.collection import MongoCollection
from data_logging.mongodb.mongo import MongoDB
from plotly.graph_objects import Figure
import pandas as pd
from datetime import date, timedelta
import plotly.express as px
from dash import Dash
from config.app_config import AppConfig
import dash_auth
import dash
from dash import html

DEFAULT_DATE_RANGE: int = 90  # days
DENSIFY_UP_TO: int = 1080  # days
WINDOWS_SIZE: int = 7  # days
DATE_FORMAT: str = "%Y-%m-%d"

config = AppConfig()
mongo = MongoDB(config)

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


if __name__ == "__main__":
    dash_app = Dash(__name__, use_pages=True)
    dash_app.layout = html.Div([
        dash.page_container
    ])
    config = AppConfig()
    mongo = MongoDB(config)
    auth = dash_auth.BasicAuth(dash_app, config.plots_config.get_authentication_dict())
    server = dash_app.server

    dash_app.run(debug=True)