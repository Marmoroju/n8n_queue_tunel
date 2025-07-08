# Webhook

## Por que Webhooks são Essenciais:
- Disparo de Workflows: Muitos workflows no n8n são iniciados por eventos externos. Webhooks são o método padrão para que sistemas externos (como um CRM, um formulário web, um sistema de e-commerce, ou outro serviço de API) notifiquem o n8n sobre um evento, disparando um workflow específico.

- Integração com Serviços Externos: Para o n8n receber dados de serviços SaaS ou outros sistemas que não oferecem APIs específicas para polling (verificação constante de novos dados), os webhooks são a solução mais eficiente e em tempo real.

- Callbacks e Retornos: Em cenários onde o n8n precisa ser notificado sobre o status de uma operação iniciada por ele em um sistema externo (por exemplo, após enviar um email, um webhook pode ser usado para confirmar a entrega), os webhooks são usados para callbacks.

- APIs Personalizadas: O n8n permite criar seus próprios "endpoints" de webhook, transformando-o em um construtor de API leve para tarefas específicas, como receber dados de sensores, formulários ou outros aplicativos personalizados.

- A ideia de criar um container separado exclusivamente para gerenciar webhooks do n8n, em vez de o próprio n8n-editor lidar com eles diretamente e ser exposto publicamente, é uma excelente prática de segurança e arquitetura em ambientes de produção. Embora o n8n permita que o editor sirva como endpoint de webhook por padrão, isolar essa função traz benefícios significativos.

## Abordagem Padrão (n8n-editor como Webhook)

Como funciona:
Por padrão, o n8n-editor é o serviço que escuta as requisições de webhook. Quando um webhook é recebido, o editor processa o evento e o envia para a fila (Redis) para ser pego por um n8n-worker.

## Abordagem com Container Dedicado para Webhooks (Gateway de Webhooks)

A forma de implementar isso seria ter um n8n-worker configurado especificamente para atuar como um "gateway" de webhooks. Este worker seria o único componente do n8n exposto publicamente para receber requisições de webhook.

Como funciona:

- `Configuração:` Você iniciaria um n8n-worker adicional (ou um grupo deles) e configuraria o WEBHOOK_URL do n8n para apontar para este novo container (ou seu proxy).

- `Exposição Pública:` Apenas este worker de webhook seria exposto à internet (via um proxy reverso com HTTPS).

- `Processamento:` Quando uma requisição de webhook chega a este worker dedicado, ele a processa minimamente e a envia para a fila (Redis).

- `Execução:` Outros n8n-workers (ou o editor, se configurado para isso em ambientes menores) pegariam o evento da fila e executariam o workflow correspondente.


### Como implementar (exemplo simplificado de comando):

Você iniciaria o n8n-editor e os workers de execução como antes, mas com uma pequena diferença na configuração do editor e a adição de um worker dedicado a webhooks:

n8n-editor:

Mantenha a porta `5678` exposta para acesso interno da UI (ou via um proxy interno).
Importante: O WEBHOOK_URL apontaria para o endereço público do novo container de webhook.

### Observações para o worker de webhook:

A porta `-p` deve ser configurada para ser acessível externamente (geralmente via um proxy reverso na porta 80/443).
`-p 8443:5678` por exemplo.

O comando n8n worker indica que ele é um worker comum, mas sua função específica será definida pela forma como o WEBHOOK_URL é configurado no editor e como ele é exposto.

Ao configurar o `WEBHOOK_URL` no n8n-editor para apontar para o endereço público deste n8n_webhook_worker, você garante que todas as URLs de webhook geradas pelo n8n apontarão para o gateway seguro, mantendo o editor isolado.

### Container
```bash
docker container run -dti --rm --name webhook --env-file .env -p 8443:5678 -v n8n_data:/home/node/ --network n8n n8nio/n8n:latest webhook
```

## Configuração do webhook no túnel da cloudflare
Assim como configurado no diretório `tunel` com o nginx, a URL para acessar o webhook deve serguir o mesmo padrão com a URL definida com o nome do container apontado pelo túnel e a porta interna, algo assim `webhook:5678`

## Método POST - Teste do webhook (sem let's encrypt)
Através do site `https://reqbin.com/post-online` é possível testar as requisições do `webhook` da seguinte maneira.

1. Acessar o editor n8n
2. Criar um trigger do tipo `webhook`
3. Definir o `HTTP Method` como POST
4. Altere o nome do `Path` para teste (pode ser outro nome)
5. Copie o link da URL de produção
5. Ative o workflow para funcionar o link de produção automaticamente sem ser preciso a execução manual
6. Acesse o site do reqbin e cole o link da URL
7. Em `Query Params` inclua uma chave:valor, por exemplo, Key:Nome Value: Seu nome
8. Faça o envio e espere o retorno com o código 200.
9. Retorne ao n8n editor e confira se houve a execução
10. Acesse o log do container do webhook. Caso queira, confira também do editor e worker.



## Webhook com let's encrypt
Na cloudflare, a URL permanece com o nome `traefik:443` com HTTPS.

Após testar o passo `4 - Tunel Cloudflare + Traefik + Nginx + Let's Encrypt`, suba todos os serviços relacionado ao n8n e então execute o docker-compose e repita o teste do método POST acima.



