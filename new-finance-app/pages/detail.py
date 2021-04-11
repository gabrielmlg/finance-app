import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_html_components.Br import Br
from dash_table import DataTable, FormatTemplate

from app_server import app
from app_server import services

df = services.resume

# teste
df3 = df[(df['periodo_cont'] > 0)].sort_values(['Tipo', 'Data'])
df3 = df3\
    .groupby(['Tipo', 'Data'])\
    .agg(financeiro=('Financeiro', 'sum'), 
        aporte=('aporte', 'sum'), 
        retirada=('retirada', 'sum'), 
        rendimento=('rendimento', 'sum'))\
    .reset_index()
df3['teste'] = (df3['aporte'].cumsum() - df3['retirada'].cumsum())
df3['%'] = df3['rendimento'] / (df3['financeiro'] - df3['retirada']) * 100
df3.fillna(0, inplace=True)

#df3 = controller.acoes.dividendo 
#df4 = controller.fiis.dividendo

layout = html.Div([

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("RENDIMENTO"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=services.revenue_timeline_chart(), config={'displayModeBar': False}),
                )
            ]), 
            lg=5, width={'offset': 1}
        ), 
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("RENDIMENTO ACUMULADO"),    
                dbc.CardBody(
                    dcc.Graph(id="revenue_by_month_chart", figure=services.timeline_by_types_chart(), config={'displayModeBar': False}),
                )
            ]), 
            lg=5
        )
    ]),
    html.Br(),

])
