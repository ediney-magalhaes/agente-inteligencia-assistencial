import pandas as pd

from processador import preparar_bloco1
from utils import COL_DATA

# função para testar a variação com o trimestre anterior zerado
def test_variacao_com_base_zero():
    df = pd.DataFrame({
        COL_DATA: pd.to_datetime(['2026-08-15', '2026-09-15'])
    })

    # guardar o resultado da função
    resultado = preparar_bloco1(df)

    # comportamento atual
    assert resultado[5] == 0