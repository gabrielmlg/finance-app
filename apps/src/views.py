from numpy.lib.function_base import extract
import pandas as pd
import numpy as np
from datetime import datetime


class Investimento():
    def __init__(self, nome_col_tipo, nome_col_valor):
        self.nome_col_tipo = nome_col_tipo
        self.nome_col_valor = nome_col_valor


    # Calcula a rentabilidade da posicao de açoes
    def calcula_rentabilidade(self, posicao, do_ano, ate_ano):
        df = posicao[(posicao['ano'] >= do_ano) &  
                                (posicao['ano'] <= ate_ano)]

        df_return = pd.DataFrame([], columns=df.columns)

        for ativo in df[self.nome_col_tipo].unique():
            df_ = df[df[self.nome_col_tipo] == ativo].sort_values(by=['data_posicao']).reset_index()
            rendimento = []

            for row in df_.index:
                if row == 0:
                    rendimento.append(0)
                else:
                    valor = df_[df_.index == row][self.nome_col_valor].sum() - df_[df_.index == row -1][self.nome_col_valor].sum()
                    rendimento.append(valor)

            df_['rendimento'] = rendimento
            df_['rendimento_acum'] = df_['rendimento'].cumsum()
            df_return = df_return.append(df_)

        return df_return


    def __reshape_extrato(self):
        tmp = self.extrato.pivot_table(index=['Papel', 'ano', 'mes', 'Data'], columns=['Tipo'], aggfunc=np.sum, fill_value=0).reset_index()
        tmp['total_compra'] = tmp.Preco.COMPRA * tmp.Qtde.COMPRA
        tmp['total_venda'] = tmp.Preco.VENDA * tmp.Qtde.VENDA

        return pd.DataFrame({
            'Papel': tmp['Papel'], 
            'Data': tmp['Data'], 
            'ano': tmp['ano'], 
            'mes': tmp['mes'], 
            'aporte': tmp['total_compra'], 
            'retirada': tmp['total_venda']
        })


    def calcula_resumo(self, data_ini, data_fim):

        df_pos = self.posicao[self.posicao['ano'] <= data_fim]
        df_pos['data_posicao'] = df_pos['data_posicao'].astype(np.datetime64)

        start = datetime(2010, 1, 1)
        end = datetime(data_fim, 12, 31)
        ix_date = pd.bdate_range(start, end, freq='M')
        df_ixDate = pd.DataFrame(ix_date, columns=['Data'])
        df_ixDate['ano'] = df_ixDate['Data'].dt.year
        df_ixDate['mes'] = df_ixDate['Data'].dt.month

        df_tmp = pd.DataFrame([], columns=df_pos.columns)

        for papel in df_pos[self.nome_col_tipo].unique():
            df_pos_ = df_ixDate.merge(df_pos[df_pos[self.nome_col_tipo] ==  papel], 
                                    how='left', 
                                    left_on=['ano', 'mes'], 
                                    right_on=['ano', 'mes']).reset_index().fillna(0)
            df_pos_[self.nome_col_tipo] = papel
            df_tmp = df_tmp.append(df_pos_)

        df_ext = self.__reshape_extrato()

        resumo = df_tmp.merge(df_ext, 
                    how='left', 
                    left_on=['ano', 'mes', self.nome_col_tipo], 
                    right_on=['ano', 'mes', self.nome_col_tipo]
                    ).fillna(0).rename(columns={'Data_x': 'Data'})

        resumo = resumo.groupby([self.nome_col_tipo, 'ano', 'mes', 'Data', 'Financeiro'])\
                        .agg(aporte=('aporte', 'sum'), 
                            retirada=('retirada', 'sum')).reset_index()

        resumo['ano'] = pd.to_numeric(resumo['ano'], downcast='signed')
        resumo['mes'] = pd.to_numeric(resumo['mes'], downcast='signed')

        df_return = pd.DataFrame([])

        for ativo in resumo[self.nome_col_tipo].unique():
            df_ = resumo[resumo[self.nome_col_tipo] == ativo].sort_values(by=['Data']).reset_index()
            rendimento = []
            rendimento_percent = []
            periodo_cont = []
            count = 0

            for row in df_.index:
                if (df_[df_.index == row]['Financeiro'].sum() > 1) | (df_[df_.index == row]['retirada'].sum() > 1):
                    if count == 0: # primeiro rendimento
                        count += 1
                        rend_ = df_[df_.index == row]['Financeiro'].sum() - df_[df_.index <= row]['aporte'].sum()
                        if df_[df_.index <= row]['aporte'].sum() > 0:
                            rend_per_ = rend_ / df_[df_.index <= row]['aporte'].sum() * 100
                        else:
                            rend_per_ = 0

                        rendimento.append(rend_)
                        rendimento_percent.append(rend_per_)
                        periodo_cont.append(1)
                    else:
                        count += 1
                        valor = df_[df_.index == row]['Financeiro'].sum() + df_[df_.index == row]['retirada'].sum() - df_[df_.index == row -1]['Financeiro'].sum() - df_[df_.index == row]['aporte'].sum()
                        rend_per_ = valor / df_[df_.index == row - 1]['Financeiro'].sum() * 100
                        rendimento.append(valor)
                        rendimento_percent.append(rend_per_)
                        periodo_cont.append(count)
                        
                else:
                    rendimento.append(0)
                    rendimento_percent.append(0)
                    periodo_cont.append(0)
                    count = 0

            df_['rendimento'] = rendimento
            df_['rendimento_percent'] = rendimento_percent
            df_['periodo_cont'] = periodo_cont
            #df_['rendimento_acum'] = df_['rendimento'].cumsum()
            df_return = df_return.append(df_)

        return df_return



