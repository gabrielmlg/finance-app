import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

#from backend.classes.repository import PosicaoRepository

# import backend.classes.repository
from classes.repository import PosicaoRepository, ExtratoRepository
from classes.views import Extrato, FundoInvestimento
from classes.graphics import fis_graph


# POSICAO
posicao_repository = PosicaoRepository()
posicao_repository.load_data()
df_fis = posicao_repository.fis
fis_graph_ = fis_graph(df_fis)

# Extrato
extrato_db = ExtratoRepository()
df_extrato = extrato_db.load_csv_extrato()

extrato = Extrato(df_extrato)

total_investido = extrato.total_investido()
total_aporte_fi = extrato.total_aportes() # extrato_fi['Vlr Aporte'].sum() -   # ToDo: Colocar o aporte de acoes e fii
total_resgatado = extrato.total_resgatado()
total_lucro = extrato.lucro_resgatado()

fundo_investimento = FundoInvestimento(posicao=df_fis, extrato=extrato.df_extrato_fis)
rendimento_fi = fundo_investimento.rendimento()
periodos = fundo_investimento.periodos()

print(periodos.min())
print(periodos.max())


app = dash.Dash(
    external_stylesheets=[dbc.themes.FLATLY]
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
                    value=[2016, 2020],
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
            md=4     
        ), 
    ], 
    align="right", 
    justify="center"),
    html.Br(), 

    # Valor selecionado no range slider
    dbc.Row(html.Div(id='output-container-range-slider')), 

    # Cards de aporte, receita e patrimonio
    dbc.Row([
        dbc.Col(dbc.Card([  
                            dbc.CardHeader("APORTES"),    
                            dbc.CardBody(
                                [
                                    html.H4("Total: R$ {:,.2f}".format(total_investido)),
                                    html.Br(),
                                    html.H6("FIs: R$ {:,.2f}".format(total_aporte_fi)),
                                    html.H6("FIIs: R$ {:,.2f}".format((49*100) + (54*90) + (11*100) + (50*100) + (50*100))),
                                    html.H6("Ações: R$ {:,.2f}".format(50000)),
                                ]
                            ),
                        ], 
                        className="mb-3", 
                        color="light"
                    ), 
                    lg=3, 
                    width={'offset': 1}
        ),
        dbc.Col(dbc.Card([
                            dbc.CardHeader("RENDIMENTOS"),   
                            dbc.CardBody(
                                [
                                    html.H5("Total: R$ {:,.2f}".format(rendimento_fi)),
                                    html.Br(),
                                    html.H6("FIs: R$ {:,.2f}".format(rendimento_fi)),
                                    html.H6("FIIs: R$ {:,.2f}".format(10000)),
                                    html.H6("Ações: R$ {:,.2f}".format(50000)),
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
                    html.H5("Total: R$ {:,.2f}".format(rendimento_fi)),
                    html.Br(),
                    html.H6("FIs: R$ {:,.2f}".format(rendimento_fi)),
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
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('period-range-slider', 'value')])
def update_output(value):
    return (value)
    
if __name__ == "__main__":
    app.run_server(debug=True)