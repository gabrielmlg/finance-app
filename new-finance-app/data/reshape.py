from datetime import datetime
from data.source import Position, Extract
import numpy as np
import pandas as pd

from components import utils

class Transform:

    def __init__(self):
        None

    def append_investiments(self, position, extract):
        df1 = position.stocks[['Papel', 'Qtd Disponivel',
                    'Cotacao', 'Financeiro', 'period', 'mes', 'ano',
                    'data_posicao']]
        df1['Tipo'] = np.where(df1['Papel'].str.contains('34'), 
                                'BDR', 
                                'Ação')

        df2 = position.fiis[['Papel', 'Qtd Disponivel', 
                    'Ult Cotacao', 'Financeiro', 'period', 'mes', 'ano', 
                    'data_posicao']]\
                .rename(columns={'Ult Cotacao': 'Cotacao'})
        df2['Tipo'] = 'FII'

        
        df2['Financeiro'] = np.where(df2['Financeiro'] == 0, 
                df2['Qtd Disponivel'] * df2['Cotacao'], 
                df2['Financeiro']) # trata os valores vazios de Financeiro. 

        # ToDo: Depois acrescentar esses campos: 'IR', 'IOF', 'Valor Liquido'
        df3 = position.fis[['Nome', 'Qtd Cotas', 'Valor Cota', 'Valor Bruto', 
                            'period', 'mes',
                            'ano', 'data_posicao']]\
                    .rename(columns={'Nome': 'Papel',
                                    'Qtd Cotas': 'Qtd Disponivel', 
                                    'Valor Cota': 'Cotacao', 
                                    'Valor Bruto': 'Financeiro'})                            
        df3['Tipo'] = 'FI'

        df4 = position.stocks_profits\
                .groupby(['Papel', 'data_posicao'])\
                    .agg(Valor=('Valor', 'sum'))\
                .reset_index()

        df5 = extract.fiis_profits\
                    .groupby(['Descricao', 'ano', 'mes'])\
                        .agg(Valor=('Valor', 'sum'))\
                    .reset_index()\
                    .rename(columns={'Descricao': 'Papel'})

        #print(df1[df1['data_posicao'].isnull()].head())
        #print(df2[df2['data_posicao'].isnull()].head())
        #print(df3[df3['data_posicao'].isnull()].head())
        #print(df1[df4['data_posicao'].isnull()].head())
        
        df_result = df1.append(df2, ignore_index=True).append(df3, ignore_index=True)   


        df_result = df_result.merge(df4, 
                                how='outer', 
                                left_on=['Papel', 'data_posicao'], 
                                right_on=['Papel', 'data_posicao'])\
                            .fillna(0)
                            
        df_result = df_result.merge(df5, 
                                how='left', # existem dividendos de periodos sem posicao ex.: BCFF11
                                left_on=['Papel', 'ano', 'mes'], 
                                right_on=['Papel', 'ano', 'mes'])\
                            .fillna(0)
        df_result['dividendo'] = df_result['Valor_x'] + df_result['Valor_y']
        df_result.drop(columns=['Valor_x', 'Valor_y'], inplace=True)

        return df_result
        #df_result.sort_values(by=['data_posicao', 'Papel']).tail()

    
    def transform_extract_stocks(self, extract):
        
        #Estou aqui!! Todo:
        #[] Renomear a coluna Tipo para outro nome para poder criar a coluna 'Tipo'
        # [] Criar a coluna 'Tipo'
        stocks = extract.extrato_acoes.copy()
        stocks.rename(columns={'Tipo': 'Operacao'}, inplace=True)
        stocks['Tipo'] = np.where(stocks['Papel'].str.contains('34'), 
                                'BDR', 
                                'Ação')

        fiis = extract.extrato_fiis.copy()
        fiis.rename(columns={'Tipo': 'Operacao'}, inplace=True)
        fiis['Tipo'] = 'FII'

        df1 = stocks.append(fiis, ignore_index=True)

        tmp = df1.pivot_table(index=['Tipo', 'Papel', 'ano', 'mes'], columns=['Operacao'], aggfunc=np.sum, fill_value=0).reset_index()
        tmp['total_compra'] = tmp.Preco.COMPRA * tmp.Qtde.COMPRA
        tmp['total_venda'] = tmp.Preco.VENDA * tmp.Qtde.VENDA
        tmp['data_posicao'] = tmp.apply(lambda x: utils.last_day_of_month(datetime(x['ano'], x['mes'], 1)), axis=1)
 
        return pd.DataFrame({
            'Tipo': tmp['Tipo'], 
            'Papel': tmp['Papel'],
            'ano': tmp['ano'], 
            'mes': tmp['mes'], 
            'data_posicao': tmp['data_posicao'], 
            'aporte': tmp['total_compra'], 
            'retirada': tmp['total_venda']
        })


    def resume(self, position, extract):
        features = self.append_investiments(position, extract)
        stock_extract = self.transform_extract_stocks(extract)

        # merge cash in e out by stocks and fiis
        df1 = features.merge(stock_extract, 
            how='outer', 
            left_on=['Tipo', 'Papel', 'ano', 'mes', 'data_posicao'], 
            right_on=['Tipo', 'Papel', 'ano', 'mes', 'data_posicao']).fillna(0).reset_index()\
                .rename(columns={'data_posicao': 'Data'})
        
        df2 = extract.extract_fis.rename(columns={
            'Nome': 'Papel'#, 
            #'Vlr Aporte': 'aporte', 
            #'Vlr Resgate': 'retirada'
        })

        df2 = df2.groupby(['Tipo', 'Papel', 'ano', 'mes', 'Data'])\
                .agg(vlr_aporte=('Vlr Aporte', 'sum'), 
                    vlr_resgate=('Vlr Resgate', 'sum'), 
                    rendimento_resgatado=('Rendimento Resgatado', 'sum')).reset_index()

        df3 = df1.merge(df2, 
                how='outer', 
                left_on=['ano', 'mes', 'Papel', 'Tipo', 'Data'], 
                right_on=['ano', 'mes', 'Papel', 'Tipo', 'Data']).fillna(0)

        df3['aporte'] = df3['vlr_aporte'] + df3['aporte']
        df3['retirada'] = df3['vlr_resgate'] + df3['retirada']
        df3.drop(columns=['vlr_aporte', 'vlr_resgate'], inplace=True)

        df_return = pd.DataFrame([])

        for ativo in df3['Papel'].unique():
            df_ = df3[df3['Papel'] == ativo].sort_values(by=['ano', 'mes']).reset_index()
            #print(df_.head())
            rendimento = []
            rendimento_percent = []
            periodo_cont = []
            count = 0

            for row in df_.index:
                if (df_[df_.index == row]['Financeiro'].sum() > 1)\
                        | (df_[df_.index == row]['retirada'].sum() > 1)\
                        | (df_[df_.index == row]['aporte'].sum() > 1):
                    if count == 0: # primeiro rendimento
                        count += 1
                        
                        if df_[df_.index == row]['Financeiro'].sum() > 0:
                            rend_ = df_[df_.index == row]['Financeiro'].sum() - df_[df_.index <= row]['aporte'].sum()
                        else: 
                            rend_ = 0 #df_[df_.index <= row]['aporte'].sum()
                        
                        if df_[df_.index <= row]['aporte'].sum() > 0:
                            rend_per_ = rend_ / df_[df_.index <= row]['aporte'].sum() * 100
                        else: rend_per_ = 0

                        rendimento.append(rend_)
                        rendimento_percent.append(rend_per_)
                        periodo_cont.append(1)
                    else:
                        count += 1
                        if (df_[df_.index == row]['Financeiro'].sum() > 0)\
                            & (df_[df_.index == row -1]['Financeiro'].sum() == 0): # segunda linha (segundo mes de invetimento)
                            valor = df_[df_.index == row]['Financeiro'].sum()\
                                        + df_[df_.index <= row]['retirada'].sum()\
                                        - df_[df_.index == row -1]['Financeiro'].sum()\
                                        - df_[df_.index <= row]['aporte'].sum()
                        
                        elif (df_[df_.index == row]['Financeiro'].sum() > 0)\
                            & (df_[df_.index == row -1]['Financeiro'].sum() > 0):
                            valor = df_[df_.index == row]['Financeiro'].sum()\
                                        + df_[df_.index == row]['retirada'].sum()\
                                        - df_[df_.index == row -1]['Financeiro'].sum()\
                                        - df_[df_.index == row]['aporte'].sum()
                        
                        elif (df_[df_.index == row]['Financeiro'].sum() == 0)\
                            & (df_[df_.index == row]['retirada'].sum() > 0)\
                            & (df_[df_.index == row -1 ]['Financeiro'].sum() > 0):
                            valor = df_[df_.index == row]['retirada'].sum()\
                                 - df_[df_.index == row -1 ]['Financeiro'].sum()
                        
                        else: 
                            valor = 0

                        if df_[df_.index == row - 1]['Financeiro'].sum() > 0: 
                            rend_per_ = valor / df_[df_.index == row - 1]['Financeiro'].sum() * 100
                        elif df_[df_.index == row]['Financeiro'].sum() > 0:
                            rend_per_ = valor / df_[df_.index <= row]['aporte'].sum() * 100
                        else: 
                            rend_per_ = 0
                        #rend_per_ = valor / df_[df_.index == row - 1]['Financeiro'].sum() * 100
                        rendimento.append(valor)
                        rendimento_percent.append(rend_per_)
                        periodo_cont.append(count)
                        
                else:
                    rendimento.append(0)
                    rendimento_percent.append(0)
                    periodo_cont.append(0)
                    count = 0

            df_['rendimento'] = rendimento
            df_['%'] = rendimento_percent
            df_['periodo_cont'] = periodo_cont
            #df_['rendimento_acum'] = df_['rendimento'].cumsum()
            df_return = df_return.append(df_)

        df_return.rename(columns={'Papel': 'Nome'}, inplace=True)
        
        #Coorreções manuais:
        df_return[(df_return['Nome'] == 'BCFF11') & (df_return['Data'] == '2014-05-31')]['rendimento'] = 0
        df_return = df_return[
            df_return['Data'] >= '2014-08-01'
        ]  

        return df_return