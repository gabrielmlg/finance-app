from datetime import datetime
import pandas as pd
import os
import xlrd
import numpy as np

import boto3
import io

from components import utils

# LOCAL
from config import config
ACCESS_KEY= config.AWS_ACCESS_KEY_ID_GABRIEL # os.getenv('AWS_ACCESS_KEY_ID') 
SECRET_KEY= config.AWS_SECRET_KEY_ID_GABRIEL # os.getenv('AWS_SECRET_KEY_ID')  

#ACCESS_KEY= os.getenv('AWS_ACCESS_KEY_ID') 
#SECRET_KEY= os.getenv('AWS_SECRET_KEY_ID')  

bucket= 'balbi-finance-app'


class AwsClient:
    def __init__(self):
        self.extrato = pd.DataFrame()
        self.extrato_bolsa = pd.DataFrame()
        self.df_list_pos = []

    def load_data_s3(self):
        s3 = boto3.client(
            's3', 
            region_name='us-east-1', 
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )

        response = s3.list_objects(Bucket=bucket)
        request_files = response["Contents"]
        for file in request_files:
            obj = s3.get_object(Bucket=bucket, Key=file["Key"])
            if file["Key"].find('datasets/posicao/') >= 0:
                #print('Posicao: {}'.format(file["Key"]))
                df_pos_ = pd.read_excel(obj['Body'].read())
                self.df_list_pos.append(df_pos_)
            elif file["Key"].find('datasets/extrato/Extrato.csv') >= 0:
                #print('Extrato: {}'.format(file["Key"]))
                self.extrato = pd.read_csv(obj["Body"], sep=';', decimal=',', encoding='utf-8')
            elif file["Key"].find('datasets/acoes/extrato_acoes.xlsx') >= 0:
                #print('Extrato ações: {}'.format(file["Key"]))
                #df_extacoes = pd.read_excel(obj["Body"], sheet_name='Planilha2')
                self.extrato_bolsa = pd.read_excel(io.BytesIO(obj['Body'].read()), sheet_name='Planilha2')


