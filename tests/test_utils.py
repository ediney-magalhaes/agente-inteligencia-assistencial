import pandas as pd

from utils import formatar_variacao

def test_variacao_sem_base_vira_traco():
    tabela = pd.DataFrame({'% variação': [12.34, float('nan')]})
    resultado = formatar_variacao(tabela)
    assert resultado['% variação'].tolist() == ['12.3', '-']
    assert tabela['% variação'].tolist()[0] == 12.34