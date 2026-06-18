ls -l *.txt | awk '{print $NF}' | awk -f ~/codes/tts/reorganizacao/indice.awk

mkdir -p reorganizado
mv *_reorganizado.txt reorganizado
