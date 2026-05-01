-- remove_emojis.lua
function string_contains_emoji(str)
	-- Verifica se a string contém emojis
	for code in str:gmatch("[\226-\244][\128-\191][\128-\191]") do
		return true
	end
	return false
end

function Str(elem)
	-- Remove emojis do texto
	local text = elem.text
	-- Padrão para capturar emojis comuns
	local emoji_pattern = "[\226-\244][\128-\191][\128-\191]"
	text = text:gsub(emoji_pattern, "")
	if text == "" then
		return {} -- Remove o elemento completamente se só tinha emoji
	end
	return pandoc.Str(text)
end
