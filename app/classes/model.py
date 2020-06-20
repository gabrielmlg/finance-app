import pandas as pd
import os
import xlrd
import numpy as np


class Posicao:

    def __init__(self):
        self.files = os.listdir('./datasets/posicao/')
        self.acoes = pd.DataFrame()
        self.dividendo_acoes = pd.DataFrame()
        self.fis = pd.DataFrame()
        self.fiis = pd.DataFrame()
        self.dividendo_fiis = pd.DataFrame()
    

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

            df_stocks = self.get_acoes(df)
            df_stocks['period'] = period
            df_stocks['mes'] = month
            df_stocks['ano'] = year
            df_stocks['data_posicao'] = dt_posicao
            self.acoes = self.acoes.append(df_stocks, ignore_index=True)

            df_pickings = self.get_acoes_provento(df)
            df_pickings['period'] = period
            df_pickings['mes'] = month
            df_pickings['ano'] = year
            df_pickings['data_posicao'] = dt_posicao
            self.dividendo_acoes = self.dividendo_acoes.append(df_pickings, ignore_index=True)

            df_fi = self.get_fi(df)
            df_fi['period'] = period
            df_fi['mes'] = month
            df_fi['ano'] = year
            df_fi['data_posicao'] = dt_posicao
            self.fis = self.fis.append(df_fi, ignore_index=True)

            df_fii = self.get_fii(df)
            df_fii['period'] = period
            df_fii['mes'] = month
            df_fii['ano'] = year
            df_fii['data_posicao'] = dt_posicao
            self.fiis = self.fiis.append(df_fii, ignore_index=True)

            df_picking_fii = self.get_fii_proventos(df)
            df_picking_fii['period'] = period
            df_picking_fii['mes'] = month
            df_picking_fii['ano'] = year
            df_picking_fii['data_posicao'] = dt_posicao
            self.dividendo_fiis = self.dividendo_fiis.append(df_picking_fii, ignore_index=True)


    def get_acoes(self, df):
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

        return pd_stock


    def get_acoes_provento(self, df):
        proventos = []
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
                proventos.append(row[['Unnamed: 2', 'Unnamed: 11',
                                      'Unnamed: 22', 'Unnamed: 60',
                                      'Unnamed: 77']].values)

        pd_proventos = pd.DataFrame(columns=['Papel', 'Qtd Provisionada',
                                             'Tipo', 'Data Pagamento', 'Valor'], data=proventos)

        return pd_proventos


    def get_fi(self, df):
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

        pd_fi = pd.DataFrame(columns=['Nome', 'Data', 'Qtd Cotas',
                                      'Valor Cota', 'Valor Bruto',
                                      'IR', 'IOF', 'Valor Liquido',
                                      'Aplicacao Pendente', 'Total Bruto'], data=x)
                                      
        #if len(pd_fi[pd_fi['Nome'].str.contains('Azul')]) > 0:
        #print(pd_fi[['Nome', 'Data']])

        return pd_fi


    def get_fii(self, df):
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

        df_aportesresult = pd.DataFrame(columns=['Papel', 'Qtd Disponivel',
                                                 'Qtd Projetada', 'Qtd Dia', 'Qtde Total',
                                                 'Ult Cotacao', 'Financeiro'], data=fii)

        return df_aportesresult


    def get_fii_proventos(self, df):
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

        df_aportesresult = pd.DataFrame(columns=['Papel', 'Tipo',
                                                 'Qtd Provisionada', 'Dt Pagamento',
                                                 'Valor Provisionado'], data=p_fii)

        return df_aportesresult



