#!/bin/bash

echo "Start Postgres"
cd postgres/
docker container run -dti --rm --name postgres --env-file .env -p 5432:5432 -v postgres_data:/var/lib/postgresql/data --network n8n postgres:16.1
sleep 1

echo "Start Redis"
docker container run -dti --rm --name redis-n8n -p 6379:6379 -v redis_data:/data --network n8n redis:8.2-m01-alpine
sleep 1

echo "Start Cloudflare Tunnel"
cd ../tunel
docker run -d --rm --name cloudflare-tunnel --network n8n -v $(pwd)/cloudflare_token.txt:/etc/cloudflared/token.txt:ro  cloudflare/cloudflared:latest tunnel --no-autoupdate run --token-file /etc/cloudflared/token.txt
sleep 1

echo "Start Editor"
cd ../editor
docker container run -dti --rm --name n8n-editor --env-file .env -p 5678:5678 -v n8n_data:/home/node/ --network n8n n8nio/n8n:latest
sleep 1

echo "Start Worker"
cd ../worker
docker container run -dti --rm --name n8n-worker-01 --env-file .env -v n8n_data:/home/node/ --network n8n n8nio/n8n:latest worker --concurrency=5
sleep 1

echo "Start Webhook + Traefik"
cd ../webhook
docker compose up -d --remove-orphans

clear
echo "Containers em Execução"
echo
docker ps