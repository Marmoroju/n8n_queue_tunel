# Configurações dos workers

Para cara worker altere o número final em `--name n8n-worker-01` conforme a quantidade desejada alterando somente o número do worker. As variáveis de ambiente deverão serem as mesmas tanto para o editor quanto para os workers.
```bash
docker container run -dti --rm --name n8n-worker-01 --env-file .env -v n8n_data:/home/node/ --network n8n --restart always docker.n8n.io/n8nio/n8n worker --concurrency=5
```

- argumento: `--concurrency=5` define a quantidade de workflows simultâneos que o worker executará.

### Workers on? Logs
Para saber se o worker está recebendo os workflows basta digitar o seguinte comando no terminal:
```bash 
watch docker logs id-container-worker
``` 
Se forem muitas execuções de workflow você pode visualizar as saídas através dos logs dentro do container:
```bash
#editor
docker exec -it <id-container> cat /home/node/.n8n/n8nEventLog.log

# Worker
docker exec -it <id-container> cat /home/node/.n8n/n8nEventLog-worker.log

# tee -> Envia a saída do comando para um arquivo
<comando> | tee editor.txt
```
Depois executar o workflow e acompanhar, se o retorno for algo como`Worker started execution 46 (job 1) Worker finished execution 46 (job 1)`, então Workers on!

O mesmo vale para o editor, se o retorno for `Enqueued execution 46 (job 1) Execution 46 (job 1) finished successfully`, então Editor on!