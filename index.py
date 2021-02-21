import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from apps.src.model import Posicao, Extrato
from apps.src.views import FundoInvestimento, Acao, FundoImobiliario
from apps.src.controller import MainController

# Connect to main app.py file
from app_server import app
from app_server import server

# Connect to your app pages
from apps import bdrs, resume, resume_detail, stocks, fis, compare_havings

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Resumo", href="/")),
        dbc.NavItem(dbc.NavLink("Analitico", href="/detail")),
        dbc.NavItem(dbc.NavLink("Comparativo", href="/compare")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Mais", header=True),
                dbc.DropdownMenuItem("Ações", href="/stocks"),
                dbc.DropdownMenuItem("BDRs", href="/bdrs"),
                dbc.DropdownMenuItem("FIs", href="/fis"),
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
    ], style={'backgroundColor': '#FAFAFA'}),
    html.Div(id='page-content', children=[], style={'backgroundColor': '#FAFAFA'})
], style={'backgroundColor': '#FAFAFA'})


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return resume.layout
    if pathname == '/resumo':
        return resume.layout
    if pathname == '/compare':
        return compare_havings.layout
    if pathname == '/detail':
        return resume_detail.layout
    if pathname == '/stocks':
        return stocks.layout
    if pathname == '/bdrs':
        return bdrs.layout
    if pathname == '/fis':
        return fis.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)