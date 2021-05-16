from data.source import AwsClient, Position, Extract
from data.reshape import Transform
from components import charts
import pandas as pd

class MainService:
    ''' Base class to all callbacks, like a controller to MVC '''
    def __init__(self):
        self.resume = self.load_data()


    def load_data(self):
        aws_client = AwsClient()
        transform = Transform()
        
        aws_client.load_data_s3()
        self.position = Position(aws_client.df_list_pos)
        self.extract = Extract(2010, 2021, aws_client.extrato, aws_client.extrato_bolsa)

        return transform.resume(self.position, self.extract)


    def groupby_date(self):
        df = self.resume[self.resume['Data'] != 0]
        df['Data'] = pd.to_datetime(df['Data'])
        
        df = df.groupby(['Data', 'ano', 'mes'])\
                        .agg(financeiro=('Financeiro', 'sum'), 
                            aporte=('aporte', 'sum'), 
                            retirada=('retirada', 'sum'), 
                            rendimento=('rendimento', 'sum'), 
                            rendimento_percent=('%', 'mean'))\
                        .reset_index()\
                        .fillna(0)
        df['%'] = df['rendimento'] / df['financeiro'] * 100
        df['renda_acum'] = df['rendimento'].cumsum()
        df['aporte_acum'] = df['aporte'].cumsum()
        df['retirada_acum'] = df['retirada'].cumsum()
        df['investido'] = df['aporte_acum'] - df['retirada_acum']
        df['% renda_acum'] = df['rendimento'].cumsum() / (df['investido']) * 100  
        df = df.fillna(0)
        
        return df


    def groupby_date_and_investiment(self):
        df = self.resume[self.resume['Data'] != 0]
        df['Data'] = pd.to_datetime(df['Data'])
        
        df = df.groupby(['Nome', 'Data', 'ano', 'mes'])\
                        .agg(financeiro=('Financeiro', 'sum'), 
                            aporte=('aporte', 'sum'), 
                            retirada=('retirada', 'sum'), 
                            rendimento=('rendimento', 'sum'), 
                            rendimento_percent=('%', 'mean'))\
                        .reset_index()\
                        .fillna(0)
        df['%'] = df['rendimento'] / df['financeiro'] * 100
        df['renda_acum'] = df['rendimento'].cumsum()
        df['aporte_acum'] = df['aporte'].cumsum()
        df['retirada_acum'] = df['retirada'].cumsum()
        df['investido'] = df['aporte_acum'] - df['retirada_acum']
        df['% renda_acum'] = df['rendimento'].cumsum() / (df['investido']) * 100  
        df = df.fillna(0)
        
        return df


    def compare_investiment(self, type, col_x):
        #print(self.resume.head(10))
        #print(self.resume.columns)
        df_ = self.resume[self.resume['Tipo'] == type].sort_values(['Tipo', 'Nome', 'Data'])
        return charts.compare_investiments_cumsum_chart(df_, col_x)


    def resume_cards(self):
        total_aportes = self.extract.total_investido()
        fi_resumo = self.resume[self.resume['Tipo'] == 'FI']
        acoes_resumo = self.resume[self.resume['Tipo'] == 'Ação']
        bdr_resume = self.resume[self.resume['Tipo'] == 'BDR']
        fiis_resumo = self.resume[self.resume['Tipo'] == 'FII']

        df = self.resume[self.resume['Data'] != 0]
        df['Data'] = pd.to_datetime(df['Data'])
        df = df.groupby(['Data', 'ano', 'mes'])\
                        .agg(financeiro=('Financeiro', 'sum'), 
                            aporte=('aporte', 'sum'), 
                            retirada=('retirada', 'sum'), 
                            rendimento=('rendimento', 'sum'), 
                            rendimento_percent=('%', 'mean'))\
                        .reset_index()\
                        .fillna(0)
        df['%'] = df['rendimento'] / df['financeiro'] * 100
        df['renda_acum'] = df['rendimento'].cumsum()
        df['aporte_acum'] = df['aporte'].cumsum()
        df['retirada_acum'] = df['retirada'].cumsum()
        df['investido'] = df['aporte_acum'] - df['retirada_acum']
        df['% renda_acum'] = df['rendimento'].cumsum() / (df['investido']) * 100  
        df = df.fillna(0)
        #df_graph1['color'] = np.where(df_graph1['%'] >= 0, '#2B04E8', '#F24171')

        try: 
            total_aporte_fi = fi_resumo['aporte'].sum() - fi_resumo['retirada'].sum()
            rendimento_fi = fi_resumo['rendimento'].sum()
            rendimento_perc_fi = (rendimento_fi / total_aporte_fi) * 100
        except: 
            total_aporte_fi = 0 
            rendimento_fi = 0 
            rendimento_perc_fi = 0

        try: 
            total_aporte_acoes = acoes_resumo['aporte'].sum() - acoes_resumo['retirada'].sum()
            total_aporte_bdrs = bdr_resume['aporte'].sum() - bdr_resume['retirada'].sum()
            rendimento_acoes = acoes_resumo['rendimento'].sum()
            rendimento_bdrs = bdr_resume['rendimento'].sum()
            rend_acoes_perc = (rendimento_acoes / total_aporte_acoes) * 100
            rend_bdrs_perc = (rendimento_bdrs / total_aporte_bdrs) * 100
        except: 
            total_aporte_acoes = 0
            total_aporte_bdrs = 0
            rendimento_acoes = 0
            rendimento_bdrs = 0
            rend_acoes_perc = 0
            rend_bdrs_perc = 0

        try: 
            total_aporte_fiis = fiis_resumo['aporte'].sum() - fiis_resumo['retirada'].sum()
            rendimento_fiis = fiis_resumo['rendimento'].sum()
            rend_fiis_perc = (rendimento_fiis / total_aporte_fiis) * 100
        except: 
            total_aporte_fiis = 0
            rendimento_fiis = 0 
            rend_fiis_perc = 0


        return (
            "R$ {:,.2f}".format(total_aportes), 
            "Ações: R$ {:,.2f}".format(total_aporte_acoes),
            "BDRs: R$ {:,.2f}".format(total_aporte_bdrs),
            "FIs: R$ {:,.2f}".format(total_aporte_fi),
            "FIIs: R$ {:,.2f}".format(total_aporte_fiis),
            
            "R$ {:,.2f}".format(rendimento_fi + rendimento_acoes + rendimento_fiis),
            "R$ {:,.2f} ({:,.2f}%)".format(rendimento_acoes, rend_acoes_perc),  
            "R$ {:,.2f} ({:,.2f}%)".format(rendimento_bdrs, rend_bdrs_perc),  
            "R$ {:,.2f} ({:,.2f}%)".format(rendimento_fi, rendimento_perc_fi),  
            "R$ {:,.2f} ({:,.2f}%)".format(rendimento_fiis, rend_fiis_perc),  
            
            
            "R$ {:,.2f}".format(total_aportes + rendimento_acoes + rendimento_fi + rendimento_fiis),
            "R$ {:,.2f}".format(total_aporte_acoes + rendimento_acoes), 
            "R$ {:,.2f}".format(total_aporte_bdrs + rendimento_bdrs), 
            "R$ {:,.2f}".format(total_aporte_fi + rendimento_fi),
            "R$ {:,.2f}".format(total_aporte_fiis + rendimento_fiis),  
            charts.revenue_chart(df), 
            charts.revenue_cumsum_chart(df)
            #self.revenue_cumsum_chart()
        )


    def revenue_timeline_chart(self):
        df = self.groupby_date()
        return charts.revenue_chart(df)

    def type_pie_chart(self, measure):
        return charts.type_pie_chart(self.resume, measure)


    def timeline_profits_chart(self):
        df = self.resume[self.resume['dividendo'] > 0]
        df = df.groupby(['Tipo', 'Nome', 'Data'])\
            .agg(dividendo=('dividendo', 'sum'))\
            .reset_index()

        names_sort = df.groupby('Nome')\
            .agg(dividendo=('dividendo', 'sum')).reset_index().sort_values('dividendo', ascending=False)['Nome']

        df['Nome'] = pd.Categorical(df['Nome'],
                             categories=names_sort,
                             ordered=True)
        df = df.sort_values('Nome', ascending=False)
        
        return charts.timeline_pickings_chart(df)


    def timeline_profits_per_type_chart(self):
        df = self.resume[self.resume['dividendo'] > 0]
        df = df.groupby(['Tipo', 'Data'])\
            .agg(dividendo=('dividendo', 'sum'))\
            .reset_index()

        names_sort = df.groupby('Tipo')\
            .agg(dividendo=('dividendo', 'sum')).reset_index().sort_values('dividendo', ascending=False)['Tipo']

        df['Tipo'] = pd.Categorical(df['Tipo'],
                             categories=names_sort,
                             ordered=True)
        df = df.sort_values('Tipo', ascending=False)
        
        return charts.timeline_profits_per_type_chart(df, 'Tipo')


    def timeline_by_types_chart(self):
        df = self.resume[self.resume['Data'] != 0]
        df = df[df['Data'] >= '2014-08-01']
        df = df[(df['periodo_cont'] > 0)].sort_values(['Tipo', 'Data'])
        df = df\
            .groupby(['Tipo', 'Data'])\
            .agg(financeiro=('Financeiro', 'sum'), 
                aporte=('aporte', 'sum'), 
                retirada=('retirada', 'sum'), 
                rendimento=('rendimento', 'sum'))\
            .reset_index()
        df['%'] = df['rendimento'] / (df['financeiro'] + df['retirada']) * 100

        return charts.timeline_by_types(df)

