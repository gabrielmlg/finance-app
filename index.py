import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from apps.src.model import Posicao, Extrato
from apps.src.views import FundoInvestimento, Acao, FundoImobiliario
from apps.src.graphics import fis_graph
from apps.src.controllers import MainController

# Connect to main app.py file
from app_server import app
from app_server import server

# Connect to your app pages
from apps import resume, resume_detail

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Resumo", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Mais", header=True),
                dbc.DropdownMenuItem("Detalhes", href="/detail"),
                dbc.DropdownMenuItem("Comparativo", href="/"),
                dbc.DropdownMenuItem("Ações", href="/"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="MEUS INVESTIMENTOS",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Row(dbc.Col(html.Div(navbar))), 
        html.Br(), 
    ], style={'backgroundColor': '#F2F2F2'}),
    html.Div(id='page-content', children=[], style={'backgroundColor': '#F2F2F2'})
], style={'backgroundColor': '#F2F2F2'})


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return resume.layout
    if pathname == '/resumo':
        return resume.layout
    if pathname == '/detail':
        return resume_detail.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)