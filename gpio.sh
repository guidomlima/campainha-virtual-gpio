 #!/bin/bash

echo "Abrindo pasta GPIO"
if ! cd ~/campainha/campainha-virtual-gpio/
then
    echo "Não foi possível acessar o diretório"
    exit 1
fi

# note que $1 aqui será substituído pelo Bash pelo primeiro argumento passado em linha de comando
if ! ~/campainha/campainha-virtual-gpio/gpio-env/bin/python app.py
then
    echo "Não foi possível iniciar o programa"
    exit 1
fi
echo "GPIO iniciado"
