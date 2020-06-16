import pandas as pd
import os
import xlrd
import numpy as np

from classes.views import Posicao, Extrato
#from views import Posicao, Extrato


class PosicaoRepository:

    files = os.listdir('./datasets/posicao/')
    posicao = Posicao()

    acoes = pd.DataFrame()
    dividendo_acoes = pd.DataFrame()
    fis = pd.DataFrame()
    fiis = pd.DataFrame()
    dividendo_fiis = pd.DataFrame()

    def load_data(self):
        
        for file_name in self.files:
            if file_name == '.DS_Store':
                continue
            
            wb = xlrd.open_workbook('./datasets/posicao/' + file_name, logfile=open(os.devnull, 'w'))
            df = pd.read_excel(wb)
            
            #df = pd.read_excel('../datasets/' + file_name)
            date_position = df[df['Unnamed: 56'].str.contains('Data de referência', na=False)]['Unnamed: 56']
            
            # position date
            date_position = pd.to_datetime(date_position.str.replace('Data de referência: ', ''), format='%d/%m/%Y')
            
            month = int(date_position.dt.month.values)
            year = int(date_position.dt.year.values)
            period = str(year) + '/' + str(month)
            dt_posicao = date_position.values[0]

            df_stocks = self.posicao.get_acoes(df)
            df_stocks['period'] = period
            df_stocks['mes'] = month
            df_stocks['ano'] = year
            df_stocks['data_posicao'] = dt_posicao
            self.acoes = self.acoes.append(df_stocks, ignore_index=True)

            df_pickings = self.posicao.get_acoes_provento(df)
            df_pickings['period'] = period
            df_pickings['mes'] = month
            df_pickings['ano'] = year
            df_pickings['data_posicao'] = dt_posicao
            self.dividendo_acoes = self.dividendo_acoes.append(df_pickings, ignore_index=True)

            df_fi = self.posicao.get_fi(df)
            df_fi['period'] = period
            df_fi['mes'] = month
            df_fi['ano'] = year
            df_fi['data_posicao'] = dt_posicao
            self.fis = self.fis.append(df_fi, ignore_index=True)

            df_fii = self.posicao.get_fii(df)
            df_fii['period'] = period
            df_fii['mes'] = month
            df_fii['ano'] = year
            df_fii['data_posicao'] = dt_posicao
            self.fiis = self.fiis.append(df_fii, ignore_index=True)

            df_picking_fii = self.posicao.get_fii_proventos(df)
            df_picking_fii['period'] = period
            df_picking_fii['mes'] = month
            df_picking_fii['ano'] = year
            df_picking_fii['data_posicao'] = dt_posicao
            self.dividendo_fiis = self.dividendo_fiis.append(df_picking_fii, ignore_index=True)


class ExtratoRepository:
    def load_csv_extrato(self):
        df = pd.read_csv('./datasets/extrato/Extrato 200091 JAN 2010 a JUN 2020.csv', sep=';', encoding='iso-8859-1', decimal=',')
        df['Mov'] = pd.to_datetime(df['Mov'], format='%d/%m/%Y')
        df['Liq'] = pd.to_datetime(df['Liq'], format='%d/%m/%Y')
        df.rename(columns={'Hist__o': 'Descricao'}, inplace=True)

        return df