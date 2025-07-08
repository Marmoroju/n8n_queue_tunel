# Traefik + Cloudflare

A ideia de usar Cloudflare e Traefik para gerenciar o tráfego de webhooks, mesmo em uma rede "interna", é uma excelente estratégia que adiciona camadas robustas de segurança, performance e gerenciamento, que vão muito além do que uma configuração interna básica poderia oferecer.

### Cloudflare
O Cloudflare pode ser incrivelmente benéfico, especialmente se seus webhooks precisam ser acessíveis por serviços externos que não estão na sua rede privada (por exemplo, APIs de terceiros, CRMs online, sistemas de pagamento).

Pontos Positivos:

- `Proteção DDoS:` A Cloudflare oferece proteção robusta contra ataques de negação de serviço distribuídos (DDoS) no nível da rede. Isso é crucial, pois um ataque a um webhook pode facilmente sobrecarregar seu servidor e interromper seus fluxos de trabalho.

- `Firewall de Aplicação Web (WAF):` O WAF da Cloudflare ajuda a proteger seus endpoints de webhook contra vulnerabilidades comuns da web, como injeção de SQL e cross-site scripting (XSS), filtrando tráfego malicioso antes que ele chegue ao seu servidor.

- `Edge Caching (Opcional, mas Útil):` Embora webhooks geralmente não sejam armazenáveis em cache, o Cloudflare pode gerenciar o cache de outros ativos estáticos (se você tiver algum no mesmo domínio), e a simples presença na borda da Cloudflare pode otimizar a rota do tráfego.

- `Gerenciamento de DNS:` A Cloudflare atua como seu provedor de DNS, oferecendo resoluções rápidas e recursos avançados de DNS.

- `HTTPS Gratuito (SSL/TLS):` A Cloudflare oferece certificados SSL/TLS gratuitos e gerenciamento automático, garantindo que todo o tráfego para seus webhooks seja criptografado por padrão. Isso é absolutamente essencial para a segurança em produção.

- `Ocultação de IP de Origem:` Seu servidor de origem (onde o Traefik e o n8n estão rodando) tem seu endereço IP oculto por trás dos IPs da Cloudflare. Isso dificulta que agentes mal-intencionados ataquem diretamente seu servidor.

- `Controle de Acesso (Zero Trust):` Com recursos como Cloudflare Access (parte da suíte Zero Trust), você pode implementar políticas de acesso rigorosas para seus webhooks, permitindo o acesso apenas de IPs específicos ou exigindo autenticação para certos endpoints, mesmo que os considere "internos" mas acessíveis de fora.

### Traefik
O Traefik é um proxy reverso moderno e balanceador de carga que se integra muito bem com Docker, sendo ideal para o seu cenário. Apontá-lo especificamente para o container de webhook é a maneira mais eficiente de gerenciá-lo.

Pontos Positivos:

- `Descoberta Automática de Serviços (Service Discovery):` O Traefik pode monitorar o Docker (e outros orquestradores) e descobrir automaticamente seus containers n8n-webhook-worker. Isso significa que você não precisa configurar manualmente cada novo worker de webhook que você escalar.

- `Balanceamento de Carga:` Se você decidir ter múltiplas instâncias do seu n8n_webhook_worker para alta disponibilidade ou escalabilidade, o Traefik irá distribuir automaticamente o tráfego entre elas.

