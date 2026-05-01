-- hr_to_pagebreak.lua
-- Converte divisórias horizontais '---' em quebras de página

function HorizontalRule()
	-- Substitui <hr/> por uma quebra de página
	return pandoc.RawBlock("html", '<div style="page-break-before: always;"></div>')
end
