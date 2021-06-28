import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

ticker_list = ['MGLU3.SA', 'APPL', 'PETR4.SA', '^BVSP', 'GOLD11.SA']

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
        ], md=6)
    ], 
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