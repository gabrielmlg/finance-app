import pandas as pd
import numpy as np

from dash.dependencies import Input, Output

from app_server import app, services

@app.callback(
[Output('total_aportes_text', 'children'), 
Output('total_aporte_acoes_text', 'children'), 
Output('total_aporte_bdrs_text', 'children'), 
Output('total_aporte_fi_text', 'children'), 
Output('total_aporte_fiis_text', 'children'), 
Output('total_rendimento_text', 'children'),
Output('total_rendimento_acoes_text', 'children'), 
Output('total_rendimento_bdrs_text', 'children'), 
Output('total_rendimento_fi_text', 'children'), 
Output('total_rendimento_fiis_text', 'children'), 
Output('total_patrimonio_text', 'children'), 
Output('total_patrimonio_acoes_text', 'children'),
Output('total_patrimonio_bdrs_text', 'children'),
Output('total_patrimonio_fi_text', 'children'), 
Output('total_patrimonio_fiis_text', 'children'), 
Output('revenue_chart', 'figure'), 
Output('revenue_cumsum_chart', 'figure')],
[Input('period-range-slider', 'value')])
def filter_period(periodo):
    return services.resume_cards()

@app.callback(
    [Output('aporte_pie_chart', 'figure'), 
    Output('rendimento_pie_chart', 'figure'), 
    Output('patrimonio_pie_chart', 'figure')], 
    Input('period-range-slider', 'value')
)
def aporte_pie_chart_update(periodo):
    return (services.type_pie_chart('investido'), 
            services.type_pie_chart('rendimento'),
            services.type_pie_chart('patrimonio'))


@app.callback(
    Output('timeline_profits_chart_id', 'figure'), 
    Input('period-range-slider', 'value')
)
def timeline_profits_chart(period):
    return services.timeline_profits_per_type_chart()

