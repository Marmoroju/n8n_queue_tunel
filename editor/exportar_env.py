import os
from pathlib import Path
from dotenv import dotenv_values

# Mapeamento: VARIÁVEL_DESTINO = VARIÁVEL_ORIGEM
VARIAVEIS_MAPEADAS = {
    
     # Variáveis n8n postgresdb
     "DB_TYPE": "DB_TYPE",
     "DB_POSTGRESDB_HOST": "DB_POSTGRESDB_HOST",
     "DB_POSTGRESDB_PORT": "DB_POSTGRESDB_PORT",
     "DB_POSTGRESDB_DATABASE": "DB_POSTGRESDB_DATABASE",
     "DB_POSTGRESDB_USER": "DB_POSTGRESDB_USER",
     "DB_POSTGRESDB_PASSWORD": "DB_POSTGRESDB_PASSWORD",

     #Variáveis Timezone
     "GENERIC_TIMEZONE":"GENERIC_TIMEZONE",
     "TZ":"TZ",

     # Variáveis de autenticação
     "N8N_RUNNERS_ENABLED": "N8N_RUNNERS_ENABLED",
     "N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS": "N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS",
     "N8N_DISABLE_PRODUCTION_MAIN_PROCESS": "N8N_DISABLE_PRODUCTION_MAIN_PROCESS",

     #Variáveis queue - modo fila
     "EXECUTIONS_MODE": "EXECUTIONS_MODE",
     "N8N_ENCRYPTION_KEY": "N8N_ENCRYPTION_KEY",
     "QUEUE_BULL_REDIS_HOST":"QUEUE_BULL_REDIS_HOST",
     "QUEUE_BULL_REDIS_PORT": "QUEUE_BULL_REDIS_PORT",
     "OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS":"OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS", # utilizar somente em trigger manual (testes)

     # Variavel para o webhook 
     "N8N_PORT":"N8N_PORT",
     "N8N_PROTOCOL":"N8N_PROTOCOL",
     "WEBHOOK_URL":"WEBHOOK_URL"
}

CAMINHO_FIXO_ENV = "../.env"

def localizar_env_fixo(caminho=CAMINHO_FIXO_ENV) -> Path:
    """Retorna o caminho fixo do .env se ele existir."""
    arquivo = Path(caminho)
    if arquivo.exists():
        return arquivo
    else:
        print(f"Arquivo .env não encontrado em: {arquivo}")
        return None

def exportar_env(arquivo_saida=".env"):
    caminho_env = localizar_env_fixo()
    if not caminho_env:
        return

    print(f"Lendo variáveis de: {caminho_env}")
    variaveis = dotenv_values(caminho_env)

    if not variaveis:
        print("Nenhuma variável encontrada no .env.")
        return

    with open(arquivo_saida, "w") as f:
        for destino, origem in VARIAVEIS_MAPEADAS.items():
            valor = variaveis.get(origem)
            if valor is not None:
                f.write(f"{destino}={valor}\n")
                print(f"{destino} = {valor}")
            else:
                f.write(f"{destino}=\n")
                print(f"{destino} não encontrado (origem: {origem})")

    print(f"\nArquivo exportado com sucesso: {arquivo_saida}")

if __name__ == "__main__":
    exportar_env()
