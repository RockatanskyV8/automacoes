import re
import sys
import logging
from collections import defaultdict
from typing import List, Dict, Tuple, Any, Iterator

class Conteudo:

    def identificar_presenca_de_pontos(self, pagina: str):
        tem_pontos = re.search(self.padrao_pontos, pagina) is not None
        return tem_pontos

    def pontos_por_quebra_de_linhas(self) -> Iterator[List[str]]:
        try:
            for pagina in range(1, 11): #enumerate(self.informacoes):
                pagina_atual = '\n'.join(self.informacoes[str(pagina)])
                if self.identificar_presenca_de_pontos(pagina_atual):
                    pagina_atual_info = re.sub(self.padrao_pontos, '\n', pagina_atual) # Substitui os pontos por uma quebra de linha
                    yield pagina_atual_info.split('\n')
        except(KeyError):
            print("Documento muito curto, provavelmente sem conteúdo relevante")
            yield {"":""}

    def linhas_com_pontos(self) -> Iterator[List[str]]:
        try:
            for pagina in range(1, 11): #enumerate(self.informacoes):
                pagina_atual = '\n'.join(self.informacoes[str(pagina)])
                if self.identificar_presenca_de_pontos(pagina_atual):
                    yield pagina_atual
        except(KeyError):
            print("Documento muito curto, provavelmente sem conteúdo relevante")
            yield {"":""}

    def __init__(self, informacoes):
        self.informacoes = informacoes
        self.padrao_pontos = r'\.{2,}'



class Indice:

    def _extrair_paginas(self, titulos: List[Tuple[str, int]], conteudo: List[str]) -> Iterator[List[str]]:
        inicio: int = len(titulos)
        if (inicio > 0):
            for i in range(1, len(titulos)):
                titulo_atual, posicao_atual = titulos[i-1]
                _, posicao_proximo = titulos[i]
    
                numeros_entre = list(range(posicao_atual + 1, posicao_proximo))
                conteudo_numeros_entre = [conteudo[numero].strip() for numero in numeros_entre if len(conteudo[numero])]
                paginas_completas = [conteudo[posicao_atual - 1].strip(), *conteudo_numeros_entre]
                paginas_completas_apenas_num = [pagina for pagina in paginas_completas if len(pagina) and pagina.isdigit()]
    
                menor = min(paginas_completas_apenas_num)
    
                if int(menor) < inicio:
                    inicio = int(min(paginas_completas_apenas_num))
    
                yield paginas_completas_apenas_num

            ultimo_titulo, ultima_posicao = titulos[-1]
            ultimos_numeros = list(range(ultima_posicao + 1, len(conteudo) - 1))
            conteudo_ultimos_numeros = [conteudo[numero].strip() for numero in ultimos_numeros if conteudo[numero].isdigit() and int(conteudo[numero]) > inicio]
            yield [conteudo[ultima_posicao - 1].strip(), *conteudo_ultimos_numeros]

    def _encontrar_texto(self, conteudo: List[str], flags: int = re.DOTALL) -> Iterator[List[str]]:
        padrao_indice_abrangente = re.compile(
            self.padrao_regex,
            flags
        )

        for titulo in conteudo:
            idx = conteudo.index(titulo)
            titulo_strip = titulo.strip()
            resultados = padrao_indice_abrangente.match(titulo_strip)
            if resultados:
                yield (titulo_strip, idx)

    def _indice_organizado(self, titulos: List[Tuple[str, int]], paginas: List[List[str]]) -> Dict[str, str]:
        indice: Dict[str, str] = defaultdict(list)  # type: ignore
        for i in range(len(titulos)):
            titulo, _ = titulos[i]
            pagina_num = [int(pagina.strip()) for pagina in paginas[i] if pagina.isdigit()]
            if len(pagina_num):
                numero = str(min(pagina_num))
                titulo_limpo = ' '.join(titulo.split())
                indice[numero] = titulo_limpo

        return dict(indice)

    def _extrair_indice(self) -> Dict[str, str]:
        """
        Extrai o índice de um arquivo de texto com base em um padrão de numeração
        seguido por título e número de página.

        Args:
            caminho_arquivo (str): O caminho para o arquivo de texto.

        Returns:
            list: Uma lista de tuplas (número, título, página) ou None em caso de erro.
        """
        conteudos: List[List[str]] = Conteudo(self.informacoes).pontos_por_quebra_de_linhas()
        try:
            indice_total: Dict[str, str] = {}
            for c in conteudos:
                titulos: List[Tuple[str, int]] = list(self._encontrar_texto(c))
                paginas: List[List[str]] = list(self._extrair_paginas(titulos, c))
                resultados = self._indice_organizado(titulos, paginas)
                indice_total = indice_total | resultados

            return indice_total
        except(KeyError):
             print("Documento muito curto, provavelmente sem conteúdo relevante")
             return {"":""}
        except Exception:
             logging.exception("### Erro de índice ###")
             return {}

    def __init__(self, informacoes: Dict[str, List[str]], padrao_regex: str = r'(\d+)(\)|-)\s*(.*?)\s') -> None:
        self.informacoes: Dict[str, List[str]] = informacoes
        self.padrao_regex: str = padrao_regex
        self.indice = self._extrair_indice()

    def __len__(self):
        return len(self.indice)

    def __str__(self):
        return str(self.indice)

    def __iter__(self):
        return iter(self.indice)

    def get_ou_padrao(self, chave: str, padrao: str = None):
        return self.indice.get(chave, padrao)

class IndiceAlinhado(Indice):

    def _encontrar_texto(self, conteudo: str, flags: int = re.DOTALL) -> Iterator[List[str]]:
        padrao_indice_abrangente = re.compile(self.padrao_regex, flags)

        resultados = padrao_indice_abrangente.findall(conteudo)
        return resultados

    def _indice_organizado(self, titulos: List[Tuple[str, str, str]]) -> Dict[str, str]:
        indice: Dict[str, str] = defaultdict(list)  # type: ignore
        for titulo in titulos:
            sessao, ttl, pagina = titulo
            nome = ' '.join([sessao, ttl])
            titulo_limpo = ' '.join(nome.split())
            indice.setdefault(pagina, titulo_limpo)

        return dict(indice)

    def _extrair_indice(self):
        conteudos: List[List[str]] = Conteudo(self.informacoes).linhas_com_pontos()
        try:
            indice_total: Dict[str, str] = {}
            for c in conteudos:
                titulos: List[Tuple[str, str, str]] = list(self._encontrar_texto(c))
                resultados = self._indice_organizado(titulos)
                indice_total = indice_total | resultados

            return indice_total
        except(KeyError):
             print("Documento muito curto, provavelmente sem conteúdo relevante")
             return {"":""}
        except Exception:
             logging.exception("### Erro de índice ###")
             return {}


    def __init__(self, informacoes: Dict[str, List[str]], padrao_regex: str = r'(\d+(?:\.\d+)*)?\s*([A-ZÀ-Ú][^\n.]*?)\s*\.{3,}\s*(\d+)') -> None:
        self.informacoes: Dict[str, List[str]] = informacoes
        self.padrao_regex: str = padrao_regex
        self.indice = self._extrair_indice()

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
            divis_info = divis.dicionarizar()

            indx = IndiceAlinhado(divis_info)
            print(str(indx))
            print(len(indx))



