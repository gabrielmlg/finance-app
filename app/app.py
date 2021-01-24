import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_html_components.Br import Br

#from backend.classes.model import Posicaomodel

# import backend.classes.model
from model import Posicao, Extrato
from views import FundoInvestimento, Acao, FundoImobiliario
from graphics import fis_graph
from controllers import MainController


# POSICAO
# ToDo: Refatorar jogando para dentro da Controller. 
main_controller = MainController()

app = dash.Dash(
    external_stylesheets=[dbc.themes.MATERIA]
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Resumo", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Mais", header=True),
                dbc.DropdownMenuItem("Posição", href="#"),
                dbc.DropdownMenuItem("Extrato", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="MEUS INVESTIMENTOS",
    brand_href="#",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    
    # header
    dbc.Row(dbc.Col(html.Div(navbar))), 
    html.Br(), 
    
    # filtro de periodo
    
    dbc.Row([
        dbc.Col(
                html.Div(
                    dcc.RangeSlider(
                    id="period-range-slider",  
                    min=2014, #2010  #periodos.min(), 
                    max=2020, #periodos.max(), 
                    value=[2014, 2020],
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
                            2020: '2020'
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
                                        html.H6(id='total_aporte_fi_text'),
                                        html.H6(id='total_aporte_fiis_text'),
                                        #html.H6("Ações: R$ {:,.2f} (*)".format(50000)),
                                    ]
                                ), 
                                dbc.Col(
                                    dcc.Graph(id="aporte_pie_chart", 
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
                #color="light"
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
                        color="light"
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
        ], color="light"), lg=3, width={'offset': -1}),
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
    
    #dbc.Alert("Em construção, aguarde ...", className="m-3"), 
    #main_controller.graph_fis()[0]
    

])


@app.callback(
    [Output('total_aportes_text', 'children'), 
    Output('total_aporte_acoes_text', 'children'), 
    Output('total_aporte_fi_text', 'children'), 
    Output('total_aporte_fiis_text', 'children'), 
    Output('total_rendimento_text', 'children'),
    Output('total_rendimento_acoes_text', 'children'), 
    Output('total_rendimento_fi_text', 'children'), 
    Output('total_rendimento_fiis_text', 'children'), 
    Output('total_patrimonio_text', 'children'), 
    Output('total_patrimonio_acoes_text', 'children'),
    Output('total_patrimonio_fi_text', 'children'), 
    Output('total_patrimonio_fiis_text', 'children'), 
    Output('revenue_chart', 'figure'), 
    Output('revenue_cumsum_chart', 'figure')],
    [Input('period-range-slider', 'value')])
def filter_period(periodo):
    return main_controller.load_new_filter(2010, periodo[1])


@app.callback(
    [Output('aporte_pie_chart', 'figure'), 
    Output('rendimento_pie_chart', 'figure'), 
    Output('patrimonio_pie_chart', 'figure')], 
    Input('period-range-slider', 'value')
)
def aporte_pie_chart_update(periodo):
    return (main_controller.aporte_pie_chart(), 
            main_controller.rendimento_pie_chart(), 
            main_controller.patrimonio_pie_chart())

    
if __name__ == "__main__":
    app.run_server(debug=True)