import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from app_server import controller

df = controller.resume()

layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("COMPARATIVO"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=controller.compare_havings_chart('Ação'), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

])