class Position:

    def __init__(self, df_list_pos):
        self.df_list_pos = df_list_pos
        self.stocks = pd.DataFrame()
        self.stocks_profits = pd.DataFrame()
        self.fis = pd.DataFrame()
        self.fiis = pd.DataFrame()
        self.fiis_profits = pd.DataFrame()
        self.__load()


    def __load(self):
        for df in self.df_list_pos:
            date_position = df[df['Unnamed: 56'].str.contains('Data de referência', na=False)]['Unnamed: 56']
            
            # position date
            date_position = pd.to_datetime(date_position.str.replace('Data de referência: ', ''), format='%d/%m/%Y')
            month = int(date_position.dt.month.values)
            year = int(date_position.dt.year.values)
            period = str(year) + '/' + str(month)
            dt_position = date_position.values[0]

            df_stocks = self.__get_stocks(df)
            df_stocks['period'] = period
            df_stocks['mes'] = month
            df_stocks['ano'] = year
            df_stocks['data_posicao'] = dt_position
            self.stocks = self.stocks.append(df_stocks, ignore_index=True)

            df_pickings = self.__get_stocks_profits(df)
            df_pickings['period'] = period
            df_pickings['mes'] = month
            df_pickings['ano'] = year
            df_pickings['data_posicao'] = dt_position
            self.stocks_profits = self.stocks_profits.append(df_pickings, ignore_index=True)

            df_fi = self.__get_fis(df)
            df_fi['period'] = period
            df_fi['mes'] = month
            df_fi['ano'] = year
            df_fi['data_posicao'] = dt_position
            self.fis = self.fis.append(df_fi, ignore_index=True)

            df_fii = self.__get_fiis(df)
            df_fii['period'] = period
            df_fii['mes'] = month
            df_fii['ano'] = year
            df_fii['data_posicao'] = dt_position
            self.fiis = self.fiis.append(df_fii, ignore_index=True)

            df_picking_fii = self.__get_fiis_profits(df)
            df_picking_fii['period'] = period
            df_picking_fii['mes'] = month
            df_picking_fii['ano'] = year
            df_picking_fii['data_posicao'] = dt_position
            self.fiis_profits = self.fiis_profits.append(df_picking_fii, ignore_index=True)



    def load_data(self):
        '''
        Carrega os arquivos extraido da XP localmente. 
        '''
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

            df_stocks = self.__get_stocks(df)
            df_stocks['period'] = period
            df_stocks['mes'] = month
            df_stocks['ano'] = year
            df_stocks['data_posicao'] = dt_posicao
            self.stocks = self.stocks.append(df_stocks, ignore_index=True)

            df_pickings = self.__get_stocks_profits(df)
            df_pickings['period'] = period
            df_pickings['mes'] = month
            df_pickings['ano'] = year
            df_pickings['data_posicao'] = dt_posicao
            self.stocks_profits = self.stocks_profits.append(df_pickings, ignore_index=True)

            df_fi = self.__get_fis(df)
            df_fi['period'] = period
            df_fi['mes'] = month
            df_fi['ano'] = year
            df_fi['data_posicao'] = dt_posicao
            self.fis = self.fis.append(df_fi, ignore_index=True)

            df_fii = self.__get_fiis(df)
            df_fii['period'] = period
            df_fii['mes'] = month
            df_fii['ano'] = year
            df_fii['data_posicao'] = dt_posicao
            self.fiis = self.fiis.append(df_fii, ignore_index=True)

            df_picking_fii = self.__get_fiis_profits(df)
            df_picking_fii['period'] = period
            df_picking_fii['mes'] = month
            df_picking_fii['ano'] = year
            df_picking_fii['data_posicao'] = dt_posicao
            self.fiis_profits = self.fiis_profits.append(df_picking_fii, ignore_index=True)


    def __get_stocks(self, df):
        acoes = []

        for index, row in df[~df['Unnamed: 2'].isnull()].iterrows():
            if row['Unnamed: 2'] == 'Papel' or row['Unnamed: 2'] == 'Ações':
                continue
            elif row['Unnamed: 2'] == 'Opções':
                break
            else:
                acoes.append(row[['Unnamed: 2', 'Unnamed: 10', 'Unnamed: 18',
                                  'Unnamed: 28', 'Unnamed: 35', 'Unnamed: 43',
                                  'Unnamed: 51', 'Unnamed: 61', 'Unnamed: 68',
                                  'Unnamed: 76', 'Unnamed: 83']].values)

        pd_stock = pd.DataFrame(columns=['Papel', 'Qtd Disponivel',
                                         'Qtd Projetado', 'Qtd Dia',
                                         'Qtd Garantia BOV', 'Qtd Garantia BMF',
                                         'Qtd Estruturados', 'Liq Termo',
                                         'Qtd Total', 'Cotacao', 'Financeiro'], data=acoes)
        
        pd_stock.loc[:, 'Papel'] = np.where(pd_stock['Papel'] == 'BPAC9', 'BPAC11', pd_stock['Papel'])
        pd_stock.loc[:, 'Papel'] = np.where(pd_stock['Papel'] == 'BPAC12', 'BPAC11', pd_stock['Papel'])
        pd_stock.loc[:, 'Papel'] = np.where(pd_stock['Papel'] == 'BPAC6', 'BPAC11', pd_stock['Papel'])

        return pd_stock.groupby(['Papel']).sum().reset_index()
        #return pd_stock


    def __get_stocks_profits(self, df):
        profits = []
        start = False

        for index, row in df[~df['Unnamed: 2'].isnull()].iterrows():
            if row['Unnamed: 2'] == 'Proventos de Ação':
                start = True
                continue
            elif row['Unnamed: 2'] == 'Papel':
                continue
            elif row['Unnamed: 2'] == 'Renda Fixa':
                break
            elif start == True:
                profits.append(row[['Unnamed: 2', 'Unnamed: 11',
                                      'Unnamed: 22', 'Unnamed: 60',
                                      'Unnamed: 77']].values)

        df_profits = pd.DataFrame(columns=['Papel', 'Qtd Provisionada',
                                             'Tipo', 'Data Pagamento', 'Valor'], data=profits)

        return df_profits


    def __get_fis(self, df):
        x = []
        start = False

        for index, row in df[~df.isnull()].iterrows():
            if row['Unnamed: 2'] == 'Fundos de Investimentos':
                start = True
                continue
            elif row['Unnamed: 2'] == 'Nome Fundo':
                continue
            elif row['Unnamed: 2'] == 'Posição de Fundos Imobiliários':
                break
            elif (start == True) and ((type(row['Unnamed: 2']) == str)):
                if type(row['Unnamed: 2']) == str:
                    fi_name = np.array([row['Unnamed: 2']])
                    data = df[df.index == index + 1][['Unnamed: 13', 'Unnamed: 19',
                                                      'Unnamed: 33', 'Unnamed: 40',
                                                      'Unnamed: 48', 'Unnamed: 54',
                                                      'Unnamed: 60', 'Unnamed: 70',
                                                      'Unnamed: 81']]

                    data.insert(0, 'Nome FI', row['Unnamed: 2'])
                    # print(data.values[0])
                    x.append(data.values[0])
                    # display(data.head())

        df_fis = pd.DataFrame(columns=['Nome', 'Data', 'Qtd Cotas',
                                      'Valor Cota', 'Valor Bruto',
                                      'IR', 'IOF', 'Valor Liquido',
                                      'Aplicacao Pendente', 'Total Bruto'], data=x)
                                      
        # Bahia AM Maraú Advisory FIC de 
        df_fis['Nome'] = np.where(df_fis['Nome'] == 'Bahia AM Maraú Advisory FIC de ', 'Bahia AM Maraú FIC de FIM', df_fis['Nome'])                                     
                                      
        #if len(pd_fi[pd_fi['Nome'].str.contains('Azul')]) > 0:
        #print(pd_fi[['Nome', 'Data']])

        return df_fis


    def __get_fiis(self, df):
        fii = []
        start = False

        for index, row in df[~df['Unnamed: 2'].isnull()].iterrows():
            if row['Unnamed: 2'] == 'Posição de Fundos Imobiliários':
                start = True
                continue
            elif row['Unnamed: 2'] == 'Nome':
                continue
            elif row['Unnamed: 2'] == 'Proventos de Fundo Imobiliário':
                break
            elif start == True:
                fii.append(row[['Unnamed: 2', 'Unnamed: 14',
                                'Unnamed: 26', 'Unnamed: 38',
                                'Unnamed: 45', 'Unnamed: 55',
                                'Unnamed: 74']].values)

        df_result = pd.DataFrame(columns=['Papel', 'Qtd Disponivel',
                                                 'Qtd Projetada', 'Qtd Dia', 'Qtde Total',
                                                 'Ult Cotacao', 'Financeiro'], data=fii)

        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'HGLG14', 'HGLG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'CNES11B', 'CNES11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'CNES12B', 'CNES11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'BCFF11B', 'BCFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'BCFF12', 'BCFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'BCFF12B', 'BCFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'OULG11B', 'OULG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'IBFF12', 'IBFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'XPLG13', 'XPLG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'XPLG14', 'XPLG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'RBRF14', 'RBRF11', df_result['Papel'])

        return df_result.groupby(['Papel']).sum().reset_index()


    def __get_fiis_profits(self, df):
        p_fii = []
        start = False

        for index, row in df[~df['Unnamed: 2'].isnull()].iterrows():
            if row['Unnamed: 2'] == 'Proventos de Fundo Imobiliário':
                start = True
                continue
            elif row['Unnamed: 2'] == 'Papel':
                continue
            elif row['Unnamed: 2'] == 'Clubes de Investimentos':
                break
            elif start == True:
                p_fii.append(row[['Unnamed: 2', 'Unnamed: 11',
                                  'Unnamed: 22', 'Unnamed: 60',
                                  'Unnamed: 77']].values)

        df_result = pd.DataFrame(columns=['Papel', 'Tipo',
                                                 'Qtd Provisionada', 'Dt Pagamento',
                                                 'Valor Provisionado'], data=p_fii)

        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'HGLG14', 'HGLG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'CNES11B', 'CNES11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'CNES12B', 'CNES11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'BCFF11B', 'BCFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'BCFF12', 'BCFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'BCFF12B', 'BCFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'OULG11B', 'OULG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'IBFF12', 'IBFF11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'XPLG13', 'XPLG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'XPLG14', 'XPLG11', df_result['Papel'])
        df_result.loc[:, 'Papel'] = np.where(df_result['Papel'] == 'RBRF14', 'RBRF11', df_result['Papel'])

        return df_result.groupby(['Papel']).sum().reset_index()



