#import sys
from collections import defaultdict
from typing import List, Dict, Any

class Divisao():

    def __init__(self, divisor: str, informacao: List[str], remover: List[str] = []) -> None:
        self.divisor: str = divisor
        self.informacao: List[str] = informacao
        self.remover: List[str] = remover

    def remover_elementos(self) -> None:
        """
        Remove elementos da lista informacao conforme especificado em self.remover.
        Renomeado de 'remover' para evitar conflito com o atributo.
        """
        try:
            for item in self.remover:
                self.informacao.remove(item)
        except ValueError as e:
            print(f"Erro: {e}")

    def dividir(self) -> Dict[str, List[str]]:
        """
        Divide a informação em páginas baseado no divisor.

        Returns:
            Dict[str, List[str]]: Dicionário onde as chaves são números de página (como strings)
                                 e os valores são listas de linhas da página.
        """
        compilado: Dict[str, List[str]] = defaultdict(list)
        pagina: int = 0

        for linha in self.informacao:
            linha_strip: str = linha.strip()

            if linha_strip == self.divisor:
                pagina += 1
            else:
                compilado[str(pagina)].append(linha)

        return dict(compilado)
