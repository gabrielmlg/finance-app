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



class Acao(Investimento):
    def __init__(self, posicao, extrato):
        self.posicao = posicao
        self.extrato = extrato
        super().__init__('Papel', 'Financeiro')

    def calcula_rentabilidade(self, do_ano, ate_ano):
        return super().calcula_rentabilidade(self.posicao, do_ano, ate_ano)



class FundoImobiliario(Investimento):
    def __init__(self, posicao, extrato):
        self.posicao = posicao
        self.extrato = extrato
        super().__init__('Papel', 'Financeiro')

    def calcula_rentabilidade(self, do_ano, ate_ano):
        return super().calcula_rentabilidade(self.posicao, do_ano, ate_ano)



class FundoInvestimento(Investimento):

    def __init__(self, posicao, extrato):
        self.posicao_hist = posicao
        self.extrato = extrato
        self.calcula_resumo(2010, 2020)


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
        end = datetime(int(datetime.now().year), 12, 31)
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
                        rendimento.append(df_[df_.index == row]['Total Bruto'].sum() - df_[df_.index == row]['aporte'].sum())
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
        self.resumo = df_return
        # return df_return


    def resumo_(self, do_ano, ate_ano):
        df_pos = self.calcula_rentabilidade(do_ano, ate_ano)
        df_pos['Data'] = df_pos['Data'].astype(np.datetime64)

        start = datetime(2010, 1, 1)
        end = datetime(int(datetime.now().year), 12, 31)
        ix_date = pd.bdate_range(start, end, freq='M')
        df_ixDate = pd.DataFrame(ix_date, columns=['Data'])
        df_ixDate['ano'] = df_ixDate['Data'].dt.year
        df_ixDate['mes'] = df_ixDate['Data'].dt.month

        df_tmp = pd.DataFrame([], columns=df_pos.columns)

        for fi in df_pos['Nome'].unique():
            df_pos_ = df_ixDate.merge(df_pos[df_pos['Nome'] ==  fi], 
                                    how='left', 
                                    left_on=['ano', 'mes'], 
                                    right_on=['ano', 'mes']).reset_index().fillna(0)
            df_pos_['Nome'] = fi
            df_pos_['mes'] = df_pos_['Data_x'].dt.month
            df_pos_['ano'] = df_pos_['Data_x'].dt.year
            df_pos_['data_posicao'] = df_pos_['Data_x']
            df_tmp = df_tmp.append(df_pos_)

        #print(df_date.head())


        #print(df_tmp[df_tmp['Nome'] == 'AZ Quest Multi FIC FIM'])
        #print(self.extrato.head())

        try: 
            resumo = self.extrato.merge(df_tmp, 
                             how='outer', 
                             left_on=['ano', 'mes', 'Nome'], 
                             right_on=['ano', 'mes', 'Nome'])

            #print(resumo[resumo['Nome'] == 'AZ Quest Multi FIC FIM'])

            resumo = resumo.groupby(['Nome', 'ano', 'mes', 'periodo_cont', 'data_posicao', 'Total Bruto'])\
                            .agg(aporte=('Vlr Aporte', 'sum'), 
                                retirada=('Vlr Resgate', 'sum'), 
                                rendimento_resgatado=('Rendimento Resgatado', 'sum'), 
                                rendimento_posicao=('rendimento', 'sum')).reset_index()

            resumo['ano'] = pd.to_numeric(resumo['ano'], downcast='signed')
            resumo['mes'] = pd.to_numeric(resumo['mes'], downcast='signed')
            resumo['periodo_cont'] = pd.to_numeric(resumo['periodo_cont'], downcast='signed')

            #resumo['rend_perc'] = resumo['rendimento_posicao'] / resumo['Valor Bruto']

        except:
            print('deu ruim')
            resumo = self.extrato.loc[:, self.extrato.columns.union(df_tmp.columns)] #self.extrato.reindex_axis(self.extrato.columns.union(df_pos.columns), axis=1)

        return resumo

    
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



