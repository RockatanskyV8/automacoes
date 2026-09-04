import re
import sys
from collections import defaultdict
from typing import List, Dict, Tuple, Any

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
        inicio: int = len(titulos)
        paginas: List[List[str]] = []
        for i in range(1, len(titulos)):
            titulo_atual, posicao_atual = titulos[i-1]
            titulo_proximo, posicao_proximo = titulos[i]

            numeros_entre = list(range(posicao_atual + 1, posicao_proximo))
            conteudo_numeros_entre = [conteudo[numero].strip() for numero in numeros_entre if len(conteudo[numero])]
            paginas_completas = [conteudo[posicao_atual - 1].strip(), *conteudo_numeros_entre]
            paginas_completas_apenas_num = [pagina for pagina in paginas_completas if len(pagina) and pagina.isdigit()]

            menor = min(paginas_completas_apenas_num)

            if int(menor) < inicio:
                inicio = int(min(paginas_completas_apenas_num))

            paginas.append(paginas_completas_apenas_num)

        ultimo_titulo, ultima_posicao = titulos[-1]
        ultimos_numeros = list(range(ultima_posicao + 1, len(conteudo) - 1))
        conteudo_ultimos_numeros = [conteudo[numero].strip() for numero in ultimos_numeros if conteudo[numero].isdigit() and int(conteudo[numero]) > inicio]
        paginas.append([conteudo[ultima_posicao - 1].strip(), *conteudo_ultimos_numeros])

        return paginas

    def indice_organizado(self, titulos: List[Tuple[str, int]], paginas: List[List[str]]) -> Dict[str, str]:
        indice: Dict[str, str] = defaultdict(list)  # type: ignore
        for i in range(len(titulos)):
            titulo, _ = titulos[i]
            pagina_num = [int(pagina.strip()) for pagina in paginas[i] if pagina.isdigit()]
            if len(pagina_num):
                numero = str(min(pagina_num))
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

        try :
            conteudos: List[List[str]] = []
            for pagina in range(1, 11): #enumerate(self.informacoes):
                pagina_atual = '\n'.join(self.informacoes[str(pagina)])
                padrao_pontos = r'\.{2,}'
                tem_pontos = re.search(padrao_pontos, pagina_atual) is not None
                if tem_pontos:
                    pagina_atual_info = re.sub(padrao_pontos, '\n', pagina_atual) # Substitui os pontos por uma quebra de linha
                    conteudos.append(pagina_atual_info.split('\n'))

            indice_total: Dict[str, str] = {}
            for c in conteudos:
                resultados = self.encontrar_texto(c)
                indice_total = indice_total | resultados
            print(indice_total)

            return indice_total
            #return self.indice_separado(resultados)
        except(KeyError):
             print("Documento muito curto, provavelmente sem conteúdo relevante")
             return {"":""}

    def testar_extrair_indice(self, pag: str) -> Dict[str, str]:
        conteudo = ' '.join(self.informacoes[pag])
        padrao_pontos = r'\.{2,}'
        conteudo = re.sub(padrao_pontos, '\n', conteudo)
        print(conteudo.strip())
        padrao_indice_abrangente = re.compile(
            self.padrao_regex,
            re.DOTALL
        )
        #for palavra in conteudo:
        resultados = padrao_indice_abrangente.findall(conteudo.strip())
        print(resultados)

        #resultados = padrao_indice_abrangente.match(conteudo)
        #return resultados

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 indiceObj.py <caminho_para_arquivo>")
    else:
        from dividir_texto import Divisao
        import manipulacao_arquivos as m_arq
        import confidencial as conf

        dados_entrada = sys.argv[1:]
        for dados in dados_entrada:
            informacao = m_arq.abrir_arquivo(dados)

            DIVISOR = conf.DIVISOR
            divis = Divisao(DIVISOR, informacao)
            divis_info = divis.dividir()
#           print(divis_info['2'])

            PADRAO_REGEX = r'(\d+?)\s*\–\s*(.*?)\n'
            #PADRAO_REGEX = r'(\d+)(\.)\s*(.*?)\n'
            #(\d+)(\)|-)\s*(.*?)\s
            indx = Indice(divis_info, PADRAO_REGEX)
            indx.exbir_possivel_indice()
            #indx = Indice(divis_info)
            #indx.testar_extrair_indice('2')
            #indx.testar_extrair_indice('3')
            #indx.testar_extrair_indice('4')

            #print("idx_extraido\n", indx_extraido)



