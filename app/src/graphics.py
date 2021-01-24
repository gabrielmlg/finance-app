import plotly.graph_objs as go
import dash_core_components as dcc

def aporte_pie_chart(df):
    df_pie = df\
            .groupby('Tipo')\
            .agg(aporte=('aporte', 'sum'), 
                    retirada=('retirada', 'sum'))\
            .reset_index()

    df_pie['investido'] = df_pie['aporte'] - df_pie['retirada']

    labels = df_pie['Tipo']
    values = df_pie['investido']

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    fig.update_layout(
        height=80,
        showlegend=False, 
        margin=dict(l=2, r=2, t=2, b=2), 
        template='plotly_white', 
    )

    return fig 


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

def graph_revenue(df):
    data = [
        go.Scatter(x=df['Data'],
                y=df['%'],
                mode='lines',
                name='% Rendimento',
                textposition='top center',
                text=df['%'].apply(lambda x: f'{x:,.2f}%'),
                marker=dict(size=7),
                line=dict(color='rgb(115,115,115)', width=1.8),
                opacity=.8)
    ]

    layout = [
        go.Layout(
            template='plotly_white', 
            legend_orientation='h', 
            #height=600, 
            #width=1000, 
            title={
                'y':0.9,
                'xanchor': 'left',
                'yanchor': 'top'}, 
            xaxes={
                'rangeslider_visible': True,
                'rangeselector': dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
                )
            }
        )
    ]

    return dcc.Graph(
        id='graph_revenue',
        figure={
            'data': data,
            'layout': layout
        }
    )

def revenue_chart(df):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df['Data'],
                y=df['%'],
                #mode='lines',
                name='% Rendimento',
                textposition='outside',
                #text=df['%'].apply(lambda x: f'{x:,.2f}%'),
                #marker=dict(size=7),
                marker_color=df['color'], 
                #line=dict(color='#6A12E8', width=1.8),
                opacity=.8))  

    fig.update_xaxes(
        #rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        template='plotly_white', 
        legend_orientation='h', 
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig

def revenue_cumsum_chart(df):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['Data'],
            y=df['renda_acum'],
            mode='lines',
            name = 'Rendimento Acumulado',
            text=df['renda_acum'].apply(lambda x: f'{x/1000:,.0f}K'),
            #textposition='outside',
            line=dict(color='#8B09FF'), 
            line_shape='linear'
            ))            
    
    fig.update_xaxes(
        #rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        template='plotly_white', 
        legend_orientation='h', 
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig