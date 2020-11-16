import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

#from backend.classes.model import Posicaomodel

# import backend.classes.model
from classes.model import Posicao, Extrato
from classes.views import FundoInvestimento, Acao, FundoImobiliario
from classes.graphics import fis_graph

from classes.controllers import MainController


# POSICAO
# ToDo: Refatorar jogando para dentro da Controller. 

main_controller = MainController()
main_controller.load_new_filter(2010, 2020)

posicao_model = Posicao() 
posicao_model.load_data()
df_fis = posicao_model.fis
df_acoes = posicao_model.acoes
fis_graph_ = main_controller.graph_fis()

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
    color="primary",
    dark=True,
)


card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]


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
                    value=[2010, 2020],
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
                                [
                                    html.H4(id='total_aportes_text'),
                                    html.Br(),
                                    html.H6(id='total_aporte_fi_text'),
                                    html.H6("Fundos Imobiliários: R$ {:,.2f}".format((49*100) + (54*90) + (11*100) + (50*100) + (50*100))),
                                    html.H6("Ações: R$ {:,.2f}".format(50000)),
                                ]
                            ),
                        ], 
                        className="ml-3", 
                        color="light"
                    ), 
                    lg=3, 
                    #className='ml-3', 
                    width={'offset': 1}
        ),
        dbc.Col(dbc.Card([
                            dbc.CardHeader("RENDIMENTOS"),   
                            dbc.CardBody(
                                [
                                    html.H4(id='total_rendimento_text'),
                                    html.Br(),
                                    html.H6(id='total_rendimento_fi_text'),
                                    html.H6(id='total_rendimento_fiis_text'),
                                    html.H6(id='total_rendimento_acoes_text'),
                                ]
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
                [
                    html.H4(id='total_patrimonio_text'),
                    html.Br(),
                    html.H6(id='total_patrimonio_fi_text'),
                    html.H6("FIIs: R$ {:,.2f}".format(10000)),
                    html.H6("Ações: R$ {:,.2f}".format(50000)),
                ]
            ),
        ], color="light"), lg=3, width={'offset': -1}),
    ]), 
    
    # dbc.Alert("Em construção, aguarde ...", className="m-5"), 
    fis_graph_[0]

])


@app.callback(
    [Output('total_aportes_text', 'children'), 
    Output('total_aporte_fi_text', 'children'), 
    Output('total_rendimento_text', 'children'),
    Output('total_rendimento_fi_text', 'children'), 
    Output('total_patrimonio_text', 'children'), 
    Output('total_patrimonio_fi_text', 'children'), 
    Output('total_rendimento_acoes_text', 'children'), 
    Output('total_rendimento_fiis_text', 'children')],
    [Input('period-range-slider', 'value')])
def filter_period(periodo):
    return main_controller.load_new_filter(periodo[0], periodo[1])
    
if __name__ == "__main__":
    app.run_server(debug=True)