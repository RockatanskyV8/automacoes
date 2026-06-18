#!/usr/bin/awk -f

# Script para emparelhar arquivos de curso com seus índices correspondentes
# Uso: awk -f emparelha.awk arquivos.txt

BEGIN {
    # Inicializa arrays
    split("", aulas)
    split("", indices)
}

{
    # Verifica se é arquivo de aula (começa com "curso-")
    if ($0 ~ /^curso-.*-aula-([0-9]+)-.*\.txt$/) {
        # Extrai o número da aula
        match($0, /-aula-([0-9]+)-/, arr)
        num_aula = arr[1]
        
        # Armazena o arquivo de aula no array usando o número como chave
        aulas[num_aula] = $0
        
    }
    # Verifica se é arquivo de índice (começa com "indice-")
    else if ($0 ~ /^indice-([0-9]+)\.txt$/) {
        # Extrai o número do índice
        match($0, /^indice-([0-9]+)\.txt$/, arr)
        num_indice = arr[1]
        
        # Armazena o arquivo de índice
        indices[num_indice] = $0
    }
}

END {
    # Percorre todas as aulas (do 00 ao 14)
    for (i = 0; i <= 14; i++) {
        # Formata o número da aula com dois dígitos
        num = sprintf("%02d", i)
        
        # Se existe arquivo de aula para este número
        if (num in aulas) {
            # Se existe índice correspondente
            if (num in indices) {
                #printf aulas[num] " " indices[num] "\n"
                system("~/codes/tts/audio/bin/python3 ~/codes/tts/reorganizacao/reorganizar_texto_sep.py " indices[num] " " aulas[num] ";")
            } else {
                print aulas[num] " " indices[num] ? indices[num] : "(índice não encontrado)", ""
            }
        }
    }
    
}

