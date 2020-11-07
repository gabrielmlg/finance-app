import pandas as pd
import numpy as np

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
        self.posicao_hist = posicao
        self.extrato_hist = extrato

        self.aportes_fi_hist = pd.DataFrame()
        self.resgates_fi_hist = pd.DataFrame()
        self.ir_fi_hist = pd.DataFrame()
        self.__set_aportes_resgates()
        self.extrato = self.__set_extrato_fis()


    def __map_fi(self, x):
        group = "unknown"
        for key in self.fi_map:
            if key in x:
                group = self.fi_map[key]
                break
        return group


    def __set_aportes_resgates(self):

        self.aportes_fi_hist = self.extrato_hist[self.extrato_hist['Descricao'].str.contains('TED APLICA')]
        self.aportes_fi_hist['Nome'] = self.aportes_fi_hist['Descricao'].apply(self.__map_fi)

        self.resgates_fi_hist = self.extrato_hist[self.extrato_hist['Descricao'].str.contains('RESGATE')]\
            .drop(self.extrato_hist[self.extrato_hist['Descricao']
                     .str.contains('IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')].index)
        self.resgates_fi_hist['Nome'] = self.resgates_fi_hist['Descricao'].apply(self.__map_fi)

        self.ir_fi_hist = self.extrato_hist[self.extrato_hist['Descricao'].str.contains(
            'IRRF S/RESGATE FUNDOS|IRRF S/ RESGATE FUNDOS')]
        self.ir_fi_hist['Nome'] = self.ir_fi_hist['Descricao'].apply(self.__map_fi)

        #df_aportes['Nome'] = df_aportes['Descricao'].map(lambda x: x.str.contains(fi_dict[0]))


    def __set_extrato_fis(self):
        #print(self.aportes_fi_hist.head(10))
        df_aportes_fi = self.aportes_fi_hist.groupby(['Nome', 'Ano', 'Mes'])\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Aporte'})

        df_aportes_fi['Vlr Aporte'] = df_aportes_fi['Vlr Aporte'].abs()

        df_fi_resgates = self.resgates_fi_hist.groupby(['Nome', 'Ano', 'Mes'])\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr Resgate'})

        df_fi_ir = self.ir_fi_hist.groupby(['Nome', 'Ano', 'Mes'])\
            .agg({'Valor': 'sum'})\
            .reset_index()\
            .rename(columns={'Valor': 'Vlr IR'})

        df_fi_ir['Vlr IR'] = df_fi_ir['Vlr IR'].abs()

        df_aportesgroup = df_aportes_fi.merge(
            df_fi_resgates,
            how='outer',
            left_on=['Nome', 'Ano', 'Mes'],
            right_on=['Nome', 'Ano', 'Mes'])\
            .merge(df_fi_ir,
                   how='outer',
                   left_on=['Nome', 'Ano', 'Mes'],
                   right_on=['Nome', 'Ano', 'Mes']
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


    def resumo(self, dt_inicio, dt_fim):
        month = self.posicao_hist[(self.posicao_hist['ano'] == dt_fim)]['mes'].max()

        pos = self.posicao_hist[
            (self.posicao_hist['ano'] == dt_fim)
            & (self.posicao_hist['mes'] == month)]

        ext = self.extrato[self.extrato['Ano'] <= dt_fim]\
                            .groupby(['Nome']).agg({'Vlr Aporte': 'sum', 
                                                    'Vlr Resgate': 'sum', 
                                                    'Vlr IR': 'sum'}).reset_index()

        result = pos[['Nome', 'Valor Bruto']].merge(ext, 
                                            how='outer', 
                                            left_on='Nome', 
                                            right_on='Nome').fillna(0)


        result['rendimento'] = result['Valor Bruto'] + result['Vlr Resgate'] - result['Vlr Aporte']
        # print(result)
        return result


    # Calcula o rendimendo de ativo FI para cada periodo. 
    # Retorna o dataset com o campo rendimento e rendimento acumulado. 
    def calcula_rentabilidade(self, do_ano, ate_ano):
        df = self.posicao_hist[(self.posicao_hist['ano'] >= do_ano) &  
                                (self.posicao_hist['ano'] <= ate_ano)]

        df_return = pd.DataFrame([], columns=df.columns)

        for ativo in df['Nome'].unique():
            df_ = df[df['Nome'] == ativo].sort_values(by=['data_posicao']).reset_index()
            rendimento = []

            for row in df_.index:
                if row == 0:
                    rendimento.append(0)
                else:
                    valor = df_[df_.index == row]['Valor Bruto'].sum() - df_[df_.index == row -1]['Valor Bruto'].sum()
                    rendimento.append(valor)

            df_['rendimento'] = rendimento
            df_['rendimento_acum'] = df_['rendimento'].cumsum()
            df_return = df_return.append(df_)

        return df_return

    
    # POSSIVEIS METODOS PARA ABSTRAIR

    def periodos(self):
        return self.posicao_hist.sort_values('Data')['Data'].dt.year.unique()

    
    def total_aportes(self):
        return self.extrato['Vlr Aporte'].sum() - self.extrato['Vlr Resgate'].sum()


    def total_resgatado(self):
        return self.extrato['Vlr Resgate'].sum()


    def total_ir(self):
        return self.extrato['Vlr IR'].sum()


    def lucro_resgatado(self):
        return self.extrato_hist['Rendimento Resgatado'].sum()


class Posicao:

    def __init__(self):
        pass



class Extrato:

    def __init__(self):
        pass
    




