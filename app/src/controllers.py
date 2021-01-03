from model import Posicao, Extrato, AwsModel
from views import FundoInvestimento, Acao, FundoImobiliario
import graphics


class MainController():
    def __init__(self):
        self.aws_model = AwsModel()
        self.aws_model.load_data_s3()

        self.posicao_model = Posicao(self.aws_model.df_list_pos) 
        self.extrato = Extrato(2010, 2020, self.aws_model.extrato, self.aws_model.extrato_bolsa)
        
        self.fi = FundoInvestimento(
            posicao=self.posicao_model.fis, 
            extrato=self.extrato.extrato_fis
        )
        self.acoes = Acao(posicao=self.posicao_model.acoes, extrato=self.extrato.extrato_acoes)
        self.fiis = FundoImobiliario(posicao=self.posicao_model.fiis, extrato=self.extrato.extrato_fiis)


    def load_new_filter(self, de_ano, ate_ano):
        fi_resumo = self.fi.resumo
        acoes_resumo = self.acoes.resumo[self.acoes.resumo['Data'] <= '2020-11-30']
        fiis_resumo = self.fiis.resumo[self.fiis.resumo['Data'] <= '2020-11-30']

        total_aportes = self.extrato.total_investido()

        try: 
            total_aporte_fi = fi_resumo['aporte'].sum() - fi_resumo['retirada'].sum()
            rendimento_fi = fi_resumo['rendimento'].sum()
            rendimento_perc_fi = (rendimento_fi / total_aporte_fi) * 100
        except: 
            total_aporte_fi = 0 
            rendimento_fi = 0 
            rendimento_perc_fi = 0

        try: 
            total_aporte_acoes = self.acoes.total_aportes() 
            rendimento_acoes = acoes_resumo['rendimento'].sum()
            rend_acoes_perc = (rendimento_acoes / total_aporte_acoes) * 100
        except: 
            total_aporte_acoes = 0
            rendimento_acoes = 0
            rend_acoes_perc = 0

        try: 
            total_aporte_fiis = fiis_resumo['aporte'].sum() - fiis_resumo['retirada'].sum()
            rendimento_fiis = self.fiis.resumo['rendimento'].sum()
            rend_fiis_perc = (rendimento_fiis / total_aporte_fiis) * 100
        except: 
            total_aporte_fiis = 0
            rendimento_fiis = 0 
            rend_fiis_perc = 0


        return (
            "Total: R$ {:,.2f}".format(total_aportes), 
            "Ações: R$ {:,.2f}".format(total_aporte_acoes),
            "FIs: R$ {:,.2f}".format(total_aporte_fi),
            "FIIs: R$ {:,.2f}".format(total_aporte_fiis),
            
            "Total: R$ {:,.2f}".format(rendimento_fi + rendimento_acoes + rendimento_fiis),
            "Ações: R$ {:,.2f} ({:,.2f}%)".format(rendimento_acoes, rend_acoes_perc),  
            "FIs: R$ {:,.2f} ({:,.2f}%)".format(rendimento_fi, rendimento_perc_fi),  
            "FIIs: R$ {:,.2f} ({:,.2f}%)".format(rendimento_fiis, rend_fiis_perc),  
            
            
            "Total: R$ {:,.2f}".format(total_aportes + rendimento_acoes + rendimento_fi + rendimento_fiis),
            "Ações: R$ {:,.2f}".format(total_aporte_acoes + rendimento_acoes), 
            "FIs: R$ {:,.2f}".format(total_aporte_fi + rendimento_fi),
            "FIIs: R$ {:,.2f}".format(total_aporte_fiis + rendimento_fiis),  
            self.revenue_chart(), 
            self.revenue_cumsum_chart()
        )


    def graph_fis(self):
        return graphics.fis_graph(self.posicao_model.fis)

    def revenue_chart(self):
        df1 = self.acoes.resumo[self.acoes.resumo['Data'] <= '2020-11-30'].groupby(['Data', 'ano', 'mes'])\
        .agg(financeiro=('Financeiro', 'sum'), 
            aporte=('aporte', 'sum'), 
            retirada=('retirada', 'sum'), 
            rendimento=('rendimento', 'sum'))\
        .reset_index()

        df2 = self.fiis.resumo[self.fiis.resumo['Data'] <= '2020-11-30'].groupby(['Data', 'ano', 'mes'])\
        .agg(financeiro=('Financeiro', 'sum'), 
            aporte=('aporte', 'sum'), 
            retirada=('retirada', 'sum'), 
            rendimento=('rendimento', 'sum'))\
        .reset_index()  

        df3 = self.fi.resumo[self.fi.resumo['data_posicao'] <= '2020-11-30'].groupby(['data_posicao', 'ano', 'mes'])\
        .agg(financeiro=('Total Bruto', 'sum'), 
            aporte=('aporte', 'sum'), 
            retirada=('retirada', 'sum'), 
            rendimento=('rendimento', 'sum'))\
        .reset_index()\
        .rename(columns={'data_posicao': 'Data'})      

        df_graph1 = df1.append(df2, ignore_index=True).append(df3, ignore_index=True)
        df_graph1 = df_graph1.groupby(['Data', 'ano', 'mes'])\
                .agg(financeiro=('financeiro', 'sum'), 
                    aporte=('aporte', 'sum'), 
                    retirada=('retirada', 'sum'), 
                    rendimento=('rendimento', 'sum'))\
                .reset_index().fillna(0)

        df_graph1['%'] = df_graph1['rendimento'] / df_graph1['financeiro'] * 100
        df_graph1['renda_acum'] = df_graph1['rendimento'].cumsum()
        df_graph1['aporte_acum'] = df_graph1['aporte'].cumsum()
        df_graph1['retirada_acum'] = df_graph1['retirada'].cumsum()
        df_graph1['investido'] = df_graph1['aporte_acum'] - df_graph1['retirada_acum']
        df_graph1['% renda_acum'] = df_graph1['rendimento'].cumsum() / (df_graph1['investido']) * 100  
        df_graph1 = df_graph1.fillna(0)
        df_graph1 = df_graph1[(df_graph1['Data'] >= '2014-01-01')]

        return graphics.revenue_chart(df_graph1) 


    def revenue_cumsum_chart(self):
        df1 = self.acoes.resumo[self.acoes.resumo['Data'] <= '2020-11-30'].groupby(['Data', 'ano', 'mes'])\
        .agg(financeiro=('Financeiro', 'sum'), 
            aporte=('aporte', 'sum'), 
            retirada=('retirada', 'sum'), 
            rendimento=('rendimento', 'sum'))\
        .reset_index()

        df2 = self.fiis.resumo[self.fiis.resumo['Data'] <= '2020-11-30'].groupby(['Data', 'ano', 'mes'])\
        .agg(financeiro=('Financeiro', 'sum'), 
            aporte=('aporte', 'sum'), 
            retirada=('retirada', 'sum'), 
            rendimento=('rendimento', 'sum'))\
        .reset_index()  

        df3 = self.fi.resumo[self.fi.resumo['data_posicao'] <= '2020-11-30'].groupby(['data_posicao', 'ano', 'mes'])\
        .agg(financeiro=('Total Bruto', 'sum'), 
            aporte=('aporte', 'sum'), 
            retirada=('retirada', 'sum'), 
            rendimento=('rendimento', 'sum'))\
        .reset_index()\
        .rename(columns={'data_posicao': 'Data'})      

        df_graph1 = df1.append(df2, ignore_index=True).append(df3, ignore_index=True)
        df_graph1 = df_graph1.groupby(['Data', 'ano', 'mes'])\
                .agg(financeiro=('financeiro', 'sum'), 
                    aporte=('aporte', 'sum'), 
                    retirada=('retirada', 'sum'), 
                    rendimento=('rendimento', 'sum'))\
                .reset_index().fillna(0)

        df_graph1['%'] = df_graph1['rendimento'] / df_graph1['financeiro'] * 100
        df_graph1['renda_acum'] = df_graph1['rendimento'].cumsum()
        df_graph1['aporte_acum'] = df_graph1['aporte'].cumsum()
        df_graph1['retirada_acum'] = df_graph1['retirada'].cumsum()
        df_graph1['investido'] = df_graph1['aporte_acum'] - df_graph1['retirada_acum']
        df_graph1['% renda_acum'] = df_graph1['rendimento'].cumsum() / (df_graph1['investido']) * 100  
        df_graph1 = df_graph1.fillna(0)
        df_graph1 = df_graph1[(df_graph1['Data'] >= '2014-01-01')]

        return graphics.revenue_cumsum_chart(df_graph1)
