import sys
import re
from collections import defaultdict
from text_unidecode import unidecode

from indiceObj import Indice, IndiceAlinhado
from dividir_texto import Divisao
import manipulacao_arquivos as m_arq
import confidencial as conf

def numero_aula(nome_arquivo):
    padrao_simples = r'aula-\d{2}'
    match = re.search(padrao_simples, nome_arquivo)

    if match:
        return match.group()
        print("Padrão encontrado")
        # Saída: aula-00
    else:
        return ''
        print("Padrão não encontrado")

def dicionarizar(indx, informacao):
    conteudo = defaultdict(list)
    secao_atual = 'introducao'

    for linha in informacao:
        secao_atual = indx.get_ou_padrao(linha, secao_atual)
        conteudo[secao_atual].append(' '.join(informacao[linha]))

    return dict(conteudo)

def reorganizar(conteudo, num_aula):
    for titulo in conteudo:
        titulo_modificado = unidecode(titulo)# Substitui letras acentuadas e caracteres especiais, como ç, por letras sem acento e c
        titulo_limpo = re.sub('[^A-Za-z0-9]+', '', titulo_modificado)
        novo_nome_arquivo = num_aula + '_' + titulo_limpo + '_reorganizado.txt'

        if len(novo_nome_arquivo) > 90:
            print(f"Novo nome de arquivo,{novo_nome_arquivo}, muito longo")
            primeira_parte = ''.join(titulo_modificado.split(' ')[:4])
            ultima_parte = ''.join(titulo_modificado.split(' ')[-1])
            novo_titulo_modificado = ''.join([primeira_parte, ultima_parte])

            novo_titulo_limpo = re.sub('[^A-Za-z0-9]+', '', novo_titulo_modificado)
            novo_nome_arquivo = num_aula + '_' + novo_titulo_limpo + '_reorganizado.txt'

            print(f"Novo nome de arquivo será: {novo_nome_arquivo}")

        m_arq.criar_novo_arquivo(novo_nome_arquivo, conteudo[titulo])

def arquivo_incompativel(conteudo_original):
    doc_desorganizado = []
    for linhas in conteudo_original:
        doc_desorganizado.append(' '.join(linhas))

    return doc_desorganizado

def processar_indice(indx, separador):
    indx['1'] = indx['1'].split(separador)[1].strip()
    return indx

DIVISOR = conf.DIVISOR
PADRAO_REGEX = conf.PADRAO_REGEX_ALT
REMOCAO = conf.REMOVER

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 extrair_indice.py <caminho_para_arquivo>")
        sys.exit(1)

    dados_entrada = sys.argv[1:]
    for dados in dados_entrada:
        informacao = m_arq.abrir_arquivo(dados)
        num_aula = numero_aula(dados)

        divis = Divisao(DIVISOR, informacao, REMOCAO)
        divis_info = divis.dividir()
        #print(divis_info)
        indx = Indice(divis_info)#, PADRAO_REGEX)
        #print(indx_extraido)
 
        if len(indx):
            print(num_aula, str(indx), "\n")
            conteudo = dicionarizar(indx, divis_info)
            reorganizar(conteudo, num_aula)
        else:
            print(num_aula, "Índice não compatível com o regex\nTestando regex alternativo...")
            indx = IndiceAlinhado(divis_info)
            #indx_extraido = processar_indice(indx.extrair_indice(), 'Sumário')
            if len(indx):
                print(num_aula, str(indx), "\n")
                conteudo = dicionarizar(indx, divis_info)
                reorganizar(conteudo, num_aula)
            else:
                print(num_aula, "Índice alternativo também não compatível com o regex\nFazendo versão desorganizada...")
                doc_desorganizado = arquivo_incompativel(list(divis_info.values()))
                m_arq.criar_novo_arquivo(num_aula + '_des_reorganizado.txt', doc_desorganizado)

