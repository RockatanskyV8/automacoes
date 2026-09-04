ARQUIVO=$1

PASTA=$HOME'/codes/ereader'

pandoc \
    --from markdown-yaml_metadata_block+hard_line_breaks --to epub3 \
    ${ARQUIVO%.*}.md --output ${ARQUIVO%.*}.epub \
    --epub-title-page=false \
    --metadata title="${ARQUIVO%.*}" \
    --lua-filter=$PASTA/pagebreak.lua \
    --lua-filter=$PASTA/emojirmv.lua

ebook-convert ${ARQUIVO%.*}.epub ${ARQUIVO%.*}.mobi

rm *.epub

DESTINO=$HOME'/MOBIs'

mv *.mobi $DESTINO
