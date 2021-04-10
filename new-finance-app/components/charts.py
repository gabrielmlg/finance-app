#from _plotly_utils.colors.carto import Sunset
import plotly.graph_objs as go
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
    df_ = df[df['Data'] >= '2014-08-01']
    df_['color'] = np.where(df_['%'] >= 0, colors[2], colors[11])
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df_['Data'],
                y=df_['%'],
                #mode='lines',
                name='% Rendimento',
                textposition='outside',
                text=df_['%'].apply(lambda x: f'{x:,.2f}%'),
                #marker=dict(size=7),
                marker_color=df_['color'], 
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
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
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

def compare_investiments_chart(df_, col_x):
    fig = go.Figure()
    
    for index, having in enumerate(df_['Nome'].unique()):
        df_tmp = df_[df_['Nome'] == having]

        fig.add_trace(go.Scatter(x=df_tmp[col_x], 
                    y=df_tmp['%'].cumsum(),
                    line=dict(width=1.5),
                    marker={'size': 4}, 
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