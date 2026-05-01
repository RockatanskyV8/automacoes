ARQUIVO=$1

PASTA=$HOME'/codes/ereader'

pandoc \
  --from markdown --to epub3 \
  ${ARQUIVO%.*}.md --output ${ARQUIVO%.*}.epub \
  -f markdown+hard_line_breaks \
  --epub-title-page=false \
  --metadata title="${ARQUIVO%.*}" \
  --lua-filter=$PASTA/pagebreak.lua \
  --lua-filter=$PASTA/emojirmv.lua

ebook-convert ${ARQUIVO%.*}.epub ${ARQUIVO%.*}.mobi

rm *.epub

DESTINO=$HOME'/Documentos/Concurso/1MeusPDFs'

mv *.mobi $DESTINO
