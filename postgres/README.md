# PostgresSQL init-data.sh

O motivo desse arquivo Dockerfile existir é apenas para inserir o script `init-data.sh` em uma imagem do `Postgres` para que com isso crie as `roles` e `tabelas` do n8n para que os dados sejam persistidos no postgres ao invés do `SQLite`.

## Environment
Antes de fazer o build da imagem crie a variável de ambiente manual ou através do do script `/utils/env_loader.py` após definir na raiz do projeto.

## Build da imagem postgreSQL
Faça o build neste mesmo diretório, fique a vontade para alterar o nome da imagem para o de sua preferência ao invés de `postgres:16.1`.
```bash
docker build -t postgres:16.1 .
```
## Observações
Lembrando que ao iniciar o container do Postgres, apontar para o nome da imagem que criou a partir do Dockerfile, por exemplo: 
```bash
docker container run --name postgres --network n8n img-postgres-dockerfile
```