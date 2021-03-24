from _plotly_utils.colors.carto import Sunset
import plotly.graph_objs as go
import dash_core_components as dcc
import plotly.express as px
import numpy as np


pie_color_map = {
    'Ação': '#343AE9', 
     'FI': '#5157FF', 
     'FII': '#01CABB', 
     'BDR': '#F74AA8', 
     'Ouro': '#FECC53'            
}

color_list = [
    '#6837A9', '#7C37A9' '#A136A9', 
    '#A93677', '#A9363E',
    '#C67D44', '#EDE375',
    '#86BE3D', '#35A968',
    '#3DA936', '#35A9A0',
    '#3678A9', '#373EA9',
    '', ''
]

#color_list = px.colors.qualitative.Pastel + px.colors.qualitative.Pastel2 + px.colors.qualitative.Pastel1
color_seq_list = px.colors.sequential.Agsunset + px.colors.sequential.matter + px.colors.sequential.Sunset
#color_list = px.colors.qualitative.Light24
color_list = px.colors.qualitative.Dark24

colors = [
    '#694AF0', '#4D5CFA', '#4F63E6', #f92424
    '#5285E3', '#4DB8FA', 
    '#4ADCF0', '#80FFE0', 
    '#FAE692', '#8130E6', 
    '#F2D984', 
    '#F04162', # vermelho
    '#E64F4F'
]

colors2 = [
    # '#f92424', 
    '#2432f9', # azul
    '#2824f9', 
    '#4124f9', 
    '#5a24f9', 
    '#6f24f9', 
    '#7924f9', 
    '#9624f9', 
    '#b924f9', 
    '#e424f9',  # rosa
    '#f924b2', 
    '#f92468', # vermelho
    '#f92424', 
    '#f93d24', 
    '#f96424', # laranja
    '#f9a124', 
    '#f9cb24', 
    '#f92424', # amarelo
    '#f9f924' # esse aqui
    '#ddf924', 
    '#c1f924', 
    '#92f924', 
    '#5df924', 
    '#24f968', 
    '#24f988', 
    '#24f6f9', 
    '#24d9f9', 
    '#249df9'
]

pie_color_map = {
    'Ação': '#343AE9', 
     'FI': '#5157FF', 
     'FII': '#01CABB', 
     'BDR': '#F74AA8', 
     'Ouro': '#FECC53'            
}

#color_list = colors


def compare_havings(df, type, col_x):
    df_ = df[(df['periodo_cont'] > 0) & (df['Tipo'] == type)].sort_values(['Tipo', 'Nome', 'Data', 'periodo_cont'])
    #fig = px.line(df_, x="periodo_cont", y="%", color='Nome')

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


def resume_pie_chart(df, col_value):
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
            line=dict(width=0.5, color=color_list[0]), 
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


def timeline_pickings_chart(df):
    fig = go.Figure()

    for index, having in enumerate(df['Papel'].unique()):
        df_tmp = df[df['Papel'] == having]

        fig.add_trace(
            go.Bar(x=df_tmp['Data'],
                    y=df_tmp['Valor'],
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
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
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