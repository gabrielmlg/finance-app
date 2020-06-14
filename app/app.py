import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

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
extrato = Extrato()
df_extrato = extrato_db.load_csv_extrato()
extrato_fi = extrato.get_extrato_fis(df_extrato)
total_aporte_fi = extrato.total_aportes(extrato_fi) # extrato_fi['Vlr Aporte'].sum() -   # ToDo: Colocar o aporte de acoes e fii
total_resgatado = extrato.total_resgatado(extrato_fi)
total_lucro = extrato.lucro_resgatado(extrato_fi)

fundo_investimento = FundoInvestimento(posicao=df_fis, extrato=extrato_fi)
rendimento_fi = fundo_investimento.rendimento()


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
    brand="Meus investimentos",
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
    dbc.Row(dbc.Col(html.Div(navbar))), 
    html.Br(), 
    dbc.Row([
        dbc.Col(dbc.Card([  
                            dbc.CardHeader("Aportes"),    
                            dbc.CardBody(
                                [
                                    html.H4("Total: R$ {:,.2f}".format(total_aporte_fi)),
                                    html.H6("FIs: R$ {:,.2f}".format(total_aporte_fi))
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
                            dbc.CardHeader("Rendimentos"),   
                            dbc.CardBody(
                                [
                                    html.H5("Total: R$ {:,.2f}".format(rendimento_fi)),
                                    html.H6("FIs: R$ {:,.2f}".format(rendimento_fi))
                                ]
                            ),
                        ], 
                        className="mb-3", 
                        color="light"
                    ), 
                    lg=3
        ),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Patrimonio"),
            dbc.CardBody(
                [
                    html.H5("Total: {:,.2f}".format(total_aporte_fi + rendimento_fi), className="card-title"),
                    html.P(
                        "FIs: R$ {:,.2f}".format(total_aporte_fi + rendimento_fi),
                        className="card-text",
                    ),
                ]
            ),
        ], color="light"), lg=3, width={'offset': -1}),
    ]), 
    # dbc.Alert("Em construção, aguarde ...", className="m-5"), 
    fis_graph_[0]
])

    
if __name__ == "__main__":
    app.run_server(debug=True)