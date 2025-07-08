#!/bin/bash

echo "Carregando variáveis de ambiente do arquivo .env"
cd utils/
python3 env_loader.py
sleep 1
echo 

echo 'Criando o arquivo .env com as variáveis de ambiente em cada diretório!'
echo

echo 'Criando arquivo .env no diretório editor!'
cd ../editor/
python3 exportar_env.py
sleep 1

echo
echo 'Criando arquivo .env no diretório postgres!'
cd ../postgres/
python3 exportar_env.py
sleep 1

echo
echo 'Criando arquivo .env no diretório traefik!'
cd ../traefik/
python3 exportar_env.py
sleep 1

echo
echo 'Criando arquivo .env no diretório webhook!'
cd ../webhook/
python3 exportar_env.py
sleep 1

echo
echo 'Criando arquivo .env no diretório worker!'
cd ../worker/
python3 exportar_env.py