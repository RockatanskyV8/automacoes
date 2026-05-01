import pandas as pd
from os import listdir
from os.path import isfile, join


from graficos import *
from pyfzf.pyfzf import FzfPrompt
import confidencial as conf


def agrupar(dataframe, coluna):
    return dataframe.groupby(coluna, as_index=False)

fzf = FzfPrompt()

#pasta = conf.FONTE
pasta = conf.DESTINO

arquivos = [x for x in listdir(pasta) if isfile(join(pasta, x))]

arquivo = fzf.prompt(arquivos)
completo = pasta+'/'+arquivo[0]

df = pd.read_csv(completo)#, encoding='ISO-8859-1')

#print(df.dtypes)

coluna = fzf.prompt(df.columns.tolist(), '--multi') #shift-tab para escolher

resultado = agrupar(df, coluna).agg(Total=('Crédito (R$)', 'sum'))

print(resultado)

arquivo_saida = "agrupado_" + arquivo[0].split('/')[-1]
print(arquivo_saida)
resultado.to_csv(arquivo_saida, index=False)
