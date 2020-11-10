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


# POSICAO
posicao_model = Posicao() 
posicao_model.load_data()
df_fis = posicao_model.fis
df_acoes = posicao_model.acoes
fis_graph_ = fis_graph(df_fis)

# Extrato
extrato = Extrato(2010,2020)
fundo_investimento = FundoInvestimento(posicao=df_fis, extrato_hist=extrato.df, extrato=extrato.extrato_fis)
fiis = FundoImobiliario(posicao=posicao_model.fiis, extrato=extrato.df)

total_investido = extrato.total_investido()
total_aporte_fi = fundo_investimento.total_aportes() # extrato_fi['Vlr Aporte'].sum() -   # ToDo: Colocar o aporte de acoes e fii
periodos = extrato.periodos()

rendimento_fi = fundo_investimento.resumo(2010, 2020)['rendimento'].sum()


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
                    min=2010, #periodos.min(), 
                    max=2020, #periodos.max(), 
                    value=[2010, 2020],
                    marks={
                            2010: '2010', 
                            2011: '2011', 
                            2012: '2012', 
                            2013: '2013', 
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
                                    html.H4(id='total_investido_text'),
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
    [Output('total_investido_text', 'children'), 
    Output('total_aporte_fi_text', 'children'), 
    Output('total_rendimento_text', 'children'),
    Output('total_rendimento_fi_text', 'children'), 
    Output('total_patrimonio_text', 'children'), 
    Output('total_patrimonio_fi_text', 'children'), 
    Output('total_rendimento_acoes_text', 'children'), 
    Output('total_rendimento_fiis_text', 'children')],
    [Input('period-range-slider', 'value')])
def filter_period(periodo):
    extrato = Extrato(periodo[0], periodo[1])
    total_investido = extrato.total_investido()
    
    fundo_investimento = FundoInvestimento(posicao=df_fis, extrato_hist=extrato.df, 
                                            extrato=extrato.extrato_fis)
    acoes = Acao(posicao=df_acoes, extrato=extrato.df)
    total_aporte_fi = fundo_investimento.total_aportes() 
    # Modo Antigo
    #rendimento_fi = fundo_investimento.resumo(periodo[0], periodo[1])['rendimento'].sum()

    try: 
        rendimento_fi = fundo_investimento.calcula_rentabilidade(periodo[0], periodo[1])['rendimento'].sum() 
    except: 
        rendimento_fi = 0 

    try: 
        rendimento_acoes = acoes.calcula_rentabilidade(periodo[0], periodo[1])['rendimento'].sum() 
    except: 
        rendimento_acoes = 0

    try: 
        rendimento_fiis = fiis.calcula_rentabilidade(periodo[0], periodo[1])['rendimento'].sum() 
    except: 
        rendimento_fiis = 0 

    return (
        "Total: R$ {:,.2f}".format(total_investido), 
        "Fundos de Investimento: R$ {:,.2f}".format(total_aporte_fi),
        "Total: R$ {:,.2f}".format(rendimento_fi + rendimento_acoes + rendimento_fiis),
        "Fundos de Investimento: R$ {:,.2f}".format(rendimento_fi),  
        "Total: R$ {:,.2f}".format(total_investido + rendimento_fi),
        "Fundos de Investimento: R$ {:,.2f}".format(total_aporte_fi + rendimento_fi),
        "Ações: R$ {:,.2f}".format(rendimento_acoes), 
        "Fundos Imobiliários: R$ {:,.2f}".format(rendimento_fiis),  
    )
    
if __name__ == "__main__":
    app.run_server(debug=True)