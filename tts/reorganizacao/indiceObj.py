import re
import sys
import os
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Any, Union

class Indice():

    def __init__(self, informacoes: Dict[str, List[str]], padrao_regex: str = r'(\d+)(\)|-)\s*(.*?)\s') -> None:
        self.informacoes: Dict[str, List[str]] = informacoes
        self.padrao_regex: str = padrao_regex

    def encontrar_texto(self, conteudo: List[str], flags: int = re.DOTALL) -> Dict[str, str]:
        padrao_indice_abrangente = re.compile(
            self.padrao_regex,
            flags
        )

        titulos: List[Tuple[str, int]] = []
        for titulo in conteudo:
            idx = conteudo.index(titulo)
            titulo_strip = titulo.strip()
            resultados = padrao_indice_abrangente.match(titulo_strip)
            if resultados:
                titulos.append((titulo_strip, idx))

        paginas: List[List[str]] = []
        if len(titulos):
            paginas = self.extrair_paginas(titulos, conteudo)

        return self.indice_organizado(titulos, paginas)

    def extrair_paginas(self, titulos: List[Tuple[str, int]], conteudo: List[str]) -> List[List[str]]:
        paginas: List[List[str]] = []
        for i in range(len(titulos) - 1):
            titulo_atual, posicao_atual = titulos[i]
            titulo_proximo, posicao_proximo = titulos[i+1]

            numeros_entre = list(range(posicao_atual + 1, posicao_proximo))
            conteudo_numeros_entre = [conteudo[numero].strip() for numero in numeros_entre]

            paginas.append([conteudo[posicao_atual - 1].strip(), *conteudo_numeros_entre])

        ultimo_titulo, ultima_posicao = titulos[-1]
        ultimos_numeros = list(range(ultima_posicao + 1, len(conteudo) - 1))
        conteudo_ultimos_numeros = [conteudo[numero].strip() for numero in ultimos_numeros if conteudo[numero].isdigit()]
        paginas.append([conteudo[ultima_posicao - 1].strip(), *conteudo_ultimos_numeros])

        return paginas

    def indice_organizado(self, titulos: List[Tuple[str, int]], paginas: List[List[str]]) -> Dict[str, str]:
        indice: Dict[str, str] = defaultdict(list)  # type: ignore
        for i in range(len(titulos)):
            titulo, _ = titulos[i]
            print(titulo, paginas[i])
            pagina_num = [pagina.strip() for pagina in paginas[i] if pagina.isdigit()]
            if len(pagina_num):
                numero = min(pagina_num)
                titulo_limpo = ' '.join(titulo.split())
                indice[numero] = titulo_limpo

        return dict(indice)

    def indice_separado(self, resultados: List[Tuple[Any, str, Any, str]]) -> Dict[str, str]:
        indice: Dict[str, str] = defaultdict(list)  # type: ignore
        for _, titulo, _, pagina in resultados:
            titulo_limpo = ' '.join(titulo.split()) # Limpa o título de espaços extras, sem regex
            #titulo_limpo = re.sub(r'\s+', ' ', titulo).strip() # Limpa o título de espaços extras
            indice[pagina] = titulo_limpo

        return dict(indice)

    def extrair_indice(self) -> Dict[str, str]:
        """
        Extrai o índice de um arquivo de texto com base em um padrão de numeração
        seguido por título e número de página.

        Args:
            caminho_arquivo (str): O caminho para o arquivo de texto.

        Returns:
            list: Uma lista de tuplas (número, título, página) ou None em caso de erro.
        """
        conteudos: List[List[str]] = []
        for pagina in range(1, 11): #enumerate(self.informacoes):
            pagina_atual = '\n'.join(self.informacoes[str(pagina)])
            padrao_pontos = r'\.{2,}'
            tem_pontos = re.search(padrao_pontos, pagina_atual) is not None
            if tem_pontos:
                pagina_atual_info = re.sub(padrao_pontos, '\n', pagina_atual)
                conteudos.append(pagina_atual_info.split('\n'))
        indice_total: Dict[str, str] = {}
        for c in conteudos:
            resultados = self.encontrar_texto(c)
            indice_total = indice_total | resultados

        return indice_total
        #return self.indice_separado(resultados)

    def testar_extrair_indice(self, pag: str) -> Dict[str, str]:
        conteudo = self.informacoes[pag]
        resultados = self.encontrar_texto(conteudo)
        return resultados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 indiceObj.py <caminho_para_arquivo>")
        sys.exit(1)
