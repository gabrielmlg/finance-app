import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

#from backend.classes.repository import PosicaoRepository

# import backend.classes.repository
from classes.repository import PosicaoRepository
from classes.views import Extrato
from classes.graphics import fis_graph

# POSICAO
posicao_repository = PosicaoRepository()
posicao_repository.load_data()
df_fis = posicao_repository.fis
fis_graph_ = fis_graph(df_fis)

# EXTRATO
extrato = Extrato()
df_extrato = extrato.get_extrato()
extrato_fi = extrato.extrato_fis(df_extrato)
total_aporte = extrato_fi['Vlr Aporte'].sum() # ToDo: Colocar o aporte de acoes e fii

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
        dbc.Col(dbc.Card(
                            [
                                dbc.CardHeader("Aportes"),
                                dbc.CardBody(
                                    [
                                        html.H5("Total: {:,.2f}".format(total_aporte), className="card-title"),
                                        html.P(
                                            "A meta do ano é acrescentar mais R$ 40K",
                                            className="card-text",
                                        ),
                                    ]
                                ),
                            ], 
                            color="success", 
                            outline=True
                        ), lg=3, width={'offset': 1}
        ),
        dbc.Col(dbc.Card(card_content, color="warning", outline=True), lg=3),
        dbc.Col(dbc.Card(card_content, color="danger", outline=True), lg=3, width={'offset': -1}),
    ], className='mb-4', align="center"), 
    # dbc.Alert("Em construção, aguarde ...", className="m-5"), 
    fis_graph_[0]
])

    
if __name__ == "__main__":
    app.run_server()