class Acao(Investimento):
    def __init__(self, posicao, extrato, dividendo):
        self.posicao = posicao
        self.extrato = extrato
        self.dividendo = dividendo
        super().__init__('Papel', 'Financeiro')
        self.resumo = self.calcula_resumo(2010, 2021)


    
    def calcula_rentabilidade(self, do_ano, ate_ano):
        return super().calcula_rentabilidade(self.posicao, do_ano, ate_ano)

    
    def calcula_resumo(self, data_ini, data_fim):

        df_pos = self.posicao[self.posicao['ano'] <= data_fim]
        df_pos['data_posicao'] = df_pos['data_posicao'].astype(np.datetime64)

        #print(df_pos[['Papel', 'data_posicao', 'Financeiro']].sort_values(['Papel', 'data_posicao']))

        start = datetime(2010, 1, 1)
        end = datetime(data_fim, 12, 31)
        ix_date = pd.bdate_range(start, end, freq='M')
        df_ixDate = pd.DataFrame(ix_date, columns=['Data'])
        df_ixDate['ano'] = df_ixDate['Data'].dt.year
        df_ixDate['mes'] = df_ixDate['Data'].dt.month

        df_tmp = pd.DataFrame([], columns=df_pos.columns)

        for papel in df_pos['Papel'].unique():
            df_pos_ = df_ixDate.merge(df_pos[df_pos['Papel'] ==  papel], 
                                    how='left', 
                                    left_on=['ano', 'mes'], 
                                    right_on=['ano', 'mes']).reset_index().fillna(0)
            df_pos_['Papel'] = papel
            df_tmp = df_tmp.append(df_pos_)

        df_ext = self.__reshape_extrato()

        resumo = df_tmp.merge(df_ext, 
                    how='left', 
                    left_on=['ano', 'mes', 'Papel'], 
                    right_on=['ano', 'mes', 'Papel']
                    ).fillna(0).rename(columns={'Data_x': 'Data'})

        #print(resumo[['Papel', 'ano', 'mes', 'Data', 'Financeiro', 'aporte', 'retirada']])

        resumo = resumo.groupby(['Papel', 'ano', 'mes', 'Data', 'Financeiro'])\
                        .agg(aporte=('aporte', 'sum'), 
                            retirada=('retirada', 'sum')).reset_index()

        resumo['ano'] = pd.to_numeric(resumo['ano'], downcast='signed')
        resumo['mes'] = pd.to_numeric(resumo['mes'], downcast='signed')
        resumo['Tipo'] = np.where(resumo['Papel'].str.contains('34'), 
                                'BDR', 
                                'Ação')

        df_return = pd.DataFrame([])

        for ativo in resumo['Papel'].unique():
            df_ = resumo[resumo['Papel'] == ativo].sort_values(by=['Data']).reset_index()
            rendimento = []
            rendimento_percent = []
            periodo_cont = []
            count = 0

            for row in df_.index:
                if (df_[df_.index == row]['Financeiro'].sum() > 1) | (df_[df_.index == row]['retirada'].sum() > 1):
                    if count == 0: # primeiro rendimento
                        count += 1
                        rend_ = df_[df_.index == row]['Financeiro'].sum() - df_[df_.index <= row]['aporte'].sum()
                        rend_per_ = rend_ / df_[df_.index <= row]['aporte'].sum() * 100

                        rendimento.append(rend_)
                        rendimento_percent.append(rend_per_)
                        periodo_cont.append(1)
                    else:
                        count += 1
                        valor = df_[df_.index == row]['Financeiro'].sum() + df_[df_.index == row]['retirada'].sum() - df_[df_.index == row -1]['Financeiro'].sum() - df_[df_.index == row]['aporte'].sum()
                        rend_per_ = valor / df_[df_.index == row - 1]['Financeiro'].sum() * 100
                        rendimento.append(valor)
                        rendimento_percent.append(rend_per_)
                        periodo_cont.append(count)
                        
                else:
                    rendimento.append(0)
                    rendimento_percent.append(0)
                    periodo_cont.append(0)
                    count = 0

            df_['rendimento'] = rendimento
            df_['rendimento_percent'] = rendimento_percent
            df_['periodo_cont'] = periodo_cont
            #df_['rendimento_acum'] = df_['rendimento'].cumsum()
            df_return = df_return.append(df_)

        return df_return

    def total_aportes(self, tipo):
        return self.resumo[self.resumo['Tipo'] == tipo]['aporte'].sum() \
                - self.resumo[self.resumo['Tipo'] == tipo]['retirada'].sum()


    def __reshape_extrato(self):

        tmp = self.extrato.pivot_table(index=['Papel', 'ano', 'mes', 'Data'], columns=['Tipo'], aggfunc=np.sum, fill_value=0).reset_index()
        tmp['total_compra'] = tmp.Preco.COMPRA * tmp.Qtde.COMPRA
        tmp['total_venda'] = tmp.Preco.VENDA * tmp.Qtde.VENDA

        return pd.DataFrame({
            'Papel': tmp['Papel'], 
            'Data': tmp['Data'], 
            'ano': tmp['ano'], 
            'mes': tmp['mes'], 
            'aporte': tmp['total_compra'], 
            'retirada': tmp['total_venda']
        })



