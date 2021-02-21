import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from app_server import controller

layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("AÇÕES"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=controller.compare_havings_chart('Ação', 'periodo_cont'), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("BDRs"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=controller.compare_havings_chart('BDR', 'periodo_cont'), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("FIs"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=controller.compare_havings_chart('FI', 'periodo_cont'), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("FIIs"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=controller.compare_havings_chart('FII', 'periodo_cont'), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

])