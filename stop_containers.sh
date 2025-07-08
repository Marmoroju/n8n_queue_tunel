#!/bin/bash

echo "Parando todos os containers..."

cd webhook/
docker compose down
sleep 1

echo
docker stop $(docker ps -a -q)

echo
echo "Todos os containers foram parados."
echo
docker ps
