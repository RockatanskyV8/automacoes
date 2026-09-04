-- Filtro otimizado para remover emojis sem quebrar a estrutura do Pandoc

local function remove_emojis_from_string(str)
    -- Mantém seu padrão original de captura de bytes UTF-8 para emojis
    local emoji_pattern = "[\226-\244][\128-\191][\128-\191]"
    return str:gsub(emoji_pattern, "")
end

-- Aplica a remoção APENAS em elementos de texto dentro do corpo do documento
function Str(elem)
    local novo_texto = remove_emojis_from_string(elem.text)
    if novo_texto == "" then
        return {} -- Remove o elemento se ele virou uma string vazia
    end
    elem.text = novo_texto
    return elem -- Retorna o elemento modificado preservando seu tipo original
end
