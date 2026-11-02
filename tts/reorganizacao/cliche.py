import manipulacao_arquivos as m_arq
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
from difflib import SequenceMatcher

def encontrar_cliches(sa, sb, min_palavras = 3):
    matcher = SequenceMatcher(None, sa, sb)
    trechos = []
    for bloco in matcher.get_matching_blocks():
        if bloco.size >= min_palavras:
            trecho = " ".join(sa[bloco.a:bloco.a + bloco.size])
            trechos.append(trecho)
    return trechos

def percorrer(informacoes):
    cliches = dict()
    for i in range(1, len(informacoes)):
        informacao_atual, informacao_proxima = informacoes[i-1].split(), informacoes[i].split()
        cliche = encontrar_cliches(informacao_atual, informacao_proxima)
        for c in cliche:
            cliches[c] = i
    return cliches

def comuns_lista(cliches, linhas, distancia_min = 3):
    comuns = [k for k, v in cliches.items() if 0 < linhas - v <= 3]
    return comuns

def remover(informacoes, comuns):
    for informacao in informacoes:
        info = informacao
        for comun in comuns:
            info = info.replace(comun, '')
        print(info)

def compactar(informacoes, comuns):
    for informacao in informacoes:
        info = informacao
        for idx, txt in comuns.items():
            print(txt)
            info = info.replace(txt, idx)
        print(info)


arquivo_teste = "/home/lucas/Documentos/Concurso/Core/AdministracaoGeral/reorganizado/aula-00_2ConceitosGeraiseIntrodutoriosCESPECEBRASPE_reorganizado.txt"
arquivo_teste2 = "/home/lucas/Documentos/Concurso/Core/AdministracaoGeral/reorganizado/aula-00_3QuestoesConceitosGeraiseIntrodutoriosCEBRASPE_reorganizado.txt"
informacao1 = m_arq.abrir_arquivo(arquivo_teste)
informacao2 = m_arq.abrir_arquivo(arquivo_teste2)

#teste = percorrer(informacao)
#print(teste)

#cliches = percorrer(informacao)
#asc = {k: v for k, v in sorted(cliches.items(), key=lambda item: item[1])}
#linhas = len(informacao)
#comuns = comuns_dict(cliches, linhas)
#print(comuns)
#compactar(informacao, comuns)
#remover(informacao, comuns)

#print(len(cliches))
#for i in range(1, len(cliches)):
#    atual = cliches[i-1]
#    proximo = cliches[i]
#    teste = sentido_comum(atual[0], proximo[0])
#    print(teste)
    #print(atual, proximo)

#cliches1 = encontrar_cliches(informacao[0].split(), informacao[1].split())
#cliches2 = encontrar_cliches(informacao[1].split(), informacao[2].split())
#print(cliches1)
#print(cliches2)
#print(list(set(cliches1) & set(cliches2)))

#for info in informacao:
#    infos = info.split(" ")
#    for idx, palavra in teste:
#        infos.remove(palavra)
#    print(" ".join(infos))