class Extrato:
    df_extrato_fis = pd.DataFrame()

    aportes_xp = pd.DataFrame()
    retiradas_xp = pd.DataFrame()
    aportes_fi_hist = pd.DataFrame()
    resgates_fi_hist = pd.DataFrame()
    ir_fi_hist = pd.DataFrame()
    

    def __init__(self, dt_inicio, dt_fim):

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
            'Inflacao Firf': 'BNP Inflacao Firf',  # idem
            'Azul QuantitativoFIM': 'Azul Quantitativo',
            'QuantitativoFI': 'Azul Quantitativo',
            'ABSOLUTO CONSUMO': 'ABSOLUTO CONSUMO',
            'Hedge Fic Fim': 'Hedge Fic Fim',
            'Legan Low Vol FIM': 'Legan Low Vol FIM',
            'XP MULT-INV FIC FIA': 'XP MULT-INV FIC FIA'
        }

        self.df = self.load_csv_extrato()
        self.filter_extrato(dt_inicio, dt_fim)
        self.set_aportes_resgates()
        self.set_extrato_fis()


    def filter_extrato(self, dt_inicio, dt_fim):
        self.df = self.df[(self.df['Mov'].dt.year >= dt_inicio) 
                                & (self.df['Mov'].dt.year <= dt_fim)]


    def load_csv_extrato(self):
        df = pd.read_csv('./datasets/extrato/Extrato 200091 JAN 2010 a JUN 2020.csv', sep=';', encoding='iso-8859-1', decimal=',')
        df['Mov'] = pd.to_datetime(df['Mov'], format='%d/%m/%Y')
        df['Liq'] = pd.to_datetime(df['Liq'], format='%d/%m/%Y')
        df.rename(columns={'Hist__o': 'Descricao'}, inplace=True)

        return df


    def map_fi(self, x):
        group = "unknown"
        for key in self.fi_map:
            if key in x:
                group = self.fi_map[key]
                break
        return group


    def set_aportes_resgates(self):

        self.aportes_xp = self.df[self.df['Descricao'].str.contains('TED - RECEBIMENTO DE TED - SPB|TED - CREDITO CONTA CORRENTE')]
        self.retiradas_xp = self.df[self.df['Descricao'].str.contains('RETIRADA EM C/C')]
        self.aportes_fi_hist = self.df[self.df['Descricao'].str.contains('TED APLICA')]
        self.aportes_fi_hist['Nome'] = self.aportes_fi_hist['Descricao'].apply(self.map_fi)

        self.resgates_fi_hist = self.df[self.df['Descricao'].str.contains('RESGATE')]\
            .drop(self.df[self.df['Descricao']
                     .str.contains('IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')].index)

        self.ir_fi_hist = self.df[self.df['Descricao'].str.contains(
            'IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')]
        self.resgates_fi_hist['Nome'] = self.resgates_fi_hist['Descricao'].apply(self.map_fi)
        self.ir_fi_hist['Nome'] = self.ir_fi_hist['Descricao'].apply(self.map_fi)
        #df_aportes['Nome'] = df_aportes['Descricao'].map(lambda x: x.str.contains(fi_dict[0]))


    def set_extrato_fis(self):
        df_aportes_fi = self.aportes_fi_hist.groupby('Nome')\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Aporte'})

        df_fi_resgates = self.resgates_fi_hist.groupby('Nome')\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Resgate'})

        df_fi_ir = self.ir_fi_hist.groupby('Nome')\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr IR'})

        df_aportesgroup = df_aportes_fi.merge(
            df_fi_resgates,
            how='outer',
            left_on='Nome',
            right_on='Nome')\
            .merge(df_fi_ir,
                   how='left',
                   left_on='Nome',
                   right_on='Nome'
                   ).fillna(0)

        # display(df_fi_aportes)
        # display(df_fi_resgates)

        df_aportesgroup['Vlr Aporte'] = df_aportesgroup['Vlr Aporte'].abs()
        df_aportesgroup['Rendimento Resgatado'] = np.where(df_aportesgroup['Vlr Resgate'] > 0,
                                                           df_aportesgroup['Vlr Resgate'] -
                                                           df_aportesgroup['Vlr Aporte'],
                                                           0)
        # df_aportesgroup[df_aportesgroup['Vlr Aporte'].isnull()]['Vlr Aporte'] = df_aportesgroup[df_aportesgroup['Vlr Aporte'].isnull()]['Vlr Resgate']

        self.df_extrato_fis = df_aportesgroup.fillna(0)


    def total_investido(self):
        return self.aportes_xp['Valor'].sum() - self.retiradas_xp['Valor'].abs().sum()


    def total_aportes(self):
        return self.df_extrato_fis['Vlr Aporte'].sum() - self.df_extrato_fis['Vlr Resgate'].sum()


    def total_resgatado(self):
        return self.df_extrato_fis['Vlr Resgate'].sum()


    def total_ir(self):
        return self.df_extrato_fis['Vlr IR'].sum()


    def lucro_resgatado(self):
        return self.df_extrato_fis['Rendimento Resgatado'].sum()


    def periodos(self):
        return self.df.sort_values('Mov')['Mov'].dt.year.unique()



class FundoInvestimento:

    posicao_hist = pd.DataFrame()
    extrato_hist = pd.DataFrame()

    def __init__(self, posicao, extrato):
        self.posicao_hist = posicao
        self.extrato_hist = extrato

    def rendimento(self, dt_inicio, dt_fim):
        fis_ultima_posicao = self.posicao_hist.groupby(['Nome']).agg({'Data': 'max'}).reset_index()\
            .merge(self.posicao_hist,
                   how='inner',
                   left_on=['Nome', 'Data'],
                   right_on=['Nome', 'Data']).reset_index()\
            .rename(columns={'Data': 'Dt ultima posicao'})

        #print(self.posicao_hist['Nome'].unique())
        #print('--------------------------------------------')
        #print(fis_ultima_posicao)
        """ print(fis_ultima_posicao)
        print('=======================================================')
        print('=======================================================')
        print(self.extrato_hist)
        print('=======================================================')
        print('=======================================================') """
        df_rendimento = fis_ultima_posicao[['Nome',
                                            'Valor Bruto',
                                            'Dt ultima posicao']].merge(self.extrato_hist,
                                                                        how='outer',
                                                                        left_on='Nome',
                                                                        right_on='Nome').reset_index()

        #df_rendimento[(df_rendimento[''])]

        df_rendimento['rendimento'] = np.where(df_rendimento['Dt ultima posicao'] == '2020-05-29',
                                               df_rendimento['Valor Bruto']\
                                                    - df_rendimento['Vlr Aporte']\
                                                    + df_rendimento['Vlr Resgate'], 
                                               df_rendimento['Rendimento Resgatado'])

        #print(df_rendimento)
        return df_rendimento['rendimento'].sum()
    
    # POSSIVEIS METODOS PARA ABSTRAIR

    def periodos(self):
        return self.posicao_hist.sort_values('Data')['Data'].dt.year.unique()

    
    def total_aportes(self):
        return self.extrato_hist['Vlr Aporte'].sum() - self.extrato_hist['Vlr Resgate'].sum()

    def total_resgatado(self, df_extrato_fis):
        return df_extrato_fis['Vlr Resgate'].sum()

    def total_ir(self, df_extrato_fis):
        return df_extrato_fis['Vlr IR'].sum()

    def lucro_resgatado(self, df_extrato_fis):
        return df_extrato_fis['Rendimento Resgatado'].sum()