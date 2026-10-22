import logging
import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# função de configuração do loggin
def configurar_logging():

    # caminho do arquivo de log vem do ambiente
    caminho_log = os.getenv('CAMINHO_LOG')
    manipuladores = [logging.StreamHandler()]

    if caminho_log:
        Path(caminho_log).parent.mkdir(parents=True, exist_ok=True)
        manipuladores.append(logging.FileHandler(caminho_log, encoding='utf-8'))

    # configuração
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=manipuladores
    )

