import os
from pathlib import Path
from dotenv import dotenv_values

# Mapeamento: VARIÁVEL_DESTINO = VARIÁVEL_ORIGEM
VARIAVEIS_MAPEADAS = {
    "POSTGRES_USER": "POSTGRES_USER",
    "POSTGRES_PASSWORD": "POSTGRES_PASSWORD",
    "POSTGRES_DB": "POSTGRES_DB",
    "POSTGRES_NON_ROOT_USER": "POSTGRES_NON_ROOT_USER",
    "POSTGRES_NON_ROOT_PASSWORD": "POSTGRES_NON_ROOT_PASSWORD"
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