- `Gerenciamento de SSL/TLS:` O Traefik pode gerenciar automaticamente certificados SSL/TLS (via Let's Encrypt, por exemplo) para seus domínios, facilitando a implementação de HTTPS para seus webhooks. Isso complementa ou até substitui o SSL da Cloudflare na borda (no caso de "Full" ou "Strict" SSL da Cloudflare).

- `Configuração Dinâmica:` Com base nas labels que você adiciona aos seus containers Docker, o Traefik se configura dinamicamente. Isso é extremamente poderoso para gerenciar rotas de tráfego, reescritas de URL e middleware.

- `Middleware:` O Traefik permite a adição de middlewares para funções como autenticação, rate limiting, compressão e reescrita de cabeçalhos, adicionando camadas de segurança e otimização antes que as requisições cheguem ao n8n.

- `Painel de Controle:` Oferece um painel web que permite visualizar o status dos seus roteadores, serviços e middlewares.

### Conclusão e Recomendação

A combinação de Cloudflare e Traefik apontando para um worker n8n dedicado a webhooks é uma arquitetura altamente recomendada e robusta para um ambiente de produção, mesmo em uma "rede interna" que precisa de qualquer exposição externa.

Cloudflare fornece a primeira linha de defesa, segurança na borda (DDoS, WAF, HTTPS), e ocultação de IP.
Traefik age como o orquestrador de tráfego inteligente dentro da sua rede, gerenciando o balanceamento de carga, a descoberta de serviços e o SSL/TLS, encaminhando o tráfego de forma eficiente e segura para os workers de webhook.
Benefícios combinados:

- Segurança Máxima: Múltiplas camadas de proteção para seus endpoints de webhook.

- Alta Disponibilidade e Escalabilidade: Facilita o balanceamento de carga e a escalabilidade dos workers de webhook.

- Gerenciamento Simplificado: Automação de descoberta de serviços e gerenciamento de SSL/TLS.

- Performance Otimizada: Tráfego roteado eficientemente e com potencial de cache de borda (se aplicável)


### Traefik - Container
Antes das variáveis de ambiente será necessário criar os volumes para armazenar as configurações, logs e certificados.
```bash
mkdir -p traefik/logs
mkdir -p traefik/config

# Dentro do diretório traefik/logs
touch traefik.log

# Dentro do diretório traefik/config
touch acme.json
sudo chmod 600 acme.json # para rescrever o Let's Encrypt
```
Para gerar o token para o certificado com o `let's encrypt` será necessário acessar o painel da Cloudflare, seu perfil, Tokens de API e criar um token que será passado na variável de ambiente `CF_DNS_API_TOKEN`. Adicione seu token na variável de ambiente neste mesmo diretório.

Configuração necessária do Token de API
```bash
# Permissões
# Zona - Zona - Lido
# Zona- DNS - Editar

# Recursos de Zona
# Incluir - Zona específica - seu_domínio
```

### Como funciona?

Docker: A porta que será exposta deverá ser exposta através do container do traefik e roteada através do `label` no container desejado.

Cloudflare: a URL do túnel deve apontar para o traefik. Diferente do que foi testado no webhook, aqui será apontado para o traefik pois será ele que receberá as requisições e apontará para o webhook através dos `routers`, como demonstrado no docker-compose abaixo feito com o nginx. E da mesma forma, caso na URL seja alterado para um nome diferente do container do traefik você receberá o erro 502 - Bad Gateway.
```bash
services:
  traefik:
    image: traefik:v3.1.5
    container_name: traefik
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Traefik dashboard
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./config/traefik.yml:/etc/traefik/traefik.yml"
    restart: unless-stopped
    networks:
      - n8n
  
  nginx:
    image: nginx:latest
    container_name: nginx
    labels:
      # HTTP PROTOCOL
      - "traefik.enable=true" 
      - "traefik.http.routers.nginx.rule=Host(`seudominio.online`)" 
      - "traefik.http.routers.nginx.entrypoints=web"
    restart: unless-stopped
    networks:
      - n8n

networks:
  n8n:
    external: true
```

Arquivo traefik.yml, exemplo:
```bash
global:
  checkNewVersion: false  
  sendAnonymousUsage: false

log:
  level: DEBUG
  filePath: /var/log/traefik.log

api:
  dashboard: true 
  insecure: true

entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
```

### Let's Encrypt
Quando for adicionar o `certificado`, atentar-se em alterar a configuração de serviço na Cloudflare de `HTTP -> HTTPS` e URL de `traefik:80 -> traefik:443`

Caso apresente falhas de `ERR_TOO_MANY_REDIRECTS`, tente abrir em um outro navegador, janela anônima, limpar cookies, flushdns.

docker-compose.yml (básico) com let's encrypt:
```bash
---
services:
  traefik:
    image: traefik:v3.1.5
    container_name: traefik
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Traefik dashboard
    environment:
      - CF_DNS_API_TOKEN={CF_DNS_API_TOKEN}
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "./config/traefik.yml:/etc/traefik/traefik.yml:ro"
      - "./config/acme.json:/acme.json:rw"
    restart: unless-stopped
    networks:
      - n8n
  
  nginx:
    image: nginx:latest
    container_name: nginx
    labels:
      - "traefik.enable=true" 

      # HTTPS PROTOCOL - let's encrypt
      - "traefik.http.routers.nginx-https.tls=true"
      - "traefik.http.routers.nginx-https.tls.certresolver=cloudflare"
      - "traefik.http.routers.nginx-https.entrypoints=websecure"
      - "traefik.http.routers.nginx-https.rule=Host(`seudominio.online`)" 

    restart: unless-stopped
    networks:
      - n8n

networks:
  n8n:
    external: true
```

Arquivo traefik.yml, exemplo:
```bash
global:
  checkNewVersion: false  
  sendAnonymousUsage: false

log:
  level: DEBUG
  filePath: /var/log/traefik.log

api:
  dashboard: true 
  insecure: true

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
          permanent: true
  websecure:
    address: ":443"

certificatesResolvers:
  cloudflare:
    acme:
      email: "seuemail@email.com"
      storage: "/acme.json"
      caServer: "https://acme-v02.api.letsencrypt.org/directory"
      KeyType: "EC256"
      dnsChallenge:
        provider: cloudflare
        resolvers:
          - "1.1.1.1:53"
          - "8.8.8.8:53"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
```

# MIDDLEWARE

[Doc Basic Auth](https://doc.traefik.io/traefik/middlewares/http/basicauth/)

Basicauth:
```bash
# install
sudo apt-get install apache2-utils -y

# Gerar hash
htpasswd -nb dash "Senha123" | sed -e 's/\$/\$\$/g'
```

Caso seja necessário incluir mais de um usuário, rode o gerador de hash para cada um com nome de usuário e sua senha, depois adicione ao final da label separando-os por `vírgula`, como no exemplo abaixo.
```bash
- "traefik.http.middlewares.auth.basicauth.users=hash-01,hash-02,hash-n"
```