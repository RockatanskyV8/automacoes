import re
import json
import sys
import confidencial as conf

from typing import Dict
from dataclasses import dataclass, asdict

@dataclass
class Questao:
    """Representa uma questão extraída do texto"""
    numero: int
    banca: str
    enunciado: str
    comentario: str
    gabarito: str

    def to_dict(self) -> Dict:
        return asdict(self)

    def validar(self) -> bool:
        enunciado_val = not self.enunciado == ""
        comentario_val = not self.comentario == ""
        return enunciado_val and comentario_val

def parse_banca(texto):
    padrao_cabecalho = re.compile(
        r'(Cebraspe|cespe|Inédita|INÉDITA)',
        re.IGNORECASE
    )
    resultado = padrao_cabecalho.search(texto)
    return bool(resultado)

def parse_parenteses(texto):
    padrao_cabecalho = re.compile(r"\(([^)]*)\)") #re.MULTILINE | re.DOTALL
    blocos = padrao_cabecalho.finditer(texto)
    idxs = [bloco for bloco in blocos]
    res = []
    for idx in idxs:
        if parse_banca(idx.group(1)):
            res.append(idx)
    if len(res) < 1:
        print("Questões não encontradas")
    return parse_questoes(texto, res)

def parse_questoes(texto, res):
    questionario = []
    for r in range(1, len(res)):
        prev, next = res[r-1], res[r]
        banca = prev.group(1)
        enunciado = texto[prev.end():next.start()].strip()
        questao, comentario = parse_comentarios(enunciado)
        _, gabarito = parse_gabarito(comentario)
        questao_organizada = Questao(r, banca, questao, comentario, gabarito)
        if (questao_organizada.validar()):
            questionario.append(questao_organizada.to_dict())
        else:
            informacoes_incompletas.append(r)
    return questionario

def parse_comentarios(texto):
    padrao_cabecalho = re.compile(r'(Comentários|Comentário|Comentários:|Comentário:)', re.DOTALL)
    blocos = padrao_cabecalho.search(texto)#finditer(texto)
    if blocos:
        questao, comentario = divisao(texto, blocos)
        return questao, comentario
    else:
        return "", ""

def parse_gabarito(texto):
    padrao_cabecalho = re.compile(r'(Gabarito:)', re.DOTALL)
    blocos = padrao_cabecalho.search(texto)#finditer(texto)
    if blocos:
        comentario, gabarito = divisao(texto, blocos)
        return comentario, gabarito
    else:
        return "", ""

def divisao(texto, bloco):
    inicio = bloco.start()
    fim = bloco.end()
    txt_inicio = texto[:inicio].strip()
    #titulo = texto[inicio:fim].strip()
    txt_end = texto[fim:].strip()
    return txt_inicio, txt_end

def remover_elementos(texto, elementos):
    txt_resultado = texto
    for elemento in elementos:
        txt_resultado.replace(elemento, " ")
    return txt_resultado

def processar_arquivos(arquivo):
    """Processa uma lista de arquivos e retorna todas as questões"""
    todas_questoes = []

    with open(arquivo, 'r', encoding='utf-8') as f:
        txt = ' '.join(f.read().split('\n'))
        texto = remover_elementos(txt, conf.REMOVER)
        todas_questoes = parse_parenteses(texto)


    return todas_questoes

erros = []
informacoes_incompletas = []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 extrair_indice.py <caminho_para_arquivo>")
        sys.exit(1)
    arquivos_entrada = sys.argv[1:]
    for arquivo in arquivos_entrada: 
        try:
            erros = []
            informacoes_incompletas = []
            print(f"Extraindo do arquivo {arquivo}")
            questoes = processar_arquivos(arquivo)
            # Salva como JSON
            nome_arquivo = arquivo.split('/')
            nome_json = nome_arquivo[-1].split('.')
            with open(nome_json[0] + '.json' , 'w', encoding='utf-8') as f:
                json.dump(questoes, f, ensure_ascii=False, indent=2)
            print(f"{arquivo}")
            print(f"Total de questões extraídas: {len(questoes)}")
            print(f"Questões com informações incompletas: {informacoes_incompletas}")
            print(" ----------------------------------------------------- ")
        except Exception as e:
            print(f"Erro ao processar {arquivo}:\n{e}")

