

pandoc -f markdown -t plain --wrap=preserve $1 | piper --model ~/codes/tts/vozes/pt_BR-cadu-medium.onnx --output_file $2; 

