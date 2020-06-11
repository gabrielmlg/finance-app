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
                    data = df[df.index == index +1][['Unnamed: 13', 'Unnamed: 19', 
                                                        'Unnamed: 33', 'Unnamed: 40', 
                                                        'Unnamed: 48', 'Unnamed: 54', 
                                                        'Unnamed: 60', 'Unnamed: 70', 
                                                        'Unnamed: 81']]
                    
                    data.insert(0, 'Nome FI', row['Unnamed: 2'])
                    # print(data.values[0])
                    x.append(data.values[0])
                    #display(data.head())
        
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
        'XP GlobCredit': 'XP GlobCredit FICFIM', # Falta posicao deste periodo
        'Vot.FicFi CambialD': 'Vot.FicFi CambialD',  # idem
        'BNP Inflacao Firf': 'BNP Inflacao Firf', # idem
        'Azul QuantitativoFIM': 'Azul Quantitativo', 
        'ABSOLUTO CONSUMO': 'ABSOLUTO CONSUMO', 
        'Hedge Fic Fim': 'Hedge Fic Fim'
    }


    def map_fi(self, x):
        group = "unknown"
        for key in self.fi_map:
            if key in x:
                group = self.fi_map[key]
                break
        return group


    def load_csv_extrato(self):
        df = pd.read_csv('./datasets/extrato/Extrato2.csv', sep=';', encoding='iso-8859-1', decimal=',')
        df['Mov'] = pd.to_datetime(df['Mov'], format='%d/%m/%Y')
        df['Liq'] = pd.to_datetime(df['Liq'], format='%d/%m/%Y')
        df.rename(columns={'Hist__o': 'Descricao'}, inplace=True)

        return df


    def transform_extrato_fi(self, df):
        df_aportes  = df[df['Descricao'].str.contains('TED APLICA')]
        df_aportes['Nome'] = df_aportes['Descricao'].apply(self.map_fi)

        df_resgates = df[df['Descricao'].str.contains('RESGATE')].drop(df[df['Descricao'].str.contains('IRRF S/RESGATE FUNDOS')].index)
        df_resgates_ir = df[df['Descricao'].str.contains('IRRF S/RESGATE FUNDOS')]
        df_resgates['Nome'] = df_resgates['Descricao'].apply(self.map_fi)
        df_resgates_ir['Nome'] = df_resgates_ir['Descricao'].apply(self.map_fi)
        #df_aportes['Nome'] = df_aportes['Descricao'].map(lambda x: x.str.contains(fi_dict[0]))
        return df_aportes, df_resgates, df_resgates_ir


    def get_extrato_fis(self, df):
        df_aportesfi_aportes, df_aportesfi_resgates, df_aportesfi_ir = self.transform_extrato_fi(df)
        df_aportesfi_aportes = df_aportesfi_aportes.groupby('Nome')\
                                        .agg({'Valor': 'sum'})\
                                        .reset_index()\
                                        .rename(columns={'Valor': 'Vlr Aporte'})

        df_aportesfi_resgates = df_aportesfi_resgates.groupby('Nome')\
                                        .agg({'Valor': 'sum'})\
                                        .reset_index()\
                                        .rename(columns={'Valor': 'Vlr Resgate'})

        df_aportesfi_ir = df_aportesfi_ir.groupby('Nome')\
                                        .agg({'Valor': 'sum'})\
                                        .reset_index()\
                                        .rename(columns={'Valor': 'Vlr IR'})

        df_aportesgroup = df_aportesfi_aportes.merge(
                                    df_aportesfi_resgates, 
                                    how='outer', 
                                    left_on='Nome', 
                                    right_on='Nome')\
                                .merge(df_aportesfi_ir, 
                                        how='left', 
                                        left_on='Nome', 
                                        right_on='Nome'
                                )

        #display(df_aportesfi_aportes)
        #display(df_aportesfi_resgates)

        df_aportesgroup['Vlr Aporte'] = df_aportesgroup['Vlr Aporte'].abs()
        df_aportesgroup['Rendimento Resgatado'] = df_aportesgroup['Vlr Resgate'] - df_aportesgroup['Vlr Aporte'] - df_aportesgroup['Vlr IR'].abs()
        df_aportesgroup['Rendimento Resgatado'] = df_aportesgroup['Rendimento Resgatado'].fillna(0)
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