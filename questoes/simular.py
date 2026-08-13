import json
import random

def exibir_questao(questao):
    print(questao["banca"])
    print(questao["enunciado"])
    input("Digite enter para exibir os comentários")
    print("COMENTÁRIO:", questao["comentario"])
    print(questao["gabarito"])
    resposta = input("Acerto ou erro? ")
    return resposta

def processar_arquivos(arquivo, quantidade):
    """Processa uma lista de arquivos e retorna todas as questões"""
    todas_questoes = []

    with open(arquivo, 'r', encoding='utf-8') as f:
        questoes = json.loads(f.read())
        numeros = random.sample(range(0, len(questoes)), quantidade)
        for numero in numeros:
            exibir_questao(questoes[numero])

    return todas_questoes


if __name__ == "__main__":
    processar_arquivos('aula-02_4QuestoesComentadasPreposicaoCebraspe_reorganizado.json', 5)

#arquivos = [
#    '/home/lucas/Documentos/Concurso/Core/estatistica/SEFAZ/reorganizado/QuestoesComentadas/aula-01_5QuestoesComentadasAlgebradeProposicoesCebraspe_reorganizado.txt',
#    '/home/lucas/Documentos/Concurso/Core/estatistica/SEFAZ/reorganizado/QuestoesComentadas/aula-02_5QuestoesComentadasProposicoesQuantificadasCebraspe_reorganizado.txt',
#    '/home/lucas/Documentos/Concurso/Core/DireitoAdministrativo/SEFAZ/reorganizado/QuestoesComentadas/aula-05_9QuestoesComentadasPoderesdaAdministracaoPublica_reorganizado.txt'
#]

