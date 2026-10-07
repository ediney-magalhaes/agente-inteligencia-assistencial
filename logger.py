import logging

from pathlib import Path

# função de configuração do loggin
def configurar_logging():

    # caminho para o pasta logs
    Path('log').mkdir(exist_ok=True)

    # configuração
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[logging.FileHandler("log/relatorio.log"), logging.StreamHandler()]
    )

