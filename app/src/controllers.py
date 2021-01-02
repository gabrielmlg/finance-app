from model import Posicao, Extrato, AwsModel
from views import FundoInvestimento, Acao, FundoImobiliario
from graphics import fis_graph


class MainController():
    def __init__(self):
        self.aws_model = AwsModel()
        self.aws_model.load_data_s3()

        self.posicao_model = Posicao(self.aws_model.df_list_pos) 
        self.extrato = Extrato(2010, 2020, self.aws_model.extrato, self.aws_model.extrato_bolsa)
        
        self.fundo_investimento = FundoInvestimento(
            posicao=self.posicao_model.fis, 
            extrato=self.extrato.extrato_fis
        )
        self.fundo_investimento.calcula_resumo(2010, 2020)   

        self.acoes = Acao(posicao=self.posicao_model.acoes, extrato=self.extrato.extrato_acoes)
        self.acoes.resumo = self.acoes.calcula_resumo(2010, 2020)

        self.fiis = FundoImobiliario(posicao=self.posicao_model.fiis, extrato=self.extrato.extrato_fiis)
        self.fiis.resumo = self.fiis.calcula_resumo(2010, 2020)

    def load_new_filter(self, de_ano, ate_ano):
        fi_resumo = self.fundo_investimento.resumo
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
        )


    def graph_fis(self):
        return fis_graph(self.posicao_model.fis)