# DETAIL  PAGE

    def cashin_timeline_chart(self):
        df = self.resume
        df = df[(df['periodo_cont'] > 0)].sort_values(['Data'])
        df = df.groupby('Data')\
                .agg(aporte=('aporte', 'sum'), 
                        retirada=('retirada', 'sum'))\
                .reset_index()
        df['aporte'] = df['aporte'] - df['retirada']

        return charts.cashin_timeline(df, 'aporte')


    def timeline_by_type_relative_chart(self):
        df = self.resume
        df = df[(df['periodo_cont'] > 0)].sort_values(['Tipo', 'Data'])
        df = df\
            .groupby(['Tipo', 'Data'])\
            .agg(financeiro=('Financeiro', 'sum'), 
                aporte=('aporte', 'sum'), 
                retirada=('retirada', 'sum'), 
                rendimento=('rendimento', 'sum'), 
                rend_percent=('%', 'mean'))\
            .reset_index()
        df['%'] = df['rendimento'] / (df['financeiro'] + df['retirada']) * 100

        return charts.timeline_by_type_relative(df)


# ''' POR TIPO DE ATIVO  '''

    def datatable_investiment_resume(self, type):
        '''
        Return a dataframe with describe by name.  
        '''
        df = self.resume.copy()
        df = df[(df['periodo_cont'] > 0) & (df['Tipo'] == type)].sort_values(['Nome', 'Data'])

        df = df\
            .groupby(['Nome'])\
            .agg(financeiro=('Financeiro', 'last'), 
                aporte=('aporte', 'sum'), 
                retirada=('retirada', 'sum'), 
                rendimento=('rendimento', 'sum'))\
            .reset_index()\
            .sort_values('financeiro', ascending=False)
        
        df['%'] = df['rendimento'] / df['aporte']
        df.fillna(0, inplace=True)

        return df


    def investiment_pie(self, type):
        '''
        Return a position investiment pie chart 
        '''

        df_pie = self.resume[self.resume['Tipo'] == type]\
            .groupby('Nome')\
            .agg(financeiro=('Financeiro', 'last'), 
                aporte=('aporte', 'sum'), 
                rendimento=('rendimento', 'sum'), 
                retirada=('retirada', 'sum'))\
            .reset_index()\
            .sort_values(by='financeiro', ascending=False)

        return charts.investiment_pie_chart(df_pie)


# RANKING PAGE

    def top_investiment(self, type):
        '''
            Return Ranking top 5 investiment by type
        '''
        df_ = self.resume[
            (self.resume['Tipo'] == type) & 
            (self.resume['Data'] == self.resume['Data'].max())
        ]

        df_ = df_[(df_['Financeiro'] > 0)].sort_values(by='%', ascending=False)
        print(df_.head(5))
        return df_.head(5)

    
    def tail_investiment(self, type):
        '''
            Return Ranking tail 5 investiment by type
        '''
        df_ = self.resume[
            (self.resume['Tipo'] == type) & 
            (self.resume['Data'] == self.resume['Data'].max())
        ]

        df_ = df_[(df_['Financeiro'] > 0)].sort_values(by='%', ascending=False)
        print(df_.tail(5))
        return df_.tail(5)
        
        