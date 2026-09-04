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

class Processar():
    def __init__(self, texto):
        self.texto = texto

    def parse_presenca(self, trecho, regex):
        padrao = re.compile(regex, re.IGNORECASE)
        resultado = padrao.search(trecho)
        return bool(resultado)

    def parse_trecho(self, trecho, regex):
        padrao = re.compile(regex, re.DOTALL)
        blocos = padrao.search(trecho) # finditer(texto)
        if blocos:
            inicio, fim = self.divisao(trecho, blocos)
            return inicio, fim
        else:
            return "", ""

    def parse_parenteses(self, regex):
        padrao_cabecalho = re.compile(regex) #re.MULTILINE | re.DOTALL
        blocos = padrao_cabecalho.finditer(self.texto)
        return [bloco for bloco in blocos]

    def divisao(self, trecho, bloco):
        inicio = bloco.start()
        fim = bloco.end()
        txt_inicio = trecho[:inicio].strip()
        txt_fim = trecho[fim:].strip()
        return txt_inicio, txt_fim

def parse_questoes(texto):
    processar = Processar(texto)
    parenteses = processar.parse_parenteses(r'\(([^)]*)\)')
    resultado = []
    for idx in parenteses:
        test = processar.parse_presenca(idx.group(0), r'(Cebraspe|cespe|Inédita|INÉDITA)')
       #print(idx.group(0), test)
        if test:
            resultado.append(idx)
    if len(resultado) < 1:
        print("Questões não encontradas")

    questionario = []
    for r in range(1, len(resultado)):
        prev, next = resultado[r-1], resultado[r]
        banca = prev.group(1)
        enunciado = texto[prev.end():next.start()].strip()
        questao, comentario = processar.parse_trecho(enunciado, r'(Comentários|Comentário|Comentários:|Comentário:)')# parse_comentario
        _, gabarito = processar.parse_trecho(comentario, r'(Gabarito:)') # parse_gabarito
        questao_organizada = Questao(r, banca, questao, comentario, gabarito)
        if (questao_organizada.validar()):
            questionario.append(questao_organizada.to_dict())
        else:
            informacoes_incompletas.append(r)
    return questionario


def remover_elementos(texto, elementos):
    txt_resultado = texto
    for elemento in elementos:
        txt_resultado = txt_resultado.replace(elemento, "")
    return txt_resultado

def processar_arquivos(arquivo):
    """Processa uma lista de arquivos e retorna todas as questões"""
    todas_questoes = []

    with open(arquivo, 'r', encoding='utf-8') as f:
        txt = ' '.join(f.read().split('\n'))
        texto = remover_elementos(txt, conf.REMOVER)
        todas_questoes = parse_questoes(texto)

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

