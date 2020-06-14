import pandas as pd
import numpy as np


class Posicao:

    def __init__(self):
        pass

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
    fi_map = {
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

    def map_fi(self, x):
        group = "unknown"
        for key in self.fi_map:
            if key in x:
                group = self.fi_map[key]
                break
        return group

    def transform_extrato_fi(self, df):
        df_aportes = df[df['Descricao'].str.contains('TED APLICA')]
        df_aportes['Nome'] = df_aportes['Descricao'].apply(self.map_fi)

        df_resgates = df[df['Descricao'].str.contains('RESGATE')]\
            .drop(df[df['Descricao']
                     .str.contains('IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')].index)

        df_resgates_ir = df[df['Descricao'].str.contains(
            'IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')]
        df_resgates['Nome'] = df_resgates['Descricao'].apply(self.map_fi)
        df_resgates_ir['Nome'] = df_resgates_ir['Descricao'].apply(self.map_fi)
        #df_aportes['Nome'] = df_aportes['Descricao'].map(lambda x: x.str.contains(fi_dict[0]))
        return df_aportes, df_resgates, df_resgates_ir

    def get_extrato_fis(self, df):
        df_fi_aportes, df_fi_resgates, df_fi_ir = self.transform_extrato_fi(df)
        df_fi_aportes = df_fi_aportes.groupby('Nome')\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Aporte'})

        df_fi_resgates = df_fi_resgates.groupby('Nome')\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Resgate'})

        df_fi_ir = df_fi_ir.groupby('Nome')\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr IR'})

        df_aportesgroup = df_fi_aportes.merge(
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

        return df_aportesgroup.fillna(0)

    def total_aportes(self, df_extrato_fis):
        return df_extrato_fis['Vlr Aporte'].sum() - df_extrato_fis['Vlr Resgate'].sum()

    def total_resgatado(self, df_extrato_fis):
        return df_extrato_fis['Vlr Resgate'].sum()

    def total_ir(self, df_extrato_fis):
        return df_extrato_fis['Vlr IR'].sum()

    def lucro_resgatado(self, df_extrato_fis):
        return df_extrato_fis['Rendimento Resgatado'].sum()


class FundoInvestimento:

    posicao_hist = pd.DataFrame()
    extrato_hist = pd.DataFrame()

    def __init__(self, posicao, extrato):
        self.posicao_hist = posicao
        self.extrato_hist = extrato

    def rendimento(self):
        fis_ultima_posicao = self.posicao_hist.groupby(['Nome']).agg({'Data': 'max'}).reset_index()\
            .merge(self.posicao_hist,
                   how='inner',
                   left_on=['Nome', 'Data'],
                   right_on=['Nome', 'Data']).reset_index()\
            .rename(columns={'Data': 'Dt ultima posicao'})

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

        df_rendimento['rendimento'] = np.where(df_rendimento['Dt ultima posicao'] == '2020-05-29',
                                               df_rendimento['Valor Bruto']\
                                                    - df_rendimento['Vlr Aporte']\
                                                    + df_rendimento['Vlr Resgate'], 
                                               df_rendimento['Rendimento Resgatado'])

        print(df_rendimento)
        return df_rendimento['rendimento'].sum()
