
from typing import List, Optional

def criar_novo_arquivo(novo_nome_arquivo: str, informacao_do_titulo: List[str]) -> None:
    """
    Cria um novo arquivo e escreve as linhas de informação, excluindo linhas que são apenas números.

    Args:
        novo_nome_arquivo: Nome do arquivo a ser criado/atualizado
        informacao_do_titulo: Lista de strings a serem escritas no arquivo

    Returns:
        None
    """
    try:
        with open(novo_nome_arquivo, "a") as saida:
            for linha in informacao_do_titulo:
                if not linha.strip().isnumeric():
                    saida.write(linha.strip() + "\n")
            print(novo_nome_arquivo)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {novo_nome_arquivo}")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

def abrir_arquivo(arquivo: str) -> Optional[List[str]]:
    """
    Abre um arquivo e lê todas as suas linhas.

    Args:
        arquivo: Caminho para o arquivo a ser lido

    Returns:
        Optional[List[str]]: Lista de strings contendo as linhas do arquivo,
                            ou None em caso de erro
    """
    informacao: List[str] = []
    try:
        with open(arquivo, "r") as f:
            for i, linha in enumerate(f, 1):
                linha = linha.strip()
                informacao.append(linha)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {arquivo}")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

    return informacao
