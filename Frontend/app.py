import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from Backend.services.StockServices import load_stock

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

df_stock = load_stock()

print(df_stock.head())

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_graph(df_stock):
    traces = [go.Scatter(x=df_stock['date'], y=df_stock['close'], name="Close", 
                            line_color='deepskyblue'), 
                go.Scatter(x=df_stock['date'], y=df_stock['open'], name="Open",
                            line_color='dimgray')
    ]

    return dcc.Graph(
        id='timeline-sotk', 
        figure={
            'data': traces, 
            'layout': go.Layout(title="Serie MGLU", 
                                xaxis_rangeslider_visible=True, 
                                width=1200, 
                                height=900)
        }
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Finance App'),
    html.Div(children='''Ações recomendadas para mentes milhonarias.'''),
    html.Br(), 
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),
    generate_graph(df_stock), 
    html.H4(children='Histórico da ação'),
    generate_table(df_stock)
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return '{}'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)