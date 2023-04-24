import dash
import dash_auth
from dash import Dash, html

from config.app_config import AppConfig

dash_app = Dash(__name__, use_pages=True)
dash_app.layout = html.Div([dash.page_container])
config = AppConfig()
auth = dash_auth.BasicAuth(dash_app, config.plots_config.get_authentication_dict())
server = dash_app.server

if __name__ == "__main__":
    dash_app.run(debug=True)
