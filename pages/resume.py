import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.CardBody import CardBody
from dash_bootstrap_components._components.Row import Row
from dash_core_components.Graph import Graph
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components.Br import Br
from dash_table import DataTable, FormatTemplate

money = FormatTemplate.money(2)
percentage = FormatTemplate.percentage(2)

top5_cols = [
    dict(id='Nome', name='Nome'),
    dict(id='rendimento', name='Rendimento', type='numeric', format=money),
    dict(id='%', name='%', type='numeric', format=percentage)
]

layout = html.Div([

    dbc.Row([
        dbc.Col(
                html.Div(
                    dcc.RangeSlider(
                    id="period-range-slider",  
                    min=2014, #2010  #periodos.min(), 
                    max=2021, #periodos.max(), 
                    value=[2014, 2021],
                    marks={
                            #2010: '2010', 
                            #2011: '2011', 
                            #2012: '2012', 
                            #2013: '2013', 
                            2014: '2014', 
                            2015: '2015', 
                            2016: '2016', 
                            2017: '2017', 
                            2018: '2018', 
                            2019: '2019', 
                            2020: '2020', 
                            2021: '2021'
                    },
                    allowCross=False, 
                    step=1, 
                    dots=True,
                    included=True,
                    # className='slider'
                ),
            ),
            md=6     
        ), 
    ], 
    align="right", 
    justify="center"),
    html.Br(), 
    
    # Valor selecionado no range slider
    dbc.Row(
        dbc.Col(html.Div(id='output-container-range-slider'))
    ), 

    # Cards de aporte, receita e patrimonio
    dbc.Row([
        dbc.Col(dbc.Card([  
                    dbc.CardHeader("APORTES"),    
                    dbc.CardBody(
                        html.Div(
                            dbc.Row([
                                dbc.Col(
                                    [
                                        html.H4(id='total_aportes_text'),
                                        html.Br(),
                                        html.H6(id='total_aporte_acoes_text'),
                                        html.H6(id='total_aporte_bdrs_text'),
                                        html.H6(id='total_aporte_fi_text'),
                                        html.H6(id='total_aporte_fiis_text'),
                                        #html.H6("Ações: R$ {:,.2f} (*)".format(50000)),
                                    ]
                                ), 
                                dbc.Col(
                                    dcc.Graph(id="aporte_pie_chart", 
                                                figure={}, 
                                                config={'displayModeBar': False}, 
                                                style={'margin-top': '20px'}
                                    ),
                                )
                            ])
                            
                        )
                    ),
                ], 
                className="mb-3", 
                #color="dark", 
            ), 
            lg=3, 
            #className='ml-3', 
            width={'offset': 1}
        ),
        dbc.Col(dbc.Card([
                            dbc.CardHeader("RENDIMENTOS"),   
                            dbc.CardBody(
                                html.Div(
                                    dbc.Row([
                                        dbc.Col(
                                            [
                                                html.H4(id='total_rendimento_text'),
                                                html.Br(),
                                                html.H6(id='total_rendimento_acoes_text'),
                                                html.H6(id='total_rendimento_bdrs_text'),
                                                html.H6(id='total_rendimento_fi_text'),
                                                html.H6(id='total_rendimento_fiis_text'),
                                            ]
                                        ), 
                                        dbc.Col(
                                            dcc.Graph(id="rendimento_pie_chart", 
                                                        figure={}, 
                                                        config={'displayModeBar': False}, 
                                                        #style={'margin-top': '20px'}
                                            ),
                                        )
                                    ])
                                    
                                )
                            ),
                        ], 
                        className="mb-3", 
                        #color="dark"
                    ), 
                    lg=3
        ),
        dbc.Col(dbc.Card([
            dbc.CardHeader("PATRIMONIO"),
            dbc.CardBody(
                html.Div(
                    dbc.Row([
                        dbc.Col(
                            [
                                html.H4(id='total_patrimonio_text'),
                                html.Br(),
                                html.H6(id='total_patrimonio_acoes_text'),
                                html.H6(id='total_patrimonio_bdrs_text'),
                                html.H6(id='total_patrimonio_fi_text'),
                                html.H6(id='total_patrimonio_fiis_text'),
                            ]
                        ), 
                        dbc.Col(
                            dcc.Graph(id="patrimonio_pie_chart", 
                                        figure={}, 
                                        config={'displayModeBar': False}, 
                                        #style={'margin-top': '20px'}
                            ),
                        )
                    ])
                    
                )
            ),
        ], 
        #color="dark", 
        ), lg=3, width={'offset': -1}),
    ]), 

    dbc.Row([
        dbc.Col(dbc.Card([  
                    dbc.CardHeader("RENDIMENTO POR MÊS (%)"),    
                    dbc.CardBody(
                        [
                            dcc.Graph(id="revenue_chart", figure={}, config={'displayModeBar': False}),
                        ]
                    ),
                ], 
                className="mb-9", 
                #color="light"
            ), 
            lg=9, 
            #className='ml-3', 
            width={'offset': 1}
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('MELHORES RENDIMENTOS | ÚLTIMO MÊS'), 
                dbc.CardBody(
                    html.Div(
                        DataTable(
                            id='top_investiment_table_id',
                            columns=top5_cols, 
                            data=[], 
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
                dbc.CardHeader('PIORES RENDIMENTOS | ÚLTIMO MÊS'), 
                dbc.CardBody(
                    html.Div(
                        DataTable(
                            id='tail_investiment_table_id',
                            columns=top5_cols, 
                            data=[], 
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
            ]), lg=4
        )
    ]), 
    html.Br(),

    dbc.Row([
        dbc.Col(dbc.Card([  
                    dbc.CardHeader("RENDIMENTO ACUMULADO"),    
                    dbc.CardBody(
                        [
                            dcc.Graph(id="revenue_cumsum_chart", figure={}, config={'displayModeBar': False}),
                        ]
                    ),
                ], 
                className="mb-9",  
                #color="light"
            ), 
            lg=9, 
            #className='ml-3', 
            width={'offset': 1}
        )
    ]),
    html.Br(),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("DIVIDENDOS"),    
                dbc.CardBody(
                    dcc.Graph(id="timeline_profits_chart_id", figure={}, config={'displayModeBar': False}),
                )
            ]), 
            lg=9, sm=10, width={'offset': 1}
        )
    ]),
    html.Br(),
    
    #dbc.Alert("Em construção, aguarde ...", className="m-3"), 
    #controller.graph_fis()[0]
    

])
