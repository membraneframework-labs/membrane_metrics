import dash
import dash_auth
from dash import Dash, html

from config.app_config import AppConfig


# Monkey patch basic auth to work on non-index pages
def basic_auth_wrapper(basic_auth, func):
    """Updated auth wrapper to work on all pages rather than just index"""

    def wrap(*args, **kwargs):
        if basic_auth.is_authorized():
            return func(*args, **kwargs)
        return basic_auth.login_request()

    return wrap


dash_auth.BasicAuth.auth_wrapper = basic_auth_wrapper

dash_app = Dash(__name__, use_pages=True)
dash_app.layout = html.Div([dash.page_container])
config = AppConfig()
auth = dash_auth.BasicAuth(dash_app, config.plots_config.get_authentication_dict())
server = dash_app.server

if __name__ == "__main__":
    dash_app.run(debug=True)
