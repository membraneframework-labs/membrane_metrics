from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from data_logging.mongodb.mongo import MongoDB
from data_logging.mongodb.collection import MongoCollection
from config.app_config import AppConfig
from datetime import date, timedelta

HOW_MANY_DAYS=90

app = Dash(__name__)
server = app.server
config = AppConfig()
mongo = MongoDB(config)

all_collections = [e.value for e in MongoCollection]

app.layout = html.Div([
    html.H1(children='Membrane Community Metrics', style={'textAlign':'center'}),
    dcc.Dropdown(all_collections, value="GoogleUsersInTutorialPerDay", id="collection-selection", clearable=False),
    dcc.Dropdown(id='categories-selection', value=["Total"], clearable=False),
    dcc.Graph(id='graph-content')
])

def densify(df, collection):
    match collection:
        case MongoCollection.HexCumulativePackagesDownloads:
            pass
        case MongoCollection.DiscordMembersAtDay:
            pass
        case default:
            df.set_index("date",drop=True,inplace=True)
            df.index = pd.to_datetime(df.index)
            idx = pd.date_range(date.today()-timedelta(days=HOW_MANY_DAYS), date.today())
            #idx = pd.date_range(df.index.min(), df.index.max())
            df=df.reindex(idx)
            df[df[collection.get_value_field_name()].isnull()] = 0
            df['date']=df.index
    return df

@callback(
    Output('categories-selection', 'options'),
    Output('categories-selection', 'value'),
    Output('categories-selection', 'multi'),
    Output('categories-selection', 'disabled'),
    Input('collection-selection', 'value')
)
def update_checkbox(collection_str):
    collection = MongoCollection(collection_str)
    df = pd.DataFrame(mongo.get_collection(collection))
    if collection.get_meta_field_name() in df:
        options = ["Total"]+list(df[collection.get_meta_field_name()].unique())
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
    Output('graph-content', 'figure'),
    Input('categories-selection', 'value'),
    Input('collection-selection', 'value')
)
def update_graph(categories, collection_str):
    collection = MongoCollection(collection_str)
    dfs_to_display = []
    if not isinstance(categories, list):
        categories = [categories]
    for category in categories:
        if category == "Total":
            df_for_category = pd.DataFrame(mongo.get_collection(collection)).drop(["_id", collection.get_meta_field_name()], axis=1).groupby("date").sum().reset_index()
        elif category == "Value":
            df_for_category = pd.DataFrame(mongo.get_collection(collection))
        else:
            df_for_category = pd.DataFrame(mongo.get_collection(collection, {collection.get_meta_field_name(): category}))
        df_for_category = densify(df_for_category, collection)
        df_for_category[collection.get_meta_field_name()] = category
        dfs_to_display.append(df_for_category)
    final_df = pd.concat(dfs_to_display)
    return px.line(final_df, x='date', y=collection.get_value_field_name(), color=collection.get_meta_field_name())

if __name__ == '__main__':
    app.run_server(debug=True)