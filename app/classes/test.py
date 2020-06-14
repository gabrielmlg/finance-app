from views import Posicao, Extrato, FundoInvestimento
from repository import PosicaoRepository, ExtratoRepository
import numpy as np

posicao_repository = PosicaoRepository()
posicao_repository.load_data()
df_fis = posicao_repository.fis

extrato_db = ExtratoRepository()
df_extrato = extrato_db.load_csv_extrato()
extrato = Extrato()


extrato_fi = extrato.get_extrato_fis(df_extrato[(df_extrato['Mov'] >= '2018-01-01') & (df_extrato['Mov'] <= '2020-10-01')])
print(df_extrato)
print('#################################')


total_aporte = extrato.total_aportes(extrato_fi) # extrato_fi['Vlr Aporte'].sum() -   # ToDo: Colocar o aporte de acoes e fii
total_resgatado = extrato.total_resgatado(extrato_fi)
total_lucro = extrato.lucro_resgatado(extrato_fi)

fundo_investimento = FundoInvestimento(posicao=df_fis, extrato=extrato_fi)
rendimento_fi = fundo_investimento.rendimento()
periodos = fundo_investimento.periodos()

print(fundo_investimento.total_aportes('2020', '2020'))

print(total_aporte)
#print(periodos.min())

#print((periodos.min().strftime('%Y/%m/%d')))

#print(df_fis.head())
#print(extrato_fi.head())