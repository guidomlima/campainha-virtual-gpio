 #!/bin/bash

echo "Abrindo pasta API"
if ! cd ~/campainha/campainha-virtual-api/
then
    echo "Não foi possível acessar o diretório"
    exit 1
fi

# note que $1 aqui será substituído pelo Bash pelo primeiro argumento passado em linha de comando
if ! ~/campainha/campainha-virtual-api/api-env/bin/python app.py
then
    echo "Não foi possível iniciar o programa"
    exit 1
fi
echo "API iniciada"
