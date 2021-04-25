import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_html_components.Br import Br
from dash_table import DataTable, FormatTemplate

from app_server import app
from app_server import main_service


money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

df = main_service.resume

# teste
df3 = df[(df['periodo_cont'] > 0)].sort_values(['Tipo', 'Data'])
df3 = df3\
    .groupby(['Tipo'])\
    .agg(financeiro=('Financeiro', 'sum'), 
        aporte=('aporte', 'sum'), 
        retirada=('retirada', 'sum'), 
        rendimento=('rendimento', 'sum'))\
    .reset_index()
#df3['teste'] = (df3['aporte'].cumsum() - df3['retirada'].cumsum())
df3['%'] = df3['rendimento'] / (df3['financeiro'] - df3['retirada']) * 100
df3.fillna(0, inplace=True)

df_resume = df3

cols_resume = [
    dict(id='Tipo', name='Tipo'),
    dict(id='financeiro', name='Posição atual', type='numeric', format=money),
    dict(id='aporte', name='Aporte', type='numeric', format=money),
    dict(id='retirada', name='Retirada', type='numeric', format=money),
    dict(id='rendimento', name='Rendimento', type='numeric', format=money),
    dict(id='%', name='%', type='numeric', format=percentage)
]

#df3 = controller.acoes.dividendo 
#df4 = controller.fiis.dividendo

layout = html.Div([

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("RENDIMENTO"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=main_service.timeline_by_type_relative_chart(), config={'displayModeBar': False}),
                )
            ]), 
            lg=5, width={'offset': 1}
        ), 
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("RENDIMENTO ACUMULADO"),    
                dbc.CardBody(
                    dcc.Graph(id="revenue_by_month_chart", figure=main_service.timeline_by_types_chart(), config={'displayModeBar': False}),
                )
            ]), 
            lg=5
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("RESUMO"),    
                dbc.CardBody(
                    html.Div(

                        DataTable(
                            id='table',
                            columns=cols_resume, #[{"name": i, "id": i} for i in df2.columns],
                            data=df_resume.to_dict('records'),
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Tipo', 'Nome']
                            ],
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                            style_as_list_view=True,
                        )

                    )
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

])