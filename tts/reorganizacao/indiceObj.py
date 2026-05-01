import re
import sys
import os
from collections import defaultdict

class Indice():

    def __init__(self, informacoes, padrao_regex = r'(\d+)(\)|-)\s*(.*?)\s'):
        self.informacoes = informacoes
        self.padrao_regex = padrao_regex

    def encontrar_texto(self, conteudo, flags=re.DOTALL):
        padrao_indice_abrangente = re.compile(
            self.padrao_regex,
            flags
        )

        titulos = []
        for titulo in conteudo:
            idx = conteudo.index(titulo)
            titulo_strip = titulo.strip()
            resultados = padrao_indice_abrangente.match(titulo_strip)
            if resultados:
                titulos.append((titulo_strip, idx))

        paginas = []
        if len(titulos):
            paginas = self.extrair_paginas(titulos, conteudo)

        return self.indice_organizado(titulos, paginas)

    def extrair_paginas(self, titulos, conteudo):
        paginas = []
        for i in range(len(titulos) - 1):
            titulo_atual, posicao_atual = titulos[i]
            titulo_proximo, posicao_proximo = titulos[i+1]

            numeros_entre = list(range(posicao_atual + 1, posicao_proximo))
            conteudo_numeros_entre = [conteudo[numero].strip() for numero in numeros_entre]

            paginas.append([ conteudo[posicao_atual - 1].strip(), *conteudo_numeros_entre ])
 
        ultimo_titulo, ultima_posicao = titulos[-1]
        ultimos_numeros = list(range(ultima_posicao + 1, len(conteudo) - 1))
        conteudo_ultimos_numeros = [conteudo[numero].strip() for numero in ultimos_numeros if conteudo[numero].isdigit()]
        paginas.append([conteudo[ultima_posicao - 1].strip(), *conteudo_ultimos_numeros ])

        return paginas


    def indice_organizado(self, titulos, paginas):
        indice = defaultdict(list)
        for i in range(len(titulos)):
            titulo, _ = titulos[i]
            #print(titulo, paginas[i])
            numero = min([pagina.strip() for pagina in paginas[i] if pagina.isdigit()])
            titulo_limpo = ' '.join(titulo.split())
            indice[numero] = titulo_limpo

        return dict(indice)

    def indice_separado(self, resultados):
        indice = defaultdict(list)
        for _, titulo, _, pagina in resultados:
            titulo_limpo = ' '.join(titulo.split()) # Limpa o título de espaços extras, sem regex
            #titulo_limpo = re.sub(r'\s+', ' ', titulo).strip() # Limpa o título de espaços extras
            indice[pagina] = titulo_limpo
    
        return dict(indice)

    def extrair_indice(self):
        """
        Extrai o índice de um arquivo de texto com base em um padrão de numeração
        seguido por título e número de página.
     
        Args:
            caminho_arquivo (str): O caminho para o arquivo de texto.
     
        Returns:
            list: Uma lista de tuplas (número, título, página) ou None em caso de erro.
        """
        conteudos = []
        for pagina in range(1, 11): #enumerate(self.informacoes):
            pagina_atual = '\n'.join(self.informacoes[str(pagina)])
            padrao_pontos = r'\.{2,}'
            tem_pontos = re.search(padrao_pontos, pagina_atual) is not None
            if tem_pontos:
                pagina_atual_info = re.sub(padrao_pontos, '\n', pagina_atual)
                conteudos.append(pagina_atual_info.split('\n'))
        indice_total = {}
        for c in conteudos:
            resultados = self.encontrar_texto(c)
            indice_total = indice_total | resultados 

        return indice_total
        #return self.indice_separado(resultados)

    def testar_extrair_indice(self, pag):
        conteudo = self.informacoes[pag]
        resultados = self.encontrar_texto(conteudo)
        return resultados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 indiceObj.py <caminho_para_arquivo>")
        sys.exit(1)




