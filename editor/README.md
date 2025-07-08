# Editor

O n8n Editor é o componente responsável por fornecer a interface gráfica de criação, edição e gerenciamento de workflows. Ele não executa workflows nem escuta webhooks — essas funções são delegadas a serviços especializados (Worker e Webhook).

Segurança e Benefícios
- Reduz a superfície de ataque: o Editor não precisa estar exposto à internet.
- Ele será executado localmente.
- Permite escalabilidade horizontal: múltiplos Workers e Webhooks podem ser adicionados conforme a carga.
- Facilita o controle de acesso: o Editor pode ser acessado apenas por administradores ou desenvolvedores.
- O Editor apenas registra os webhooks no banco de dados e os Workers executam os fluxos


Dentro do arquivo `exportar_env.py` neste mesmo diretório a variável de ambiente `N8N_DISABLE_PRODUCTION_MAIN_PROCESS`está descomentada, comente-a caso queira testar o editor executando por si mesmo a função de webhook caso este ainda não tenha sido configurado.

Inicia o container do editor
```bash
docker container run -dti --rm --name n8n-editor --env-file .env -p 5678:5678 -v n8n_data:/home/node/ --network n8n n8nio/n8n:latest
```


