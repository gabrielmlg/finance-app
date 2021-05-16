from dash_bootstrap_components._components.Card import Card
from dash_bootstrap_components._components.CardBody import CardBody
from dash_bootstrap_components._components.CardHeader import CardHeader
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_table import DataTable, FormatTemplate

from app_server import main_service

main_service.top_investiment('Ação')

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

cols1 = [
    #dict(id='Tipo', name='Tipo'),
    dict(id='Nome', name='Nome'),
    dict(id='financeiro', name='Posição atual', type='numeric', format=money),
    dict(id='aporte', name='Aporte', type='numeric', format=money),
    dict(id='retirada', name='Retirada', type='numeric', format=money),
    dict(id='rendimento', name='Rendimento', type='numeric', format=money),
    dict(id='%', name='%', type='numeric', format=percentage)
]

top5_cols = [
    dict(id='Nome', name='Nome'),
    dict(id='rendimento', name='Rendimento', type='numeric', format=money),
    dict(id='%', name='%', type='numeric', format=percentage)
]

layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("DISTRIBUIÇÃO DA CARTEIRA"),    
                dbc.CardBody(
                    dcc.Graph(id="position_pie_chart", figure=main_service.investiment_pie('Ação'), config={'displayModeBar': False}),
                )
            ]), 
            lg=3, width={'offset': 1}
        ), 
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("CALENDARIO"),    
                dbc.CardBody(
                    dcc.Graph(id="compare_havings_chart", figure=main_service.compare_investiment('Ação', 'Data'), config={'displayModeBar': False}),
                )
            ]), 
            lg=7
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('MELHORES RENDIMENTOS'), 
                dbc.CardBody(
                    html.Div(
                        DataTable(
                            id='tb_top5',
                            columns=top5_cols, 
                            data=main_service.top_investiment('Ação').to_dict('records'), 
                            style_data={'width': 'auto'}, 
                            style_cell={'font-family':'sans-serif', 'width': 'auto'},
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold',  
                                'font-family':'sans-serif', 
                                'width': 'auto'
                            },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                        'textAlign': 'left' 
                                } for c in ['Nome']
                            ],
                        )
                    )
                )
            ])
        ], lg=5, width={'offset': 1}), 
        dbc.Col(
            dbc.Card([
                dbc.CardHeader('PIORES RENDIMENTOS'), 
                dbc.CardBody(
                    html.Div(
                        DataTable(
                            id='tb_tail5',
                            columns=top5_cols, 
                            data=main_service.tail_investiment('Ação').to_dict('records'), 
                            style_cell={'font-family':'sans-serif'},
                            fixed_rows={'headers': True},
                            style_as_list_view=True,
                            style_header={
                                'backgroundColor': 'white',
                                'fontWeight': 'bold',  
                                'font-family':'sans-serif' 
                            },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left',  
                                } for c in ['Nome']
                            ],
                        )
                    )
                )
            ]), lg=5
        )
    ]), 
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Ativos"),    
                dbc.CardBody(
                    html.Div(

                        DataTable(
                            id='table',
                            columns=cols1, #[{"name": i, "id": i} for i in df2.columns],
                            data=main_service.datatable_investiment_resume('Ação').to_dict('records'),
                            style_cell={'fontSize':14, 'font-family':'sans-serif'}, 
                            style_cell_conditional=[
                                {
                                    'fontSize': 14,
                                    'font-family':'sans-serif',
                                    'if': {'column_id': c},
                                    'textAlign': 'left',  
                                } for c in ['Nome']
                            ],
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)', 
                                }
                            ],
                            fixed_rows={'headers': True},
                            #style_table={'height': 400}, 
                            style_as_list_view=True,
                            style_header={
                                #'backgroundColor': 'white',
                                'fontWeight': 'bold', 
                                'fontSize': 16, 
                                'font-family':'sans-serif' 
                            },
                        )

                    )
                )
            ]),
            lg=10, width={'offset': 1}
        )
    ]),
    html.Br(),

])