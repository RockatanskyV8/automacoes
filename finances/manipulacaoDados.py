import pandas as pd
from os import listdir
from os.path import isfile, join

from pyfzf.pyfzf import FzfPrompt
import re
import confidencial as conf

def igual(dataframe, coluna, filtro):
    return dataframe[(dataframe[coluna] == filtro)]

def diferente(dataframe, coluna, filtro):
    return dataframe[(dataframe[coluna] != filtro)]

def total(dataframe, coluna, filtro):
    return dataframe[coluna].sum()


def string_para_int_seguro(s):
    if s is None:
        return None
    s_limpo = str(s).strip()
    if s_limpo and s_limpo.isdigit():
        return int(s_limpo)
    return s 

funcoes = {
    "igual" : igual,
    "diferente" : diferente,
    "total" : total
}

fzf = FzfPrompt()

pasta = conf.FONTE
#pasta = conf.DESTINO

arquivos = [x for x in listdir(pasta) if isfile(join(pasta, x))]

arquivo = fzf.prompt(arquivos)
print(pasta + arquivo[0])
completo = pasta +'/'+ arquivo[0]

dataframe = pd.read_csv(completo)#, encoding='ISO-8859-1')

while True:
    funcao = fzf.prompt(list(funcoes.keys()))[0]

    coluna = fzf.prompt(dataframe.columns.tolist())[0] #shift-tab para escolher
    filtro = fzf.prompt(dataframe[coluna].unique())[0]

    print(coluna, filtro)
    resultado = funcoes[funcao](dataframe, coluna, string_para_int_seguro(filtro))
    print(resultado.dtypes)
    print(resultado)
    opcoes = input("Salvar? [S/n]: ").lower()
    if(opcoes == 's'):
        pattern = f'[^a-zA-Z0-9\s]'
        arquivo_final = re.sub(pattern, '', filtro).replace(" ", "_") + "-" + arquivo[0].split('/')[-1]
        print(arquivo_final)
        resultado.to_csv("csv/" + arquivo_final, index=False)
        break

