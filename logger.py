import logging

from pathlib import Path

# guardar resultado
logger = logging.getLogger(__name__)

# caminho para o pasta logs
Path('log').mkdir(exist_ok=True)

# configuração
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[logging.FileHandler("log/relatorio.log"), logging.StreamHandler()]
)

logger.info("teste")
