import dash
import dash_bootstrap_components as dbc
from components.services import MainService

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.MATERIA], 
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

main_service = MainService()