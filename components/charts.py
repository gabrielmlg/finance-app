#from _plotly_utils.colors.carto import Sunset
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_core_components as dcc
import plotly.express as px
import numpy as np

# Colors 
color_list = px.colors.qualitative.Light24
colors = [
    '#694AF0', '#4D5CFA', '#4F63E6', #f92424
    '#5285E3', '#4DB8FA', 
    '#4ADCF0', '#80FFE0', 
    '#FAE692', '#8130E6', 
    '#F2D984', 
    '#F04162', # vermelho
    '#E64F4F'
]
pie_color_map = {
    'Ação': '#343AE9', 
     'FI': '#5157FF', 
     'FII': '#01CABB', 
     'BDR': '#F74AA8', 
     'Ouro': '#FECC53'            
}


def type_pie_chart(df, col_value):
    df_pie = df\
            .groupby('Tipo')\
            .agg(aporte=('aporte', 'sum'), 
                    rendimento=('rendimento', 'sum'), 
                    retirada=('retirada', 'sum'))\
            .reset_index()

    df_pie['investido'] = df_pie['aporte'] - df_pie['retirada']
    df_pie['patrimonio'] = df_pie['investido'] + df_pie['rendimento']

    labels = df_pie['Tipo']
    values = df_pie[col_value].astype(int)
    colors = df_pie['Tipo'].map(pie_color_map)

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels, 
                values=values, 
                marker_colors=colors,
                hole=.5, 
                hoverinfo='label+value+percent',
                textinfo='label+percent',
                textfont=dict(size=9),
                scalegroup='one', 
                rotation=45
            )
        ]
    )

    fig.update_layout(
        height=125,
        showlegend=False, 
        margin=dict(l=0, r=0, t=0, b=0), 
        uniformtext_mode='hide', # esconde caso nao caiba na figura
        uniformtext_minsize=7, 
        template='plotly_white', 
    )

    return fig