class FundoImobiliario(Investimento):
    def __init__(self, posicao, extrato, dividendo):
        self.posicao = posicao
        self.extrato = extrato
        self.dividendo = dividendo
        super().__init__('Papel', 'Financeiro')
        self.resumo = self.calcula_resumo(2010, 2021)

    def calcula_rentabilidade(self, do_ano, ate_ano):
        return super().calcula_rentabilidade(self.posicao, do_ano, ate_ano)

    def calcula_resumo(self, data_ini, data_fim):
        return super().calcula_resumo(data_ini, data_fim)



class FundoInvestimento(Investimento):

    def __init__(self, posicao, extrato):
        self.posicao_hist = posicao
        self.extrato = extrato
        self.resumo = self.calcula_resumo(2010, 2021)


    # Calcula o rendimendo de ativo FI para cada periodo. 
    # Retorna o dataset com o campo rendimento e rendimento acumulado. 
    def calcula_rentabilidade(self, do_ano, ate_ano):
        df = self.posicao_hist[(self.posicao_hist['ano'] >= do_ano) &  
                                (self.posicao_hist['ano'] <= ate_ano)]

        df_return = pd.DataFrame([], columns=df.columns)

        for ativo in df['Nome'].unique():
            df_ = df[df['Nome'] == ativo].sort_values(by=['data_posicao']).reset_index()
            rendimento = []
            periodo_cont = []
            count = 1

            for row in df_.index:
                if row == 0:
                    rendimento.append(0)
                    periodo_cont.append(1)
                    count += 1
                else:
                    valor = df_[df_.index == row]['Valor Bruto'].sum() - df_[df_.index == row -1]['Valor Bruto'].sum()
                    rendimento.append(valor)
                    periodo_cont.append(count)
                    count += 1

            df_['rendimento'] = rendimento
            df_['periodo_cont'] = periodo_cont
            df_['rendimento_acum'] = df_['rendimento'].cumsum()
            df_return = df_return.append(df_)

        return df_return


    def calcula_resumo(self, do_ano, ate_ano):
        
        df = self.posicao_hist[(self.posicao_hist['ano'] >= do_ano) &  
                                (self.posicao_hist['ano'] <= ate_ano)]
        df['Data'] = df['Data'].astype(np.datetime64)

        start = datetime(2010, 1, 1)
        end = datetime(ate_ano, 12, 31)
        ix_date = pd.bdate_range(start, end, freq='M')
        df_ixDate = pd.DataFrame(ix_date, columns=['Data'])
        df_ixDate['ano'] = df_ixDate['Data'].dt.year
        df_ixDate['mes'] = df_ixDate['Data'].dt.month

        df_tmp = pd.DataFrame([], columns=df.columns)

        for fi in df['Nome'].unique():
            df_pos_ = df_ixDate.merge(df[df['Nome'] ==  fi], 
                                    how='left', 
                                    left_on=['ano', 'mes'], 
                                    right_on=['ano', 'mes']).reset_index().fillna(0)
            df_pos_['Nome'] = fi
            df_pos_['mes'] = df_pos_['Data_x'].dt.month
            df_pos_['ano'] = df_pos_['Data_x'].dt.year
            df_pos_['data_posicao'] = df_pos_['Data_x']
            df_tmp = df_tmp.append(df_pos_)

        resumo = self.extrato.merge(df_tmp, 
                            how='outer', 
                            left_on=['ano', 'mes', 'Nome'], 
                            right_on=['ano', 'mes', 'Nome'])

        #print(resumo[resumo['Nome'] == 'AZ Quest Multi FIC FIM'])

        resumo = resumo.groupby(['Nome', 'ano', 'mes', 'data_posicao', 'Total Bruto'])\
                        .agg(aporte=('Vlr Aporte', 'sum'), 
                            retirada=('Vlr Resgate', 'sum'), 
                            rendimento_resgatado=('Rendimento Resgatado', 'sum')).reset_index()

        resumo['ano'] = pd.to_numeric(resumo['ano'], downcast='signed')
        resumo['mes'] = pd.to_numeric(resumo['mes'], downcast='signed')

        df_return = pd.DataFrame([], columns=df.columns)

        for ativo in resumo['Nome'].unique():
            df_ = resumo[resumo['Nome'] == ativo].sort_values(by=['data_posicao']).reset_index()
            rendimento = []
            periodo_cont = []
            count = 0

            for row in df_.index:
                if (df_[df_.index == row]['Total Bruto'].sum() > 1) | (df_[df_.index == row]['retirada'].sum() > 1):
                    if count == 0: # primeiro rendimento
                        count += 1
                        rendimento.append(df_[df_.index == row]['Total Bruto'].sum() - df_[df_.index <= row]['aporte'].sum())
                        periodo_cont.append(1)
                    else:
                        count += 1
                        valor = df_[df_.index == row]['Total Bruto'].sum() + df_[df_.index == row]['rendimento_resgatado'].sum() - df_[df_.index == row -1]['Total Bruto'].sum() - df_[df_.index == row]['aporte'].sum()
                        rendimento.append(valor)
                        periodo_cont.append(count)
                        
                else:
                    rendimento.append(0)
                    periodo_cont.append(0)
                    count = 0

            df_['rendimento'] = rendimento
            df_['periodo_cont'] = periodo_cont
            #df_['rendimento_acum'] = df_['rendimento'].cumsum()
            df_return = df_return.append(df_)
            
        df_return.drop(columns=['Data', 'Qtd Cotas', 'Valor Cota', 'Valor Bruto', 'IR', 'IOF', 'Valor Liquido', 'period', 'Aplicacao Pendente'], inplace=True)

        return df_return
        # return df_return

    
    # POSSIVEIS METODOS PARA ABSTRAIR

    def periodos(self):
        return self.posicao_hist.sort_values('Data')['Data'].dt.year.unique()

    
    def total_aportes(self):
        return self.resumo['aporte'].sum() - self.resumo['retirada'].sum()


    def total_resgatado(self):
        return self.resumo['rendimento_resgatado'].sum()


    def total_ir(self):
        return self.extrato['Vlr IR'].sum()


    def lucro_resgatado(self):
        return self.extrato['Rendimento Resgatado'].sum()



