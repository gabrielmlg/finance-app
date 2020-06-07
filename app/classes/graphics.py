import plotly.graph_objs as go
import dash_core_components as dcc

def fis_graph(df):
    
    fis_graph = []

    for fi in df['Nome'].unique():
        df_ = df[df['Nome'] == fi].sort_values('period')

        traces = [(go.Scatter(x=df_['period'], y=df_['Qtd Cotas'] * df_['Valor Cota'], 
                                connectgaps=True,
                                mode='lines+markers',
                                name=fi, 
                                #text=round(df[mkt].astype(float)/1000000, 2).astype(str) + 'M', 
                                textposition="top center",
                                textfont={'color': 'rgb(100,100,100)', 'size':9}, 
                                # fill='tonexty', 
                                # df_offplatformByWeek['2020 10'].map('{:,.0f}'.format), 
                                marker=dict(size=3), 
                                opacity=.8)
        )]

        layout = go.Layout(legend_orientation="h",
                        title=fi, 
                        height=300, 
                        width=600, 
                        legend=dict(font=dict(size=9)), 
                        template='plotly_white'                
        )

        fis_graph.append(dcc.Graph(
                        id='graph_' + str(len(fis_graph)),
                        figure={
                            'data': traces,
                            'layout': layout
                        })
        )
    
    return fis_graph