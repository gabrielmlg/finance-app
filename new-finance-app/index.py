import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app_server import app
#import callbacks
import flask

# Connect to your app pages
from pages import resume, stocks, detail, bdrs, fis

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Resumo", href="/")),
        dbc.NavItem(dbc.NavLink("Comparativo", href="/detail")),
        #dbc.NavItem(dbc.NavLink("Comparativo", href="/compare")),
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
        return resume.layout #compare_havings.layout
    if pathname == '/detail':
        return detail.layout #resume_detail.layout
    if pathname == '/stocks':
        return stocks.layout
    if pathname == '/bdrs':
        print('PARAMETROS: {}'.format(flask.request.args.get('type')))
        return bdrs.layout #bdrs.layout
    if pathname == '/fis':
        return fis.layout #fis.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)