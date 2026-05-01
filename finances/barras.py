from os import listdir
from os.path import isfile, join
from pyfzf.pyfzf import FzfPrompt

import pandas as pd

from graficos import *
import confidencial as conf

pasta = conf.FONTE
#pasta = conf.DESTINO

fzf = FzfPrompt()

arquivos = [x for x in listdir(pasta) if isfile(join(pasta, x))]
arquivo = fzf.prompt(arquivos)
completo = pasta +'/'+ arquivo[0]

df = pd.read_csv(completo, encoding='ISO-8859-1')

def agrupar(coluna):
    return df.groupby(coluna, as_index=False) 

gastos_mensais = agrupar(['Mês', 'Tipo Lançamento']).agg(
    Total=('Valor', 'sum')
)

plotsTotal = Barras(gastos_mensais, 'Mês', 'Total', arquivo[0].split('.')[0])

plotsTotal.grafico()
plotsTotal.plots()

