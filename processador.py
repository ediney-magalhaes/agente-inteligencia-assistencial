#---------------------------------------------------
# Script que realiza a preparação dos dados
# Criado por: Ediney Magalhães
# Data: 20/04/2026
#---------------------------------------------------

import pandas as pd
from utils import (
    atualizacao_schema,
    texto_variacao,
    tem_investigacao,
    foi_tratada,
    check_tool,
    MAPEAMENTO_COLUNAS,
    COL_DATA,
    COL_CLASSIFICACAO,
    COL_STATUS,
    COL_PL,
    COL_ACR,
    COL_PAC,
    COL_CAT,
    COL_INCIDENTE,
    COL_TIPO_SETOR,
    COL_EFETIVO,
    COL_DESCRICAO,
    COL_TAXON,
    COL_SETOR,
    COL_GRAU,
    COL_OPCAO,
    COL_TURNO
)

# Carregar schema
def carregar_validar(df):
    try:
        df_corrigido, lista_ausentes = atualizacao_schema(df)
        if lista_ausentes:
            raise ValueError(f'Colunas ausentes: {lista_ausentes}')
        else:
            df_corrigido [COL_DATA]= pd.to_datetime(df_corrigido[COL_DATA], errors='coerce')
            return df_corrigido
    except Exception as e:
        print(f'Erro inesperado: {e}')

# Preparar dados - Bloco 1 (Quantidade notificações)
def preparar_bloco1(df):
    data_maxima = df[COL_DATA].max()
    ano_atual = data_maxima.year
    trimestre_atual = data_maxima.quarter

    # Ajuste de comparação quando for 1º trimestre
    if trimestre_atual == 1:
        trimestre_anterior = 4
        ano_anterior = ano_atual - 1
    else:
        trimestre_anterior = trimestre_atual - 1
        ano_anterior = ano_atual

    # Filtro do trimestre atual
    df_atual = df[(df[COL_DATA].dt.year == ano_atual) & (df[COL_DATA].dt.quarter == trimestre_atual)]

    # Filtro do trimestre anterior
    df_tri_anterior = df[(df[COL_DATA].dt.year == ano_anterior) & (df[COL_DATA].dt.quarter == trimestre_anterior)]

    # Filtro do ano anterior
    df_ano_anterior = df[(df[COL_DATA].dt.year == ano_atual - 1) & (df[COL_DATA].dt.quarter == trimestre_atual)]

    # Cálculo do total
    total_atual = len(df_atual)
    total_tri_anterior = len(df_tri_anterior)
    total_ano_anterior = len(df_ano_anterior)

    # Cálculo da variação
    var_tri = ((total_atual - total_tri_anterior) / total_tri_anterior * 100) if total_tri_anterior else 0
    var_ano = ((total_atual - total_ano_anterior) / total_ano_anterior * 100) if total_ano_anterior else 0

    return (total_atual,
            total_tri_anterior,
            total_ano_anterior,
            var_tri,
            var_ano,
            trimestre_atual,
            ano_atual,
            trimestre_anterior,
            ano_anterior
    )

# Preparar dados - Bloco 2 (Turnos notificações)
def preparar_bloco2(df_atual, df_anterior):
    qtde_atual = df_atual[COL_TURNO].value_counts()
    qtde_anterior = df_anterior[COL_TURNO].value_counts()

    # Criando tabela comparativa entre os trimestres
    tabela = pd.DataFrame({
        'Trimestre atual': qtde_atual,
        'Trimestre anterior': qtde_anterior
    }).fillna(0)

    # Coluna das variações
    denominador = tabela['Trimestre anterior'].replace(0, float('nan'))
    tabela['% variação'] = ((tabela['Trimestre atual'] - tabela['Trimestre anterior']) /  denominador * 100).fillna(0).round(1)

    return tabela