import pandas as pd

from processador import preparar_bloco1, carregar_validar
from utils import COL_DATA, MAPEAMENTO_COLUNAS

# função para testar a variação com o trimestre anterior zerado
def test_variacao_com_base_zero():
    df = pd.DataFrame({
        COL_DATA: pd.to_datetime(['2026-08-15', '2026-09-15'])
    })

    # guardar o resultado da função
    resultado = preparar_bloco1(df)

    # comportamento atual
    assert resultado[5] == 0

# verifica colunas padrão para análise
def test_descarta_coluna_fora_da_lista(tmp_path):
    dados = {coluna: ['x'] for coluna in MAPEAMENTO_COLUNAS }
    dados['Nome do Paciente'] = ['Pessoa Ficticia']
    df = pd.DataFrame(dados)
    caminho = tmp_path/'notificacoes.xlsx'
    df.to_excel(caminho, index=False)
    resultado = carregar_validar(caminho)

    # confere se a coluna 'Nome do Paciente' consta nas colunas padronizadas
    assert 'Nome do Paciente' not in resultado.columns

    # confere se a lista de colunas esta como o padronizado
    assert list(resultado.columns) == list(MAPEAMENTO_COLUNAS)