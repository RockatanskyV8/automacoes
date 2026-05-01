
def criar_novo_arquivo(novo_nome_arquivo, informacao_do_titulo):
    if len(novo_nome_arquivo) < 90:
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
    else:
        print(f"Novo nome de arquivo,{novo_nome_arquivo}, muito longo")
        return None

def abrir_arquivo(arquivo):
    informacao = []
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

