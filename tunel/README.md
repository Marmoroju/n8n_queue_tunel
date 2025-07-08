# Tunnel Cloudflared -> Localhost

Como eles trabalham juntos:
1. O túnel (cloudflared) é iniciado e fica escutando conexões da Cloudflare.

2. Quando alguém acessa https://abc.seudominio.online, a Cloudflare encaminha essa requisição para o túnel.

3. O cloudflared redireciona essa requisição para https://localhost:8443.

### Tunnel - Cloudflare - Docker
A partir da plataforma da Cloudflare:

1. No painel inicial, acesse o menu `Access` e inicie o `Zero Trust`
2. Selecione sua conta
3. Menu lateral `Redes` - `Tunnels`
4. Tela Túneis - Cloudflared - `Adicionar um túnel`
5. Selecione o tipo de túnel recomendado, crie um nome (opte em colocar o subdominio e o seu domínio, no meu caso ficaria `abc.seudominio.online`) e salva.
6. Tela de configurações. Escolha o Docker que ao ser escolhido irá gerar um código de execução do container junto a um token. Copie o token e cole-o no arquivo `cloudflare_token.txt`, crie este arquivo caso não o tenha.
7. Tela para Encaminhar o tráfego. Exemplo: `Nome do host = n8n` - `Domínio = seudominio.online` - `Path =  ` - `Service Type = HTTP` - `URL = nome_container:porta_interna_container`, exemplo `nginx:80`, pois o serviço que pretendo expor está em um container ao qual foi nomeado como nginx e sua porta interna é a 80.
8. No menu Nomes de hosts públicos, ao clicar irá aparecer uma janela lateral com o domínio público que será acessado ao ser vinculada a instância local.


## Protocol QUIC
O protocolo QUIC une o melhos dos dois mundos entre as transferências UDP e TCP.

Refere-se ao envio e recebimento de buffers durante o tunnel, normalmente gera esse erro `failed to sufficiently increase receive buffer size (was: 208 kiB, wanted: 7168 kiB, got: 416 kiB). See https://github.com/quic-go/quic-go/wiki/UDP-Buffer-Sizes for details.`ao subir o container do cloudflare, para corrigir deve ser executado esses dois comandos abaixo. 

```bash
sudo sysctl -w net.core.rmem_max=7500000

sudo sysctl -w net.core.wmem_max=7500000
```

### TESTE DO TÚNEL
Não é obrigatório passar a `/` no campo Caminho, mas somente a porta interna do container na URL e o nome do container `nginx:80`. Por exemplo, mesmo que o nginx esteja sendo passado com a porta externa 8443, dentro do túnel da Cloudflare, ele deve ser passado com sua porta interna `80`.

Dentro do diretório `tunel`, execute:
```bash
# Container Cloudflare Tunnel
docker run -d --rm --name cloudflare-tunnel --network n8n -v $(pwd)/cloudflare_token.txt:/etc/cloudflared/token.txt:ro  cloudflare/cloudflared:latest tunnel --no-autoupdate run --token-file /etc/cloudflared/token.txt

# Container nginx
docker container run -d --rm --name nginx -p 8443:80 --network n8n nginx:alpine
```
Agora acesse o navegador através do seu domínio.

O detalhe aqui é que o túnel foi executado como container `Docker` e o docker possui um `DNS interno` através do nome de cada container. O nome pode mudar direto na cloudflare pois a propagação do dns é dinâmica.

Outro exemplo, ao apontar o tunnel direto para o `webhook` a URL passada deve ser `webhook:5678`, exatamente com o nome dado ao container e sua porta interna durante o tempo de execução.
Se na URL alterar uma letra sequer, o retorno será `502 - Bad Gateway`