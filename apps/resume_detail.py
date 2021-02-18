import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_html_components.Br import Br
from dash_table import DataTable, FormatTemplate

from app_server import app
from app_server import controller

import numpy as np

df = controller.resume()

# teste
df3 = df[(df['periodo_cont'] > 0)].sort_values(['Tipo', 'Data'])
df3 = df3\
    .groupby(['Tipo', 'Data'])\
    .agg(financeiro=('financeiro', 'sum'), 
        aporte=('aporte', 'sum'), 
        retirada=('retirada', 'sum'), 
        rendimento=('rendimento', 'sum'))\
    .reset_index()
df3['teste'] = (df3['aporte'].cumsum() - df3['retirada'].cumsum())
df3['%'] = df3['rendimento'] / (df3['financeiro'] - df3['retirada']) * 100
df3.fillna(0, inplace=True)

df3 = controller.acoes.dividendo 
df4 = controller.fiis.dividendo

#df3 = controller.acoes.dividendo.groupby(['Papel', 'Tipo']).agg(Valor=('Valor', 'sum')).reset_index().sort_values('Papel')
#df4 = controller.fiis.dividendo.groupby('Descricao').agg(Valor=('Valor', 'sum')).reset_index().sort_values('Valor', ascending=False)

#df3 = df[df['periodo_cont'] > 0].sort_values(['Tipo', 'Nome', 'periodo_cont'])

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

df_resume = df.groupby(['Tipo', 'Nome'])\
    .agg(financeiro=('financeiro', 'last'), 
        aporte=('aporte', 'sum'), 
        retirada=('retirada', 'sum'), 
        rendimento=('rendimento', 'sum'))\
        .reset_index()\
    .groupby('Tipo')\
        .agg(financeiro=('financeiro', 'sum'), 
            aporte=('aporte', 'sum'), 
            retirada=('retirada', 'sum'), 
            rendimento=('rendimento', 'sum'))\
            .reset_index()\
            .sort_values('financeiro', ascending=False)
df_resume['%'] = df_resume['rendimento'] / df_resume['aporte']

df2 = df.groupby(['Tipo', 'Nome'])\
    .agg(financeiro=('financeiro', 'last'), 
        aporte=('aporte', 'sum'), 
        retirada=('retirada', 'sum'), 
        rendimento=('rendimento', 'sum'))\
        .reset_index()        

df2['%'] = df2['rendimento'] / df2['aporte']

df_stocks = df2[df2['Tipo'] == 'Ação'].sort_values('financeiro', ascending=False)
df_bdrs = df2[df2['Tipo'] == 'BDR'].sort_values('financeiro', ascending=False)
df_fis = df2[df2['Tipo'] == 'FI'].sort_values('financeiro', ascending=False)
df_fiis = df2[df2['Tipo'] == 'FII'].sort_values('financeiro', ascending=False)

cols_resume = [
    dict(id='Tipo', name='Tipo'),
    dict(id='financeiro', name='Posição atual', type='numeric', format=money),
    dict(id='aporte', name='Aporte', type='numeric', format=money),
    dict(id='retirada', name='Retirada', type='numeric', format=money),
    dict(id='rendimento', name='Rendimento', type='numeric', format=money),
    dict(id='%', name='%', type='numeric', format=percentage)
]

cols1 = [
    #dict(id='Tipo', name='Tipo'),
    dict(id='Nome', name='Nome'),
    dict(id='financeiro', name='Posição atual', type='numeric', format=money),
    dict(id='aporte', name='Aporte', type='numeric', format=money),
    dict(id='retirada', name='Retirada', type='numeric', format=money),
    dict(id='rendimento', name='Rendimento', type='numeric', format=money),
    dict(id='%', name='%', type='numeric', format=percentage)
]

layout = html.Div([

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("AÇÕES"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=controller.timeline_by_types_chart(), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("AÇÕES"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=controller.timeline_by_pickings_chart(), config={'displayModeBar': False}),
                )
            ]), 
            lg=10, width={'offset': 1}
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

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("AÇÕES"),    
                dbc.CardBody(
                    html.Div(

                        DataTable(
                            id='table',
                            columns=cols1, #[{"name": i, "id": i} for i in df2.columns],
                            data=df_stocks.to_dict('records'),
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Nome']
                            ],
                            fixed_rows={'headers': True},
                            #style_table={'height': 400}, 
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                        )

                    )
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
                    html.Div(

                        DataTable(
                            id='table',
                            columns=cols1, #[{"name": i, "id": i} for i in df2.columns],
                            data=df_bdrs.to_dict('records'),
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Nome']
                            ],
                            fixed_rows={'headers': True},
                            #style_table={'height': 400}, 
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                        )

                    )
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
                    html.Div(

                        DataTable(
                            id='table',
                            columns=cols1, #[{"name": i, "id": i} for i in df2.columns],
                            data=df_fis.to_dict('records'),
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Nome']
                            ],
                            fixed_rows={'headers': True},
                            #style_table={'height': 400}, 
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                        )

                    )
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
                    html.Div(

                        DataTable(
                            id='table',
                            columns=cols1, #[{"name": i, "id": i} for i in df2.columns],
                            data=df_fiis.to_dict('records'),
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Nome']
                            ],
                            fixed_rows={'headers': True},
                            #style_table={'height': 400}, 
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                        )

                    )
                )
            ]),
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("DIVIDENDO AÇÕES"),    
                dbc.CardBody(
                    html.Div(

                        DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in df3.columns],
                            data=df3.to_dict('records'),
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Nome']
                            ],
                            fixed_rows={'headers': True},
                            #style_table={'height': 400}, 
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                        )

                    )
                )
            ]),
            lg=10, sm=10, width={'offset': 1}
        )
    ]),
    html.Br(),


    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("DIVIDENDO FII"),    
                dbc.CardBody(
                    html.Div(

                        DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in df4.columns],
                            data=df4.to_dict('records'),
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Nome']
                            ],
                            fixed_rows={'headers': True},
                            #style_table={'height': 400}, 
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold'
                            },
                        )

                    )
                )
            ]),
            lg=10, sm=10, width={'offset': 1}
        )
    ]),
    html.Br(),
    
])