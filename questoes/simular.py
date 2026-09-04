import json
import random

def exibir_questao(questao):
    questao_atual = []
    questao_atual.append(f"### {questao["numero"]}.{questao["banca"]}")
    questao_atual.append(questao["enunciado"])
    questao_atual.append("---")
    return questao_atual

def exibir_gabarito(questao):
    gabarito_atual = []
    gabarito_atual.append(f"### {questao["numero"]}.{questao["banca"]}")
    gabarito_atual.append(questao["comentario"])
    gabarito_atual.append(questao["gabarito"])
    gabarito_atual.append("---")
    return gabarito_atual


def processar_arquivos(arquivo, quantidade):
    """Processa uma lista de arquivos e retorna todas as questões"""
    todas_questoes = []
    todos_gabaritos = []
    with open(arquivo, 'r', encoding='utf-8') as f:
        questoes = json.loads(f.read())
        numeros = random.sample(range(0, len(questoes)), quantidade)
        for numero in numeros:
            todas_questoes.append(exibir_questao(questoes[numero]))
            todos_gabaritos.append(exibir_gabarito(questoes[numero]))
    return todas_questoes, todos_gabaritos

def criar_arquivos(questoes, gabaritos):
    with open("questionario1.md", 'w', encoding='utf-8') as f:
        for questao in questoes:
            f.write("\n".join(questao))
            f.write("\n")

    with open("gabarito1.md", 'w', encoding='utf-8') as f:
        for gabarito in gabaritos:
            f.write("\n".join(gabarito))
            f.write("\n")


if __name__ == "__main__":
    questoes, gabaritos = processar_arquivos('aula-02_4QuestoesComentadasPreposicaoCebraspe_reorganizado.json', 5)
    criar_arquivos(questoes, gabaritos)

