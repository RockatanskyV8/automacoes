python3 ~/codes/tts/reorganizacao/reorganizar_texto_min.py $@

mkdir -p reorganizado
mv *_reorganizado.txt reorganizado

#python3 ~/codes/tts/divisao/dividir_texto.py $@
#python3 ~/codes/tts/reorganizacao/reorganizar_texto.py *_divido.txt
#python3 ~/codes/tts/reorganizacao/indice.py *_divido.txt | python3 ~/codes/tts/reorganizacao/reorganizar_texto_min.py *_divido.txt

#mv *_divido.txt dividido
#mv *_reorganizado.txt reorganizado

#sed -i '/^$/d' $1
#sed -i '/^[[:space:]]*$/d' $1
