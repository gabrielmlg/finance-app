from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from datetime import datetime, date
import pandas as pd

from components import utils

ticker_list = ['MGLU3.SA', 'APPL', 'PETR4.SA', '^BVSP', 'GOLD11.SA']
dates = utils.rangeDateList('', '')
marks = {
    0: dates[0],
    365: dates[366],   
    len(dates)-1: dates[-1]
}
mytotaldates = {i: x for i,x in enumerate(dates)}
a = (list(mytotaldates.keys()))

layout = html.Div([
    
    dbc.Row([
        dbc.Col([
            html.Div(
                dcc.Dropdown(
                    id='ticker-selected',
                    options=[{'label': i, 'value': i} for i in ticker_list],
                    value='Ticker'
                ),
            ), 
        ], md=5)], 
        align='right', 
        justify='center'), 
    html.Br(),

    dbc.Row(
        dbc.Col(
            html.Div([
                dcc.RangeSlider(
                    id='periodRangeSliderId',
                    min=a[0],
                    max=a[-1],
                    marks=marks,
                    value=[a[0], a[-1]],
                    allowCross=False
                ),
                html.Div(id='OutputContainer')
            ]), 
            md=5
        ),
        align='right', 
        justify='center'), 
    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(id='ticker-graphic')
                )
            )
        ], lg=10, width={'offset': 1})
    ])

])