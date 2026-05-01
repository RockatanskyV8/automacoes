import pandas as pd

from os import listdir
from os.path import isfile, join

from graficos import *
from pyfzf.pyfzf import FzfPrompt
import confidencial as conf

fzf = FzfPrompt()

def agrupar(coluna):
    return df.groupby(coluna, as_index=False) 

pasta = conf.FONTE
#pasta = conf.DESTINO

arquivos = [x for x in listdir(pasta) if isfile(join(pasta, x))]

arquivo = fzf.prompt(arquivos)
completo = pasta+'/'+arquivo[0]

df = pd.read_csv(completo, encoding='ISO-8859-1')

gastos_mensais = agrupar(['Mês', 'Tipo Lançamento']).agg(
    Total=('Valor', 'sum')
)

gastos_mensais = gastos_mensais.pivot(index='Mês', columns='Tipo Lançamento', values='Total').reset_index().fillna(0)
plotsTotal = Linhas(gastos_mensais, 'Mês', ['Entrada', 'Saída'], arquivo[0].split('.')[0])

plotsTotal.grafico()
plotsTotal.plots()

