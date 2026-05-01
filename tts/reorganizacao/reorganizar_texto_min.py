import sys
import re
from collections import defaultdict
from text_unidecode import unidecode

from indiceObj import Indice
from dividir_texto import Divisao
import manipulacao_arquivos as m_arq
import confidencial as conf

def numero_aula(nome_arquivo):
    padrao_simples = r'aula-\d{2}'
    match = re.search(padrao_simples, nome_arquivo)

    if match:
        return match.group()
        print(f"Padrão encontrado: {aula_encontrada}")
        # Saída: aula-00
    else:
        return ''
        print("Padrão não encontrado")

def dicionarizar(indx, informacao):
    conteudo = defaultdict(list)
    secao_atual = 'introducao'

    for linha in informacao:
        secao_atual = indx.get(linha, secao_atual)
        conteudo[secao_atual].append(' '.join(informacao[linha]))

    return dict(conteudo)

def reorganizar(conteudo, num_aula):
    for titulo in conteudo:
        titulo_modificado = unidecode(titulo)# Substitui letras acentuadas e caracteres especiais, como ç, por letras sem acento e c
        titulo_limpo = re.sub('[^A-Za-z0-9]+', '', titulo_modificado)
        novo_nome_arquivo = num_aula + '_' + titulo_limpo + '_reorganizado.txt'

        m_arq.criar_novo_arquivo(novo_nome_arquivo, conteudo[titulo])

def arquivo_imcompativel(conteudo_original):
    doc_desorganizado = []
    for linhas in conteudo_original:
        doc_desorganizado.append(' '.join(linhas))

    return doc_desorganizado

def processar_indice(indx, separador):
    indx['1'] = indx['1'].split(separador)[1].strip()
    return indx

DIVISOR = conf.DIVISOR
PADRAO_REGEX = conf.PADRAO_REGEX_ALT

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 extrair_indice.py <caminho_para_arquivo>")
        sys.exit(1)

    dados_entrada = sys.argv[1:]
    for dados in dados_entrada:
        informacao = m_arq.abrir_arquivo(dados)
        num_aula = numero_aula(dados)

        divis = Divisao(DIVISOR, informacao)
        divis_info = divis.dividir()
        print(dados)
        #indx = Indice(divis_info, PADRAO_REGEX)
        #print(divis_info)
        indx = Indice(divis_info)#, PADRAO_REGEX)
        #indx_extraido = processar_indice(indx.extrair_indice(), 'Sumário')
        indx_extraido = indx.extrair_indice()
        #print(indx_extraido)

        if len(indx_extraido):
            print(num_aula, indx_extraido, "\n")
            conteudo = dicionarizar(indx_extraido, divis_info)
            reorganizar(conteudo, num_aula)
        else:
            print(num_aula, "indice não compatível com o regex", "\n")
            doc_desorganizado = arquivo_imcompativel(list(divis_info.values()))
            m_arq.criar_novo_arquivo(num_aula + '_des_reorganizado.txt', doc_desorganizado)