def revenue_chart(df):
    df['color'] = np.where(df['%'] >= 0, colors[2], colors[11])
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df['Data'],
                y=df['%'],
                #mode='lines',
                name='% Rendimento',
                textposition='outside',
                text=df['%'].apply(lambda x: f'{x:,.2f}%'),
                #marker=dict(size=7),
                marker_color=df['color'], 
                #line=dict(color='#6A12E8', width=1.8),
                #opacity=.8
        )
    ) 

    fig.update_xaxes(
        #rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        template='plotly_white', 
        legend_orientation='h', 
        margin=dict(l=20, r=20, t=20, b=20), 
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


def revenue_cumsum_chart(df):
    # ToDo: Estou aqui!!! Adicionar novos traces por Tipo.

    fig = go.Figure()


    fig.add_trace(
        go.Scatter(x=df['Data'],
            y=df['renda_acum'],
            xperiod='M1',  
            #mode='none',
            #fill='tozeroy', 
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5, color=color_list[1]), 
            stackgroup='one'
            #name = 'Rendimento Acumulado',
            #text=df['renda_acum'].apply(lambda x: f'{x/1000:,.0f}K'),
            #textposition='outside',
            #line=dict(color=color_list[0], width=3),  
            #line_shape='linear'
        )
    )  
 
    fig.update_xaxes(
        #rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        template='plotly_white', 
        legend_orientation='h', 
        margin=dict(l=20, r=20, t=20, b=20), 
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


def timeline_profits_per_type_chart(df, col_category):
    fig = go.Figure()

    for index, having in enumerate(df[col_category].unique()):
        df_tmp = df[df[col_category] == having]

        fig.add_trace(
            go.Bar(x=df_tmp['Data'],
                    y=df_tmp['dividendo'],
                    #mode='lines',
                    name=having,
                    textposition='outside',
                    xperiod="M1",
                    #text=df['%'].apply(lambda x: f'{x:,.2f}%'),
                    #marker=dict(size=7),
                    marker_color=color_list[index], 
                    #line=dict(color='#6A12E8', width=1.8),
                    #opacity=.8
            )
    )  

    fig.update_xaxes(
        #rangeslider_visible=True,
        tickformat="%b\n%Y", 
        ticklabelmode="period", 
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        barmode='stack',
        template='plotly_white', 
        legend_orientation='v', 
        margin=dict(l=20, r=20, t=20, b=20), 
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


def timeline_pickings_chart(df):
    fig = go.Figure()

    for index, having in enumerate(df['Nome'].unique()):
        df_tmp = df[df['Nome'] == having]

        fig.add_trace(
            go.Bar(x=df_tmp['Data'],
                    y=df_tmp['dividendo'],
                    #mode='lines',
                    name=having,
                    textposition='outside',
                    xperiod="M1",
                    #text=df['%'].apply(lambda x: f'{x:,.2f}%'),
                    #marker=dict(size=7),
                    marker_color=color_list[index], 
                    #line=dict(color='#6A12E8', width=1.8),
                    #opacity=.8
            )
    )  

    fig.update_xaxes(
        #rangeslider_visible=True,
        tickformat="%b\n%Y", 
        ticklabelmode="period", 
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        barmode='stack',
        template='plotly_white', 
        legend_orientation='v', 
        margin=dict(l=20, r=20, t=20, b=20), 
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


def compare_investiments_cumsum_chart(df_, col_x, names):
    fig = go.Figure()
    
    for index, having in enumerate(names):
        df_tmp = df_[df_['Nome'] == having]

        fig.add_trace(go.Scatter(x=df_tmp[col_x], 
                    y=df_tmp['%'].cumsum() * 100,
                    line=dict(width=1.5),
                    marker={'size': 3}, 
                    marker_color=color_list[index], 
                    mode='lines+markers',
                    line_shape='spline',
                    name=having))

    fig.update_layout(
        template='plotly_white', 
        legend_orientation='v',
        margin=dict(l=10, r=10, t=10, b=10),
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


def compare_investiments_chart(df_, col_x):
    fig = go.Figure()
    
    for index, having in enumerate(df_['Nome'].unique()):
        df_tmp = df_[df_['Nome'] == having]

        fig.add_trace(go.Scatter(x=df_tmp[col_x], 
                    y=df_tmp['%'],
                    line=dict(width=1.5),
                    marker={'size': 3}, 
                    marker_color=color_list[index], 
                    mode='lines+markers',
                    #line_shape='spline',
                    name=having))

    fig.update_layout(
        template='plotly_white', 
        legend_orientation='h',
        margin=dict(l=10, r=10, t=10, b=10),
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


def timeline_by_types(df):
    fig = go.Figure()

    for index, type in enumerate(df['Tipo'].unique()):
        df_tmp = df[df['Tipo'] == type]

        fig.add_trace(go.Scatter(x=df_tmp['Data'], 
                    y=df_tmp['%'].cumsum(),
                    line=dict(width=2),
                    marker={'size': 4}, 
                    marker_color=color_list[index], 
                    mode='lines+markers',
                    line_shape='spline', 
                    name=type))

    fig.update_layout(
        template='plotly_white', 
        legend_orientation='h', 
        margin=dict(l=10, r=10, t=10, b=10),
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


def timeline_by_type_relative(df):
    fig = go.Figure()

    for index, type in enumerate(df['Tipo'].unique()):
        df_tmp = df[df['Tipo'] == type]
        
        fig.add_trace(go.Bar(x=df_tmp['Data'],
                    y=df_tmp['%'],
                    #mode='lines',
                    name=type,
                    textposition='outside',
                    xperiod="M1",
                    #text=df['%'].apply(lambda x: f'{x:,.2f}%'),
                    #marker=dict(size=7),
                    marker_color=color_list[index], 
                    #line=dict(color='#6A12E8', width=1.8),
                    #opacity=.8
            ))

    fig.update_xaxes( 
        #rangeslider_visible=True,
        tickformat="%b\n%Y", 
        ticklabelmode="period", 
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        barmode='stack',
        template='plotly_white', 
        legend_orientation='v', 
        margin=dict(l=20, r=20, t=20, b=20), 
        #height=600, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig

# PAGE DETAIL    


def cashin_timeline(df, col):
    fig = go.Figure()
   
    fig.add_trace(go.Scatter(x=df['Data'], 
                    y=df[col].cumsum(),
                    line=dict(width=2, color='#1F8DF1'),
                    marker={'size': 4}, 
                    fill='tozeroy', 
                    #marker_color=color_list[index], 
                    #mode='lines+markers',
                    #line_shape='spline', 
                    name=col))

    fig.update_layout(
        barmode='stack',
        template='plotly_white', 
        legend_orientation='v', 
        margin=dict(l=20, r=20, t=20, b=20), 
        height=200, 
        #width=1000, 
        title={
            'y':0.9,
            'xanchor': 'left',
            'yanchor': 'top'}
        
    )

    return fig


####
# BDR, Ações, FIS, FIIS
#####

def investiment_pie_chart(df):
    df = df[df['financeiro'] > 0]
    labels = df['Nome']
    values = df['financeiro'].astype(int)
    colors = color_list

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels, 
                values=values, 
                marker_colors=colors,
                hole=.3,  
                hoverinfo='label+value+percent',
                textinfo='label+percent',
                textfont=dict(size=12),
                scalegroup='one', 
                #rotation=45
            )
        ]
    )

    fig.update_layout(
        #height=125,
        showlegend=False, 
        margin=dict(l=50, r=50, t=50, b=50), 
        uniformtext_mode='hide', # esconde caso nao caiba na figura
        uniformtext_minsize=7, 
        template='plotly_white', 
    )

    return fig


# ANALYSIS PAGE

def tickerAnalysisGraphic(df, ticket, lines=[]):
    df_ = df.tail(360*2)
    trace = {
        'x': df_.index, 
        'open': df_['Open'], 
        'close': df_['Close'], 
        'high': df_['High'], 
        'low': df_['Low'], 
        'type': 'candlestick', 
        'increasing_line_color': '#03A688', 
        'decreasing_line_color': '#F20544', 
        'name': ticket, 
        'showlegend': False, 
        'yaxis':'y1'
    }

    data = [trace]
    layout = go.Layout(
        template='plotly_white', 
        margin=dict(l=50, r=10, t=50, b=10), 
    )

    fig_ = go.Figure(data=data, layout=layout)
    fig = make_subplots(specs=[[{"secondary_y": True}]], figure=fig_)

    if len(lines) > 0:
        for col in lines:
            fig.add_trace(
                go.Scatter(
                    x=list(df_.index), 
                    y=df_[col], 
                    mode='lines', 
                    name=col, 
                    yaxis='y1'
                )
            )

    fig.add_trace(
        go.Bar(x=df_.index,
            y=df_['Volume'],
            name = 'Volume',
            marker=dict(color='gray'), 
            yaxis='y2'
            ))

    fig.add_trace(
        go.Scatter(
            x=list(df_.index), 
            y=df_['mm_vol_60d'], 
            mode='lines', 
            name=col, 
            yaxis='y2', 
            line=dict(color='rgb(241,149,18)', width=0.8),
        )
    )

    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        yaxis2=dict(
            range=[0, df_['Volume'].max()*5]
        )
    )

    return fig