import pandas as pd

from os import listdir
from os.path import isfile, join


from graficos import *
from pyfzf.pyfzf import FzfPrompt

import confidencial as conf

def similar(dataframe, coluna, filtro):
    return dataframe[dataframe[coluna].str.contains(f'.*{filtro}.*', case=False, na=False)]

fzf = FzfPrompt()


pasta = conf.FONTE
#pasta = conf.DESTINO

arquivos = [x for x in listdir(pasta) if isfile(join(pasta, x))]

arquivo = fzf.prompt(arquivos)
completo = pasta+'/'+arquivo[0]

print(completo)

df = pd.read_csv(completo, encoding='ISO-8859-1')

coluna = fzf.prompt(df.columns.tolist()) #shift-tab para escolher

texto = input(coluna[0] + ": ")

resultado = similar(df, coluna[0], texto)
print(resultado)

resultado.to_csv("csv/" + texto.replace(" ", "") + "_" + arquivo[0].split('/')[-1], index=False)
