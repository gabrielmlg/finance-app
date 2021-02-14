import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_html_components.Br import Br
import dash_table

from app_server import app
from app_server import controller

df = controller.resume()

df2 = df.groupby(['Tipo', 'Nome'])\
    .agg(financeiro=('financeiro', 'last'), 
        aporte=('aporte', 'sum'), 
        retirada=('retirada', 'sum'), 
        rendimento=('rendimento', 'sum'))\
        .reset_index()

df2['%'] = df2['rendimento'] / df2['aporte'] * 100

layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody(
                    html.Div(

                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in df2.columns],
                            data=df2.to_dict('records'),
                        )

                    )
                )
            ])
        )
    ]), 
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody(
                    html.Div(

                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=df.to_dict('records'),
                        )

                    )
                )
            ])
        )
    ])
])