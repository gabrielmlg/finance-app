from classes.model import Posicao, Extrato
from classes.views import FundoInvestimento, Acao, FundoImobiliario
from classes.graphics import fis_graph

class MainController():
    def __init__(self):
        self.posicao_model = Posicao() 
        self.posicao_model.load_data()
        self.extrato = Extrato(2010, 2020)
        self.fundo_investimento = FundoInvestimento(
            posicao=self.posicao_model.fis, 
            extrato=self.extrato.extrato_fis
        )
        self.acoes = Acao(posicao=self.posicao_model.acoes, extrato=self.extrato.df)
        self.fiis = FundoImobiliario(posicao=self.posicao_model.fiis, extrato=self.extrato.df)

    def load_new_filter(self, de_ano, ate_ano):
        self.extrato = Extrato(2010, ate_ano)
        self.fundo_investimento.calcula_resumo(2010, ate_ano)       
        resumo = self.fundo_investimento.resumo
        print(resumo[resumo['periodo_cont'] >= 1]['data_posicao'].max())
        total_aportes = self.extrato.total_investido()

        try: 
            total_aporte_fi = self.fundo_investimento.total_aportes() 
            print('Total: {} - {}'.format(total_aporte_fi, resumo['aporte'].sum() - resumo['retirada'].sum()))
            rendimento_fi = resumo['rendimento'].sum()
            rendimento_perc_fi = (rendimento_fi / total_aporte_fi) * 100
        except: 
            print('ERRO')
            total_aporte_fi = 0
            rendimento_fi = 0 
            rendimento_perc_fi = 0

        try: 
            rendimento_acoes = self.acoes.calcula_rentabilidade(de_ano, ate_ano)['rendimento'].sum() 
        except: 
            rendimento_acoes = 0

        try: 
            rendimento_fiis = self.fiis.calcula_rentabilidade(de_ano, ate_ano)['rendimento'].sum() 
        except: 
            rendimento_fiis = 0 

        return (
            "Total: R$ {:,.2f}".format(total_aportes), 
            "Fundos de Investimento: R$ {:,.2f}".format(total_aporte_fi),
            "Total: R$ {:,.2f}".format(rendimento_fi + rendimento_acoes + rendimento_fiis),
            "Fundos de Investimento: R$ {:,.2f} ({:,.2f}%)".format(rendimento_fi, rendimento_perc_fi),  
            "Total: R$ {:,.2f}".format(total_aportes + rendimento_fi),
            "Fundos de Investimento: R$ {:,.2f}".format(total_aporte_fi + rendimento_fi),
            "Ações: R$ {:,.2f}".format(rendimento_acoes),  
            "Fundos Imobiliários: R$ {:,.2f}".format(rendimento_fiis),  
        )


    def graph_fis(self):
        return fis_graph(self.posicao_model.fis)

