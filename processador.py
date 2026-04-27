#---------------------------------------------------
# Script que realiza a preparação dos dados
# Criado por: Ediney Magalhães
# Data: 20/04/2026
#---------------------------------------------------

import pandas as pd
import numpy as np
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
    COL_TURNO,
    COL_LOCAL,
    COL_NOTA
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

    # Contagem das notificações mês a mês
    qtde_mensal = df.groupby([df[COL_DATA].dt.year, df[COL_DATA].dt.month]).size()

    # Contagem das notificações por trimestre
    qtde_trimestral = df.groupby([df[COL_DATA].dt.year, df[COL_DATA].dt.quarter]).size()

    return (total_atual,
            total_tri_anterior,
            total_ano_anterior,
            qtde_mensal,
            qtde_trimestral,
            var_tri,
            var_ano,
            trimestre_atual,
            ano_atual,
            trimestre_anterior,
            ano_anterior,
            df_atual,
            df_tri_anterior
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

    # Dataframe com contexto para leitura da IA
    colunas_necessarias = [COL_TURNO, COL_CLASSIFICACAO, COL_DESCRICAO]
    df_contexto_ia = df_atual[colunas_necessarias]

    return tabela, df_contexto_ia

# Preparar dados - Bloco 3 (Classificação notificações)
def preparar_bloco3(df_atual, df_anterior):
    qtde_atual = df_atual[COL_CLASSIFICACAO].value_counts()
    qtde_anterior = df_anterior[COL_CLASSIFICACAO].value_counts()

    # Criando tabela comparativa
    tabela_comparativa = pd.DataFrame({
        'Trimestre atual': qtde_atual,
        'Trimestre anterior':qtde_anterior
    }).fillna(0)

    # Variações
    denominador = tabela_comparativa['Trimestre anterior'].replace(0, float('nan'))
    tabela_comparativa['% variação'] = ((tabela_comparativa['Trimestre atual'] - tabela_comparativa['Trimestre anterior']) / denominador * 100).fillna(0).round(1)

    # Dicionário top 3
    dicionario = {}

    # Montando tabela com top 3 das classificações
    for classificacao in df_atual[COL_CLASSIFICACAO].unique():

        # Cria filtro onde a coluna de classificação é verificada com a variável classificação do for
        df_filtrado = df_atual[df_atual[COL_CLASSIFICACAO] == classificacao]
        
        # Seleciona a coluna de Opção, faz a contagem de cada valor único e seleciona os 3 mais frequentes
        contagem = df_filtrado[COL_OPCAO].value_counts().head(3)
        
        # Seleciona a coluna de Opção, faz o cálculo do percentual
        percentual = (df_filtrado[COL_OPCAO].value_counts(normalize=True).head(3) * 100).round(1)

        # Criando Data Frame
        tabela = pd.DataFrame({'Frequência': contagem, 'Percentual': percentual})
        
        # Adiciona ao dicionário vazio cada classificação com sua tabela de frequência absoluta e relativa
        dicionario[classificacao] = tabela

    # DataFrame de contexto para IA
    colunas_necessarias = [COL_CLASSIFICACAO, COL_TURNO, COL_SETOR, COL_GRAU, COL_DESCRICAO]
    df_contexto_ia = df_atual[colunas_necessarias]

    return tabela_comparativa, dicionario, df_contexto_ia

# Preparar dados - Bloco 4 (Eventos Adversos Notificados)
def preparar_bloco4(df_atual, df_anterior):
    
    # Filtrar apenas Eventos Adversos
    df_eventos_adversos = df_atual[(df_atual[COL_CLASSIFICACAO] == 'Evento adverso')]
    df_eventos_adversos_tri_anterior = df_anterior[(df_anterior[COL_CLASSIFICACAO] == 'Evento adverso')]

    # Top 3 dos eventos adversos
    top3_eventos = df_eventos_adversos[COL_OPCAO].value_counts().head(3)

    # Percentual top 3 eventos adversos
    percentual_top3_eventos = (df_eventos_adversos[COL_OPCAO].value_counts(normalize=True).head(3) * 100).round(1)

    # Tabela de frequência absoluta e relativa do top 3
    tabela_top3_eventos = pd.DataFrame({'Frequência': top3_eventos, 'Percentual': percentual_top3_eventos})

    # Quantidade de eventos adversos
    qtde_eventos_tri_atual = df_eventos_adversos[COL_GRAU].value_counts()
    qtde_eventos_tri_anterior = df_eventos_adversos_tri_anterior[COL_GRAU].value_counts()

    # Criando tabela para comparação entre trimestres
    tabela_comparativa = pd.DataFrame({'Trimestre atual': qtde_eventos_tri_atual,
                                       'Trimestre anterior': qtde_eventos_tri_anterior}).fillna(0)
    
    # Cálculo da variação
    denominador = tabela_comparativa['Trimestre anterior'].replace(0, float('nan'))
    calculo_normal = ((tabela_comparativa['Trimestre atual'] - tabela_comparativa['Trimestre anterior']) / denominador * 100).round(1)
    tabela_comparativa['% variação'] = np.where(tabela_comparativa['Trimestre anterior'] == 0, '-', calculo_normal)

    # Filtrando o status das notificações 'Grave' e 'Óbito'
    status_eventos = df_eventos_adversos[df_eventos_adversos[COL_GRAU].isin(['Óbito', 'Grave'])][[COL_DESCRICAO, COL_GRAU, COL_STATUS]]

    # DataFrame Contexto para IA
    colunas_necessarias = [COL_TURNO, COL_SETOR, COL_GRAU, COL_OPCAO, COL_DESCRICAO]
    df_contexto_ia = df_eventos_adversos[colunas_necessarias]

    return tabela_comparativa, tabela_top3_eventos, status_eventos, df_contexto_ia

# Função para os blocos 5 e 6 do relatório
def preparar_bloco_setores(df_atual, df_anterior, coluna):
    # Top 3
    qtde_tri_atual = df_atual[coluna].value_counts().head(3)
    qtde_tri_anterior = df_anterior[coluna].value_counts().head(3)

    # Tabelas
    tab_tri_atual = pd.DataFrame({'Trimestre atual': qtde_tri_atual})
    tab_tri_anterior = pd.DataFrame({'Trimestre anterior': qtde_tri_anterior})

    # Variação
    tab_tri_atual['(%)'] = (df_atual[coluna].value_counts(normalize=True).head(3) * 100).round(1)
    tab_tri_anterior['(%)'] = (df_anterior[coluna].value_counts(normalize=True).head(3) * 100).round(1)

    # Tabela descrições
    tab_analise_IA = df_atual[df_atual[coluna].isin(qtde_tri_atual.index)][[coluna, COL_DESCRICAO]]

    return tab_tri_atual, tab_tri_anterior, tab_analise_IA

# Função para o bloco 7 (Indicadores de qualidade)
def preparar_bloco7(df_atual, df_indicadores, indicador, trim_atual, ano_atual):
    # Dicionário trimestre
    trimestres = {1: ['Janeiro', 'Fevereiro','Março'],
                  2: ['Abril', 'Maio', 'Junho'],
                  3: ['Julho', 'Agosto', 'Setembro'],
                  4: ['Outubro', 'Novembro', 'Dezembro']}
    
    # Lista meses do trimestre atual
    trimestre_atual = trimestres[trim_atual]

    # Filtro do trimestre
    df_tri_atual = df_indicadores[(df_indicadores['Ano'] == ano_atual) & (df_indicadores['Mês'].isin(trimestre_atual))]
    df_tri_anterior = df_indicadores[(df_indicadores['Ano'] == ano_atual - 1) & (df_indicadores['Mês'].isin(trimestre_atual))]

    # Filtro do período e indicador
    df_ano_atual = df_indicadores[df_indicadores['Ano'] == ano_atual][[indicador, 'Mês']].round(2)
    df_ano_anterior = df_indicadores[df_indicadores['Ano'] == ano_atual - 1][[indicador, 'Mês']].round(2)

    # Cálculo da média nos trimestres
    df_media_tri_atual = df_tri_atual[indicador].mean().round(2)
    df_media_tri_anterior = df_tri_anterior[indicador].mean().round(2)

    return df_ano_atual, df_ano_anterior, df_media_tri_atual, df_media_tri_anterior

# Função para indicador de Queda
def preparar_detalhe_queda(df_atual):
    
    # Filtra a coluna de incidente que contém a palavra queda
    df_quedas = df_atual[df_atual[COL_INCIDENTE].str.contains('queda', case=False, na=False)]

    # Quantidades
    qtde_grau_dano = df_quedas[COL_GRAU].value_counts()
    qtde_tipo_queda = df_quedas[COL_OPCAO].value_counts()
    qtde_local_queda = df_quedas[COL_LOCAL].value_counts()

    return qtde_grau_dano, qtde_local_queda, qtde_tipo_queda

# Função que prepara dataset para IA filtrar possíveis erro de medicação, flebite e outros casos semelhantes
def preparar_dataset_ia(df_atual):
    colunas_necessarias = [COL_TAXON,
                           COL_CAT,
                           COL_CLASSIFICACAO,
                           COL_INCIDENTE,
                           COL_OPCAO,
                           COL_DESCRICAO]
    df_indicador = df_atual[colunas_necessarias]
    return df_indicador

# Função para preparar dataset para IA filtrar as lesões admitidas e adquiridas
def preparar_dataset_ia_LPP(df_atual):

    colunas_necessarias = [COL_TAXON,
                           COL_CAT,
                           COL_CLASSIFICACAO,
                           COL_INCIDENTE,
                           COL_OPCAO,
                           COL_DESCRICAO,
                           COL_NOTA]
    # Filtra a coluna de incidentes
    df_filtrado = df_atual[(df_atual[COL_CAT] == 'Lesões da pele e partes moles')]

    # Monta dataset apenas com as colunas necessárias
    df_indicador = df_filtrado[colunas_necessarias]
    return df_indicador

# Função para cumprimento da análise das notificações
def preparar_bloco8(df_atual): # parâmetro precisa ser dataframe completo sem filtro
    noti_elegiveis = [COL_PL, COL_ACR, COL_PAC]
    
    # Filtro de notificações elegível a tratativa
    df_elegiveis = df_atual[(df_atual[noti_elegiveis].notna().any(axis=1))]

    # Filtro onde as elegíveis foram tratadas
    df_tratadas = df_elegiveis[(df_elegiveis[COL_STATUS].isin(['Validado', 'Concluído após a investigação']))]

    # Quantidade elegíveis
    qtde_elegiveis = df_elegiveis.groupby(df_elegiveis[COL_DATA].dt.year).size()

    # Quantidade tratadas
    qtde_tratadas = df_tratadas.groupby(df_tratadas[COL_DATA].dt.year).size()

    # Taxa anual
    taxa_anual = (qtde_tratadas / qtde_elegiveis * 100.0).round(1)

    tabela_anual = pd.DataFrame({
        'Nº notificações para responder': qtde_elegiveis,
        'Nº notificações respondidas': qtde_tratadas,
        'Taxa de cumprimento': taxa_anual
    })

    # Encontrando o ano atual
    ano_recente = df_elegiveis[COL_DATA].max().year

    # Filtrando pelo ano atual
    df_elegiveis_ano_atual = df_elegiveis[(df_elegiveis[COL_DATA].dt.year == ano_recente)]
    df_tratadas_ano_atual = df_tratadas[(df_tratadas[COL_DATA].dt.year == ano_recente)]

    # Agrupando pelo mês
    qtde_elegiveis_mensal = df_elegiveis_ano_atual.groupby(df_elegiveis_ano_atual[COL_DATA].dt.month).size()
    qtde_tratadas_mensal = df_tratadas_ano_atual.groupby(df_tratadas_ano_atual[COL_DATA].dt.month).size()

    # Cálculo da taxa de cumprimento mensal
    taxa_mensal = (qtde_tratadas_mensal / qtde_elegiveis_mensal * 100.0).round(1)

    # Tabela da taxa de cumprimento mensal

    tabela_mensal = pd.DataFrame({
        'Nº notificações para responder': qtde_elegiveis_mensal,
        'Nº notificações respondidas': qtde_tratadas_mensal,
        'Taxa de cumprimento': taxa_mensal
    })

    return tabela_anual, tabela_mensal