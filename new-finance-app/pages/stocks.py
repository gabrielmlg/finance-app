import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from app_server import services

df = services.resume

layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("CALENDARIO"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=services.compare_investiment('Ação', 'Data'), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

])