class Extract:
    
    def __init__(self, dt_inicio, dt_fim, df_extrato, df_extrato_acoes):
        self.fi_map = {
            'Equitas': 'Equitas Selection FIC FIA',
            'Polo Norte': 'Polo Norte I FIC FIM',
            'XP Macro': 'XP Macro FIM',
            'Bahia AM Mara': 'Bahia AM Maraú FIC de FIM',
            'QuestMult': 'AZ Quest Multi FIC FIM',
            'Mau Macro FIC FIM': 'Mauá Macro FIC FIM',
            'MiraeMacroStrategy': 'Mirae Asset Multimercado ',
            'XP LONG SHORT': 'XP Long Short FIC FIM',
            'XP GlobCredit': 'XP GlobCredit FICFIM',  # Falta posicao deste periodo
            'Vot.FicFi CambialD': 'FICFIVot. CambDola',  # idem
            'FICFIVot. CambDola': 'FICFIVot. CambDola',
            'Vot.FicFi CambialDol': 'FICFIVot. CambDola',
            'Inflacao Firf': 'BNP Paribas Inflação FI RF',  # idem
            'Azul QuantitativoFIM': 'Azul Quantitativo FIM',
            'QuantitativoFI': 'Azul Quantitativo FIM',
            'ABSOLUTO CONSUMO': 'XP Absoluto Consumo FIA',
            'Hedge Fic Fim': 'NP Hedge FIC FIM',
            'Legan Low Vol FIM': 'Legan Low Vol FIM',
            'XP MULT-INV FIC FIA': 'XP MULT-INV FIC FIA', 
            'Icatu Vanguarda Pré-F': 'Icatu Vanguarda Pré-Fixado FIRF ', 
            'Macro FIC FIM': 'Mauá Macro FIC FIM'
        }

        self.extract_fis = pd.DataFrame()
        self.cash_in_xp = pd.DataFrame()
        self.cash_out_xp = pd.DataFrame()
        self.__cashin_fi_hist = pd.DataFrame()
        self.__cashout_fi_hist = pd.DataFrame()
        self.fiis_profits = pd.DataFrame()
        self.ir_fi_hist = pd.DataFrame()
        

        self.df = df_extrato
        self.__transform_data(dt_inicio, dt_fim)
        self.__set_extrato_fis()

        self.extrato_acoes = pd.DataFrame()
        self.extrato_fiis = pd.DataFrame()
        self.load_extrato_acoes(df_extrato_acoes)
        

    def load_extrato_acoes(self, df_extrato_acoes):
        df = df_extrato_acoes
        
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
        df['ano'] = df['Data'].dt.year
        df['mes'] = df['Data'].dt.month

        self.extrato_acoes = df[df['Categoria'] == 'ACAO']
        self.extrato_fiis = df[df['Categoria'] == 'FII']


    def __map_fi(self, x):
        group = "unknown"
        for key in self.fi_map:
            if key in x:
                group = self.fi_map[key]
                break
        return group

    def __transform_data(self, dt_inicio, dt_fim):
        self.df['Mov'] = pd.to_datetime(self.df['Mov'], format='%d/%m/%Y')
        self.df['Liq'] = pd.to_datetime(self.df['Liq'], format='%d/%m/%Y')
        self.df['ano'] = self.df['Mov'].dt.year
        self.df['mes'] = self.df['Mov'].dt.month

        self.df = self.df[(self.df['Mov'].dt.year >= dt_inicio) 
                                & (self.df['Mov'].dt.year <= dt_fim)]

        self.cash_in_xp = self.df[self.df['Descricao'].str.contains('TED - RECEBIMENTO DE TED - SPB|TED - CREDITO CONTA CORRENTE')]
        self.cash_out_xp = self.df[self.df['Descricao'].str.contains('RETIRADA EM C/C')]

        self.__cashin_fi_hist = self.df[self.df['Descricao'].str.contains('TED APLICA')]
        self.__cashin_fi_hist.loc[:, 'Nome'] = self.__cashin_fi_hist['Descricao'].apply(self.__map_fi)

        self.__cashout_fi_hist = self.df[self.df['Descricao'].str.contains('RESGATE')]\
            .drop(self.df[self.df['Descricao']
                     .str.contains('IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')].index)
        self.__cashout_fi_hist.loc[:, 'Nome'] = self.__cashout_fi_hist['Descricao'].apply(self.__map_fi)

        self.ir_fi_hist = self.df[self.df['Descricao'].str.contains(
            'IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')]
        self.ir_fi_hist.loc[:, 'Nome'] = self.ir_fi_hist['Descricao'].apply(self.__map_fi)

        self.fiis_profits = self.df[self.df['Descricao'].str.contains('RENDIMENTOS DE CLIENTES')]
        
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('HGLG11'), 'HGLG11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('HGLG14'), 'HGLG11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('CNES11'), 'CNES11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('CNES11B'), 'CNES11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('CNES12B'), 'CNES11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('BCFF11'), 'BCFF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('BCFF11B'), 'BCFF11B', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('BCFF12'), 'BCFF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('BCFF12'), 'BCFF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('OULG11'), 'OULG11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('OULG11B'), 'OULG11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('IBFF11'), 'IBFF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('IBFF12'), 'IBFF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('XPLG11'), 'XPLG11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('XPLG13'), 'XPLG11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('XPLG14'), 'XPLG11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('RNGO11'), 'RNGO11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('TBOF11'), 'TBOF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('TBOF13'), 'TBOF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('RBRF14'), 'RBRF11', self.fiis_profits['Descricao'])
        self.fiis_profits.loc[:, 'Descricao'] = np.where(self.fiis_profits['Descricao'].str.contains('RENDIMENTOS DE CLIENTES CNES'), 'CNES11', self.fiis_profits['Descricao'])
        self.fiis_profits = self.fiis_profits[~self.fiis_profits['Descricao'].str.contains('RENDIMENTOS DE CLIENTES PETR4')]

    def __set_extrato_fis(self):
        df_aportes_fi = self.__cashin_fi_hist.groupby(['Nome', 'ano', 'mes', 'Mov'])\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Aporte', 
                            'Mov': 'Data'})

        df_aportes_fi['Vlr Aporte'] = df_aportes_fi['Vlr Aporte'].abs()

        df_fi_resgates = self.__cashout_fi_hist.groupby(['Nome', 'ano', 'mes', 'Mov'])\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Resgate', 
                                'Mov': 'Data'})

        df_fi_ir = self.ir_fi_hist.groupby(['Nome', 'ano', 'mes', 'Mov'])\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr IR', 
                            'Mov': 'Data'})

        df_fi_ir['Vlr IR'] = df_fi_ir['Vlr IR'].abs()

        df_aportesgroup = df_aportes_fi.merge(
            df_fi_resgates,
            how='outer',
            left_on=['Nome', 'ano', 'mes', 'Data'],
            right_on=['Nome', 'ano', 'mes', 'Data'])\
            .merge(df_fi_ir,
                   how='outer',
                   left_on=['Nome', 'ano', 'mes', 'Data'],
                   right_on=['Nome', 'ano', 'mes', 'Data']
                   ).fillna(0)

        # display(df_fi_aportes)
        # display(df_fi_resgates)

        df_aportesgroup['Vlr Aporte'] = df_aportesgroup['Vlr Aporte'].abs()
        df_aportesgroup.loc[:, 'Rendimento Resgatado'] = np.where(df_aportesgroup['Vlr Resgate'] > 0,
                                                           df_aportesgroup['Vlr Resgate'] -
                                                           df_aportesgroup['Vlr Aporte'],
                                                           0)
        df_aportesgroup['Tipo'] = 'FI' 
        df_aportesgroup['Data'] = pd.to_datetime(df_aportesgroup['Data']).apply(lambda x: utils.last_day_of_month(x))

        df_aportesgroup['Data2'] = df_aportesgroup.apply(lambda x: utils.last_day_of_month(datetime(x['ano'], x['mes'], 1)), axis=1)

        #df_aportesgroup['Data'] = np.where(df_aportesgroup['Data'].isnull(), 
        #                                    )

        
        self.extract_fis = df_aportesgroup.fillna(0)


    def total_investido(self):
        return self.cash_in_xp['Valor'].sum() - self.cash_out_xp['Valor'].abs().sum()


    def periodos(self):
        return self.df.sort_values('Mov')['Mov'].dt.year.unique()