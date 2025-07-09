# N8N MODO FILA
 
## Documentação de apoio
- [n8n - docker](https://docs.n8n.io/hosting/installation/docker/)
- [Postgres - Dockerhub](https://hub.docker.com/_/postgres)
- [Redis - Dockerhub](https://hub.docker.com/_/redis)
- [Cloudflare](https://www.cloudflare.com/pt-br/)
- [Traefik](https://doc.traefik.io/traefik/https/acme/)
- [QUIC - Doc](https://github.com/quic-go/quic-go/wiki/UDP-Buffer-Sizes)


## Leia antes de iniciar

0. É preciso um domínio e ter ele configurado na Cloudflare
1. Uma instância/servidor linux, pode ser pelo WSL (testes).
2. instalar o Docker e dar permissão para seu usuário para evitar executar containers através do root;
3. Chave de criptografia para comunicação entre o Editor, Workers e Webhook em modo fila que pode ser gerada através do terminal ou através de outro programa e armazenado na variável de ambiente `N8N_ENCRYPTION_KEY`;
4. Criação de volumes através do Docker ou em um diretório de sua preferência para persistência dos dados;
4. Criação de uma rede interna no docker para que os serviços se comuniquem;
6. Criação e modificação dos arquivos de variável de ambiente em cada diretório. Pode ser criado um arquivo geral só que ao utilizar o `docker inspect id-container` este recebe até a variáveis que não lhe pertence;
7. Entendimento dos diretórios
```bash
# Dentro dos diretórios estão as instruções no arquivo README.md

# Diretórios principais de configuração do n8n: editor - postgres - tunel - worker - webhook

# A execução do banco de dados Redis pode ser iniciada de qualquer diretório, pois ele atenderá somente como um message brokers.

# Os diretórios tunel e traefik servem para testar estes serviços antes de serem apontados para o webhook. Siga essa ordem do que testar:

# 1º: Tunel Cloudflare + Nginx
# 2º: Tunel Cloudflare + Webhook [POST] + Reqbin
# 3º: Tunel Cloudflare + Traefik + Nginx
# 4º: Tunel Cloudflare + Traefik + Nginx + Let's Encryptt
# 5º: Tunel Cloudflare + Traefik + Webhook [POST] + Let's Encrypt + Reqbin

# No final deste README contém uma tag chamada "Quality of Life" seguidas de tags 'QOF' que explicam a respeito dos scripts python e shell, arquivos .env e etc.
```

8. Ordem de execução (manual) dos containers após criar as variáveis de ambiente, volumes e rede. 
```bash 
1º: Postgres
2º: Redis
3º: Cloudflare Tunnel
4º: Editor
5º: Workers
6º: Traefik
7º: Webhook
```
9. Antes de chegar ao caminho feliz, teste container por container e sua cominicação com o ambiente.

## CONFIGURAÇÕES

### Domínio
Para utilizar o webhook e traefik, mesmo local, será necessário possuir um domínio ou comprar um, caso não tenha. Pode ser pela Hostinger, Registro.br, Hostgator ou qualquer outro.

Obs.: Ao comprar o domínio na Hostinger, tive que deslogar na plataforma e logar novamente para aparecer o domínio e terminar de configurar o registro.

- Para teste, desative a opção "Renovação Automática"
- Ative a autenticação em dois fatores
- Pode levar de 15 minutos a 24 horas para que os domínios comecem a funcionar

### Cloudflare
A partir do domínio existente ou criado, a próxima etapa será passar o apontamento  para a Cloudflare, isto é, agora ela quem irá gerenciar seu domínio.

Esse serviço irá trazer mais proteção para a aplicação, pois servirá como uma barreira/filtro entre as conexões.

- Conecte seu domínio à Cloudflare
- Procure pelo registro de seu domínio, por exemplo, `seudominio.online`
- Escolha o tipo de plano
- Com os dois nomes aleatórios de DNS disponibilizados pela Cloudflare, copie-os e substitua no provedor de seu domínio, eles devem estar como ns1.dns e ns2.dns
- Pode levar de 15 minutos a 24 horas para o domínio se propagar com os novos servidores de DNS.
- No menu `DNS` criar o filtro CNAME e A

### Volumes - Docker - Backup
Caso decida seguir a criação de volume padrão descrita aqui, estes são os locais de armazenamento interno do Docker. Quando fizer a configuração de backup, aponte para estes locais abaixo.
```bash 
# Ficam neste caminho abaixo e são acessados como root.
/var/lib/docker/volumes/VOLUME_CRIADO/_data
 
# Os arquivos no n8n ficam em diretórios ocultos
/var/lib/docker/volumes/VOLUME_CRIADO/_data.cache 
/var/lib/docker/volumes/VOLUME_CRIADO/_data.n8n 
```

### Instalação do docker
```bash
curl -fsSL https://get.docker.com | bash

```
### Permissão para executar o docker com usuário não-root
```bash
sudo usermod -aG docker meu-usuario

newgrp docker
```
### N8N_ENCRYPTION_KEY
Gera chave aleatória de criptografia com 40 caracteres através do terminal
```bash
tr -dc A-Za-z0-9 < /dev/urandom | head -c 40
```

### Docker Volume n8n
```bash
docker volume create n8n_data
```

### Docker Volume Postgres
```bash
docker volume create postgres_data
```

### Docker Volume Redis
```bash
docker volume create redis_data
```

### Docker network 
Os containers precisam estar na mesma rede para se enxergarem. Assim é possível substituir o `sqlite` padrão do n8n pelo `postgres`, por exemplo.
```bash
docker network create n8n
```

## Execução manual dos containers básicos antes de executar o scripts automatizados

### PostgreeSQL
Antes de executar este conteiner, acesse o diretório `postgres` para criar a imagem através do arquivo `Dockerfile` contido nele, então inicie o container do postgres em seu prórpio diretório por causa do `.env`. 
```bash
docker container run -dti --rm --name postgres --env-file .env -p 5432:5432 -v postgres_data:/var/lib/postgresql/data --network n8n postgres:16.1
```

### Redis
O redis servirá como um message broker ou intermediário e sua função será apenas receber e passar as informações do editor para os workers.
```bash
docker container run -dti --rm --name redis-n8n -p 6379:6379 -v redis_data:/data --network n8n redis:8.2-m01-alpine
```

### n8n editor
Iniciar o container do n8n diretório `editor` por causa arquivo `.env`
```bash
docker container run -dti --rm --name n8n-editor --env-file .env -p 5678:5678 -v n8n_data:/home/node/ --network n8n n8nio/n8n:latest
```
### Worker
Iniciar o container do n8n diretório `worker` por causa arquivo `.env`
```bash
docker container run -dti --rm --name n8n-worker-01  --env-file .env -v n8n_data:/home/node/ --network n8n n8nio/n8n:latest worker --concurrency=5
```

- Parar todos os containers em execução
```bash
docker stop $(docker ps -a -q)
```

## Quality of Life - QOF
Para melhorar as etapas de teste, quando todos os containers e serviços estiverem funcionando corretamente, foram criados no diretório raiz dois arquivos `.sh`, um para executar os containers `run_containers.sh` e outro com o intuito de parar os containers em execução `stop_containers.sh` que devem ser executados neste mesmo diretório raiz do n8n. Atente-se pois o script `stop_containers.sh` irá parar `TODOS OS CONTAINERS EM EXECUÇÃO`.
```bash
# Execução padrão
chmod +x run_containers.sh
chmod +x stop_containers.sh

./run_containers.sh
./stop_containers.sh

# Execução simples
bash run_containers.sh
bash stop_containers.sh
```
### QOF - .env
Na raiz do projeto existe um arquivo `.env` onde serão colocadas todas as variáveis de todos os serviços que serão executados e depois carregados através de outros scripts. 

### QOF - /utils
Neste diretório está o script python que irá carregar toda as variáveis do arquivo `.env` do diretório raiz e transmitir através de outros scripts em seus respectivos diretórios.

### QOF - scripts python
Em cada diretório irá conter um script python que será o `exportar_env.py` ele será responsáveel por obter as variáveis de ambiente e exportá-las em um arquivo `.env` naquele respectivo diretório. Configurá-los no inicio será trabalhoso, mas facilitará durante quando forem passadas através de alguma secret.

### QOF - exportar_env.py
Esse script faz a exportação das chaves e valores das variáveis armazenadas no script getenv.py para um arquivo `.env` local somente com aquelas que foram definidas dentro do dicionário `VARIAVIES_MAPEADAS`.

```bash
VARIAVEIS_MAPEADAS = {
    "POSTGRES_USER": "POSTGRES_USER",
    "POSTGRES_PASSWORD": "POSTGRES_PASSWORD",
    "POSTGRES_DB": "POSTGRES_DB",
    "POSTGRES_NON_ROOT_USER": "POSTGRES_NON_ROOT_USER",
    "POSTGRES_NON_ROOT_PASSWORD": "POSTGRES_NON_ROOT_PASSWORD"
}
```
### QOF - Como utilizar
```bash
# Etapa 1: Preencha as variáveis de ambiente no arquivo .env do diretório raiz

# Etapa 2: Preencha as variáveis de ambiente necessárias em cada arquivo exportar_env.py nos diretórios, caso queira adicionar outras de sua preferência, basta seguir o modelo já existente. Fora isso, elas já possuem as variáveis básicas nos scripts python.

# Etapa 3: Instalar o python, caso não o tenha instalado

# Etapa 4: Execute o 'pip install -r requirements.txt' caso não tenha o pacote dotenv instalado. Caso a sua versão do ubuntu seja maior ou igual a 23.04, utilize este comando `pip install --break-system-packages -r requirements.txt` 

# Etapa 5: Execute o script criar_env.sh que irá fazer o carregamento das variáveis de ambiente e a criação dos arquivos .env. Forma de executar: bash criar_env.sh

# Etapa 6: Verificar no script run_container.sh se as configurações dos containers estão de acordo com o que você criou como rede, volume, nome, porta e etc, incluindo os docker-compose.

# Etapa 7: Se estiver tudo ok, execute o script run_container.sh para subir todo o serviço. Forma de executar: bash run_container.sh
```

### Observações
- No script `run_containers.sh` os códigos de execução dos containers foram passados com o argumento `--rm`, porém se quiser que eles restartem qsempre que houver algum erro altere esse argumento para `--restart always`.

- Definir o consumo de memória e cpu de cada container.

