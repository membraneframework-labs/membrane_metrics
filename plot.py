from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from data_logging.mongodb.mongo import MongoDB
from data_logging.mongodb.collection import MongoCollection
from config.app_config import AppConfig
from datetime import date, timedelta

HOW_MANY_DAYS=90

app = Dash(__name__)
config = AppConfig()
mongo = MongoDB(config)

all_collections = [e.value for e in MongoCollection]

collection = None
df = None

app.layout = html.Div([
    html.H1(children='Membrane Community Metrics', style={'textAlign':'center'}),
    dcc.Dropdown(all_collections, value="GoogleUniqueUsersInTutorialPerDay", id="collection-selection", clearable=False),
    dcc.Dropdown(id='categories-selection', value=["Total"], clearable=False),
    dcc.Graph(id='graph-content')
])

def fill_none_value(df, collection):
    match collection:
        case MongoCollection.HexCumulativePackagesDownloads:
            df = df.dropna()
        case MongoCollection.DiscordMembersAtDay:
            df = df.dropna()
        case default:
            df[df[collection.get_value_field_name()].isnull()] = 0
    return df

@callback(
    Output('categories-selection', 'options'),
    Output('categories-selection', 'value'),
    Output('categories-selection', 'multi'),
    Output('categories-selection', 'disabled'),
    Input('collection-selection', 'value')
)
def update_checkbox(collection_str):
    global collection
    collection = MongoCollection(collection_str)
    global df
    df = pd.DataFrame(mongo.get(collection))
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
    Input('categories-selection', 'value')
)
def update_graph(categories):
    dffs = []
    if not isinstance(categories, list):
        categories = [categories]
    for value in categories:
        if value == "Total":
            dff = df.groupby("date").sum().reset_index()
        elif value == "Value":
            dff = df
        else:
            dff = df[df[collection.get_meta_field_name()]==value]
        dff.set_index("date",drop=True,inplace=True)
        dff.index = pd.to_datetime(dff.index)
        idx = pd.date_range(date.today()-timedelta(days=HOW_MANY_DAYS), date.today())
        #idx = pd.date_range(dff.index.min(), dff.index.max())
        dff=dff.reindex(idx)
        dff = fill_none_value(dff, collection)
        print(dff)
        dff['date']=dff.index
        dff[collection.get_meta_field_name()] = value
        dffs.append(dff)
    final_dff = pd.concat(dffs)
    return px.line(final_dff, x='date', y=collection.get_value_field_name(), color=collection.get_meta_field_name())

if __name__ == '__main__':
    app.run_server(debug=True)

