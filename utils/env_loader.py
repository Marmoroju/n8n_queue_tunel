import os
from dotenv import load_dotenv
from pathlib import Path

def carregar_envs():
    """
    Carrega o .env da raiz do projeto e, se existir, o .env local do subdiretório atual.
    O .env local sobrescreve variáveis do global.
    """
    caminho_atual = Path(__file__).resolve()

    # Caminho para a raiz do projeto
    raiz_projeto = next((p for p in caminho_atual.parents if (p / '.env').exists()), None)
    if not raiz_projeto:
        raise FileNotFoundError("Arquivo .env da raiz não encontrado.")

    # Carrega o .env da raiz
    load_dotenv(dotenv_path=raiz_projeto / '.env', override=False)

    # Caminho para o .env local (no mesmo diretório do script que chamou)
    script_chamador = Path(os.getcwd())
    env_local = script_chamador / '.env'
    if env_local.exists():
        load_dotenv(dotenv_path=env_local, override=True)