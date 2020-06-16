from views import Posicao, Extrato, FundoInvestimento
from repository import PosicaoRepository, ExtratoRepository
import numpy as np

posicao_repository = PosicaoRepository()
posicao_repository.load_data()
df_fis = posicao_repository.fis

extrato_db = ExtratoRepository()
df_extrato = extrato_db.load_csv_extrato()
extrato = Extrato(df_extrato[(df_extrato['Mov'].dt.year >= 2010) & (df_extrato['Mov'].dt.year <= 2020)])

#print(df_extrato[(df_extrato['Mov'].dt.year >= 2020) & (df_extrato['Mov'].dt.year <= 2020)])

#extrato_fi = extrato.get_extrato_fis(df_extrato[(df_extrato['Mov'].dt.year >= 2010) & (df_extrato['Mov'].dt.year <= 2020)])
#print(extrato_fi)
print('#################################')

total_aporte_xp = extrato.aportes_xp['Valor'].sum()
total_retirada_xp = extrato.retiradas_xp['Valor'].abs().sum()
total_aporte = extrato.total_aportes() # extrato_fi['Vlr Aporte'].sum() -   # ToDo: Colocar o aporte de acoes e fii
total_resgatado = extrato.total_resgatado()
total_lucro = extrato.lucro_resgatado()

fundo_investimento = FundoInvestimento(posicao=df_fis, extrato=extrato.df_extrato_fis)
rendimento_fi = fundo_investimento.rendimento()
periodos = fundo_investimento.periodos()

# print(fundo_investimento.total_aportes('2020', '2020'))

print('Total aportado XP: {:,.2f}'.format(total_aporte_xp))
print('Total retirado XP: {:,.2f}'.format(total_retirada_xp))
print('Resumo aportado XP: {:,.2f}'.format(total_aporte_xp - total_retirada_xp))
print(extrato.total_investido())
print(total_aporte)
print(periodos)
print(periodos.min())


#print((periodos.min().strftime('%Y/%m/%d')))

#print(df_fis.head())
#print(extrato_fi.head())