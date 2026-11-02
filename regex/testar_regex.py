import sys
import readline
import re
from typing import List#, Iterator

def encontrar_tudo(texto: str, padrao_regex: str, flags: int = re.DOTALL):
    padrao_indice_abrangente = re.compile(padrao_regex, flags)
    findall = padrao_indice_abrangente.findall(texto)
    print('tudo')
    print(findall)

def encontrar_partes(textos: List[str], padrao_regex: str, flags: int = re.DOTALL):
    padrao_indice_abrangente = re.compile(padrao_regex, flags)
    for texto in textos:
        match = padrao_indice_abrangente.match(texto.strip())
        print('partes')
        print(match, texto)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 testar_regex.py <caminho_para_arquivo>")
    else:
        textos = sys.argv[1:]
        padrao_regex = input("Digite o padrão: ")
        while not padrao_regex == "sair" :
            encontrar_tudo(' '.join(textos), padrao_regex)
            encontrar_partes(textos, padrao_regex)
            padrao_regex = input("Digite o padrão: ")

        print(padrao_regex)


# (\d+(?:\.\d+)?\s)?\s*([A-ZÀ-Ú][^\n.]*?)\s*\.{3,}\s*(\d+)
# ^(?:\d+)\s(\d(?:\.\d+)*\s*[A-ZÀ-Ú][a-zà-ú\s]+)?

# (\d+(?:\.\d+)*)?\s*([A-ZÀ-Ú][^\n.]*?)\s*\.{3,}\s*(\d+)
