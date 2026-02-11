#import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import google.generativeai as genai

# Funções
# ==========================================
# AS FUNÇÕES DO AGENTE (O "Cérebro")
# ==========================================

# --- BLOCO 1 ---
def analisar_bloco_1(df):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    data_maxima = df['Data da notificação'].max()
    ano_atual, tri_atual = data_maxima.year, data_maxima.quarter
    ano_ano_anterior, tri_ano_anterior = ano_atual - 1, tri_atual
    
    if tri_atual == 1: tri_tri_anterior, ano_tri_anterior = 4, ano_atual - 1
    else: tri_tri_anterior, ano_tri_anterior = tri_atual - 1, ano_atual
        
    df_atual = df[(df['Data da notificação'].dt.year == ano_atual) & (df['Data da notificação'].dt.quarter == tri_atual)]
    df_tri_anterior = df[(df['Data da notificação'].dt.year == ano_tri_anterior) & (df['Data da notificação'].dt.quarter == tri_tri_anterior)]
    df_ano_anterior = df[(df['Data da notificação'].dt.year == ano_ano_anterior) & (df['Data da notificação'].dt.quarter == tri_ano_anterior)]

    total_atual, total_tri_anterior, total_ano_anterior = len(df_atual), len(df_tri_anterior), len(df_ano_anterior)
    var_tri = ((total_atual - total_tri_anterior) / total_tri_anterior * 100) if total_tri_anterior > 0 else 0
    var_ano = ((total_atual - total_ano_anterior) / total_ano_anterior * 100) if total_ano_anterior > 0 else 0

    def texto_variacao(valor):
        if valor > 0: return f"um aumento de {valor:.1f}%"
        elif valor < 0: return f"uma redução de {abs(valor):.1f}%" 
        else: return "uma estabilidade"

    return f"""**RELATÓRIO DE SEGURANÇA - {tri_atual}º TRIMESTRE {ano_atual}**\n\nDurante o período, o Núcleo de Segurança do Paciente documentou um total de **{total_atual}** notificações.\n\nIsso representa {texto_variacao(var_tri)} em relação ao {tri_tri_anterior}º trimestre de {ano_tri_anterior} ({total_tri_anterior} notificações). Quando comparado ao mesmo período do ano anterior ({total_ano_anterior} notificações no {tri_ano_anterior}º Tri {ano_ano_anterior}), o cenário configura {texto_variacao(var_ano)}."""

# --- BLOCO 2 ---
def gerar_grafico_bloco_2(df):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    data_maxima = df['Data da notificação'].max()
    ano_atual, tri_atual = data_maxima.year, data_maxima.quarter
    anos_presentes = sorted(df['Data da notificação'].dt.year.unique())
    anos_analise = anos_presentes[-5:] if len(anos_presentes) >= 5 else anos_presentes
    ano_inicial = anos_analise[0]

    cores = ['#A6A6A6', '#5B9BD5', '#264478', '#707070', '#002060']
    cores_personalizadas = {ano: cores[i] if i < len(cores) else '#333333' for i, ano in enumerate(anos_analise)}
    meses_por_trimestre = {1: [1,2,3], 2: [4,5,6], 3: [7,8,9], 4: [10,11,12]}
    nomes_meses = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
    
    df_filtrado = df[df['Data da notificação'].dt.year.isin(anos_analise)]
    partes_do_grafico = []

    for mes_num in meses_por_trimestre[tri_atual]:
        filtro = df_filtrado[df_filtrado['Data da notificação'].dt.month == mes_num]
        df_temp = pd.DataFrame(filtro.groupby(filtro['Data da notificação'].dt.year).size()).T
        df_temp.index = [nomes_meses[mes_num]]
        partes_do_grafico.append(df_temp)

    def_tri = {'1º Trimestre': [1,2,3], '2º Trimestre': [4,5,6], '3º Trimestre': [7,8,9], '4º Trimestre': [10,11,12]}
    for nome_tri, lista_meses in def_tri.items():
        filtro = df_filtrado[df_filtrado['Data da notificação'].dt.month.isin(lista_meses)]
        df_temp = pd.DataFrame(filtro.groupby(filtro['Data da notificação'].dt.year).size()).T
        df_temp.index = [nome_tri]
        partes_do_grafico.append(df_temp)

    tabela_final = pd.concat(partes_do_grafico).fillna(0)
    fig, ax = plt.subplots(figsize=(14, 6))
    lista_cores = [cores_personalizadas.get(ano, '#333333') for ano in tabela_final.columns]

    tabela_final.plot(kind='bar', ax=ax, width=0.85, color=lista_cores, zorder=3)
    ax.set_title(f'Número de notificações realizadas\nHospital Santa Rosa, comparativo {ano_inicial} a {ano_atual}', fontsize=16, fontweight='bold', pad=40)
    ax.set_xlabel('')
    ax.grid(axis='y', linestyle='-', alpha=0.3, color='lightgrey', zorder=0)
    ax.tick_params(axis='x', rotation=0)
    ax.legend(title='', frameon=False, loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=len(anos_analise))

    for container in ax.containers: ax.bar_label(container, padding=3, fmt='%d', fontsize=9, fontweight='bold')
    for spine in ['top', 'right', 'left']: ax.spines[spine].set_visible(False)
    fig.tight_layout()
    return fig

# --- BLOCO 3 ---
def gerar_grafico_bloco_3(df):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    data_maxima = df['Data da notificação'].max()
    ano_atual, tri_atual = data_maxima.year, data_maxima.quarter
    anos_presentes = sorted(df['Data da notificação'].dt.year.unique())
    anos_analise = anos_presentes[-5:] if len(anos_presentes) >= 5 else anos_presentes
    cores = ['#A6A6A6', '#5B9BD5', '#264478', '#707070', '#002060']
    cores_personalizadas = {ano: cores[i] if i < len(cores) else '#333333' for i, ano in enumerate(anos_analise)}
    meses_por_trimestre = {1: [1,2,3], 2: [4,5,6], 3: [7,8,9], 4: [10,11,12]}
    meses_analise = meses_por_trimestre[tri_atual]
    
    df_trimestre_todos_anos = df[df['Data da notificação'].dt.month.isin(meses_analise)]
    df_trimestre_todos_anos = df_trimestre_todos_anos[df_trimestre_todos_anos['Data da notificação'].dt.year.isin(anos_analise)]
    tabela_grafico = df_trimestre_todos_anos.groupby(['Classificação da Notificação', df_trimestre_todos_anos['Data da notificação'].dt.year]).size().unstack(fill_value=0)
    
    if ano_atual in tabela_grafico.columns: tabela_grafico = tabela_grafico.sort_values(by=ano_atual, ascending=False)
    lista_cores = [cores_personalizadas.get(ano, '#333333') for ano in tabela_grafico.columns]
    
    fig, ax = plt.subplots(figsize=(16, 7))
    tabela_grafico.plot(kind='bar', ax=ax, width=0.85, color=lista_cores, zorder=3)
    
    labels_originais = [item.get_text() for item in ax.get_xticklabels()]
    labels_quebrados = [textwrap.fill(texto, width=15) for texto in labels_originais]
    ax.set_xticklabels(labels_quebrados, rotation=0, fontsize=9)
    
    ax.set_title(f'Número de notificações realizadas por tipo de classificação\nComparativo do {tri_atual}º Trimestre ({anos_analise[0]} a {ano_atual})', fontsize=16, fontweight='bold', pad=40)
    ax.set_ylabel('Nº de notificações')
    ax.set_xlabel('')
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax.legend(title='', frameon=False, loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=len(anos_analise))

    for container in ax.containers: ax.bar_label(container, padding=3, fmt='%d', fontsize=8, fontweight='bold')
    for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
    fig.tight_layout()
    return fig

def gerar_analise_ia_bloco_3(df, api_key):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual, tri_atual = df['Data da notificação'].max().year, df['Data da notificação'].max().quarter
    ano_anterior = ano_atual - 1

    df_tri = df[df['Data da notificação'].dt.quarter == tri_atual]
    tabela_historico = df_tri.groupby(['Classificação da Notificação', df_tri['Data da notificação'].dt.year]).size().unstack(fill_value=0)
    
    if ano_atual in tabela_historico.columns and ano_anterior in tabela_historico.columns:
        var_ano_a_ano = ((tabela_historico[ano_atual] - tabela_historico[ano_anterior]) / tabela_historico[ano_anterior]) * 100
        var_ano_a_ano = var_ano_a_ano.replace([float('inf'), -float('inf')], 0).fillna(0)
        relevantes = tabela_historico[(tabela_historico[ano_atual] > 0) | (tabela_historico[ano_anterior] > 0)].index
        var_ano_a_ano = var_ano_a_ano[relevantes]
        
        if not var_ano_a_ano.empty:
            nome_menor, nome_maior = var_ano_a_ano.idxmin(), var_ano_a_ano.idxmax() 
            df_atual = df_tri[df_tri['Data da notificação'].dt.year == ano_atual]
            descricoes_queda = df_atual[df_atual['Classificação da Notificação'] == nome_menor]['Descrição do incidente'].dropna().head(5).tolist()
            descricoes_alta = df_atual[df_atual['Classificação da Notificação'] == nome_maior]['Descrição do incidente'].dropna().head(5).tolist()

            prompt = f"""Atue como Analista de Qualidade. Analise os dados do {tri_atual}º Trimestre.
            Tabela Histórica:\n{tabela_historico.to_string()}\n
            Descrições reais para justificar {ano_atual}:
            - Categoria de maior queda ('{nome_menor}'): {descricoes_queda}
            - Categoria de maior aumento ('{nome_maior}'): {descricoes_alta}
            Escreva 2 ou 3 parágrafos focando na gestão de risco e comparando o {tri_atual}º Tri de {ano_atual} vs {ano_anterior}."""
            try:
                nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
                return f"*(Análise modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
            except Exception as e: return f"Erro IA: {e}"
    return "Dados insuficientes."

# --- BLOCO 4 ---
def preparar_dados_bloco_4(df):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual, tri_atual = df['Data da notificação'].max().year, df['Data da notificação'].max().quarter
    ano_anterior = ano_atual - 1

    df_atual = df[(df['Data da notificação'].dt.year == ano_atual) & (df['Data da notificação'].dt.quarter == tri_atual)]
    df_anterior = df[(df['Data da notificação'].dt.year == ano_anterior) & (df['Data da notificação'].dt.quarter == tri_atual)]

    tabela_comparativa = pd.DataFrame({f'{tri_atual}º Tri {ano_atual}': df_atual['Classificação da Notificação'].value_counts(), 
                                       f'{tri_atual}º Tri {ano_anterior}': df_anterior['Classificação da Notificação'].value_counts()}).fillna(0).astype(int)
    
    ea_atual = df_atual[df_atual['Classificação da Notificação'] == 'Evento adverso']
    vilao_geral = ea_atual['Incidente'].value_counts().index[0] if not ea_atual.empty else "N/A"
    
    df_turnos = pd.DataFrame([{'Turno': t, 'Casos': q, 'Principal Incidente': ea_atual[ea_atual['Turno']==t]['Incidente'].value_counts().index[0]} 
                              for t, q in ea_atual['Turno'].value_counts().items() if not ea_atual[ea_atual['Turno']==t].empty])

    return tabela_comparativa, df_turnos, df_atual, vilao_geral, tri_atual, ano_atual, ano_anterior

def gerar_analise_ia_bloco_4(tabela_comp, df_turnos, df_atual, vilao_geral, tri_atual, ano_atual, ano_anterior):
    descricoes = df_atual[(df_atual['Classificação da Notificação'] == 'Evento adverso') & (df_atual['Incidente'] == vilao_geral)]['Descrição do incidente'].dropna().head(6).tolist()
    prompt = f"""Atue como Gerente de Qualidade. Faça a análise do {tri_atual}º Trimestre de {ano_atual}.
    Tabela:\n{tabela_comp.to_string()}\nTurnos:\n{df_turnos.to_string(index=False)}\n
    Descrições reais de '{vilao_geral}': {descricoes}
    Escreva 3 parágrafos técnicos analisando a tabela geral, a causa raiz do ofensor '{vilao_geral}' e a especificidade dos turnos."""
    try:
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        return f"*(Análise modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
    except Exception as e: return f"Erro IA: {e}"

# --- BLOCO 5 ---
def preparar_dados_bloco_5(df, pac_dia_atual, pac_dia_ant):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual, tri_atual = df['Data da notificação'].max().year, df['Data da notificação'].max().quarter
    ano_anterior = ano_atual - 1

    df_atual = df[(df['Data da notificação'].dt.year == ano_atual) & (df['Data da notificação'].dt.quarter == tri_atual)]
    df_anterior = df[(df['Data da notificação'].dt.year == ano_anterior) & (df['Data da notificação'].dt.quarter == tri_atual)]

    ea_atual = df_atual[df_atual['Classificação da Notificação'] == 'Evento adverso']
    ea_anterior = df_anterior[df_anterior['Classificação da Notificação'] == 'Evento adverso']

    densidade_atual = (len(ea_atual) / pac_dia_atual) * 1000 if pac_dia_atual > 0 else 0
    densidade_ant = (len(ea_anterior) / pac_dia_ant) * 1000 if pac_dia_ant > 0 else 0

    tabela_gravidade = pd.DataFrame({f'{ano_anterior}': ea_anterior['Grau do dano'].value_counts(), f'{ano_atual}': ea_atual['Grau do dano'].value_counts()}).fillna(0).astype(int)
    tabela_gravidade['Variação (Casos)'] = tabela_gravidade[f'{ano_atual}'] - tabela_gravidade[f'{ano_anterior}']
    tabela_gravidade['Variação (%)'] = ((tabela_gravidade['Variação (Casos)'] / tabela_gravidade[f'{ano_anterior}']) * 100).replace([float('inf'), -float('inf')], 100).fillna(0).round(1)

    tax_atual = df_atual[df_atual['Taxonomia da OMS'].notna() & (df_atual['Taxonomia da OMS'] != '')]
    tax_anterior = df_anterior[df_anterior['Taxonomia da OMS'].notna() & (df_anterior['Taxonomia da OMS'] != '')]
    tabela_taxonomia = pd.DataFrame({f'{ano_anterior}': tax_anterior['Taxonomia da OMS'].value_counts(), f'{ano_atual}': tax_atual['Taxonomia da OMS'].value_counts()}).fillna(0).astype(int)
    tabela_taxonomia['Variação (Casos)'] = tabela_taxonomia[f'{ano_atual}'] - tabela_taxonomia[f'{ano_anterior}']
    tabela_taxonomia['Variação (%)'] = ((tabela_taxonomia['Variação (Casos)'] / tabela_taxonomia[f'{ano_anterior}']) * 100).replace([float('inf'), -float('inf')], 100).fillna(0).round(1)
    tabela_taxonomia = tabela_taxonomia.sort_values(f'{ano_atual}', ascending=False)

    return tabela_gravidade, tabela_taxonomia, densidade_atual, densidade_ant, len(ea_atual), df_atual, tri_atual, ano_atual, ano_anterior

def gerar_analise_ia_bloco_5(tabela_gravidade, tabela_taxonomia, densidade_atual, densidade_ant, total_ea_atual, df_atual, tri_atual, ano_atual, ano_anterior):
    ea_atual = df_atual[df_atual['Classificação da Notificação'] == 'Evento adverso']
    descricoes_graves = ea_atual[ea_atual['Grau do dano'].isin(['Grave', 'Óbito', 'Moderado'])]['Descrição do incidente'].dropna().head(4).tolist()
    top_taxonomia = tabela_taxonomia.index[0] if not tabela_taxonomia.empty else "N/A"
    descricoes_taxonomia = df_atual[df_atual['Taxonomia da OMS'] == top_taxonomia]['Descrição do incidente'].dropna().head(4).tolist()

    prompt = f"""Atue como Especialista em Segurança do Paciente. Escreva a análise para o {tri_atual}º Trimestre de {ano_atual}.
    - Incidência {ano_atual}: {densidade_atual:.2f} por 1.000 pacientes/dia (Anterior: {densidade_ant:.2f}). Total Eventos: {total_ea_atual}.
    - Gravidade do Dano:\n{tabela_gravidade.to_string()}\n- Taxonomia OMS (Top 5):\n{tabela_taxonomia.head(5).to_string()}
    Descrições reais:
    - Danos Graves/Moderados: {descricoes_graves}
    - Taxonomia líder '{top_taxonomia}': {descricoes_taxonomia}
    Escreva 4 parágrafos técnicos: 1. Densidade. 2. Gravidade (usando descrições). 3. Taxonomia OMS (usando descrições). 4. Conclusão de Gestão."""
    try:
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        return f"*(Análise modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
    except Exception as e: return f"Erro IA: {e}"

# --- BLOCO 6 ---
def preparar_dados_bloco_6(df, df_setores):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual, tri_atual = df['Data da notificação'].max().year, df['Data da notificação'].max().quarter
    df_atual = df[(df['Data da notificação'].dt.year == ano_atual) & (df['Data da notificação'].dt.quarter == tri_atual)].copy()

    df_atual['Setor_Match'] = df_atual['Setor Responsável'].astype(str).str.strip()
    df_setores['Setor'] = df_setores['Setor'].astype(str).str.strip()
    df_completo = df_atual.merge(df_setores, left_on='Setor_Match', right_on='Setor', how='left')
    
    if 'Assistencial/ Administrativo/ Apoio' in df_completo.columns:
        df_assist = df_completo[df_completo['Assistencial/ Administrativo/ Apoio'].astype(str).str.contains('Assistencial', case=False, na=False)].copy()
    else: df_assist = df_completo
        
    return df_assist, tri_atual, ano_atual

def gerar_grafico_bloco_6(df_assist, tri_atual, ano_atual):
    total_geral = len(df_assist)
    if 'Servico Proprio / Servico tercerizado' in df_assist.columns:
        ranking = df_assist.groupby(['Setor_Match', 'Servico Proprio / Servico tercerizado']).size().unstack(fill_value=0)
        cores = ['#1f4e79' if 'proprio' in str(c).lower() else '#d48e00' for c in ranking.columns]
    else:
        ranking = df_assist.groupby(['Setor_Match']).size().to_frame(name='Total')
        cores = ['#1f4e79']

    ranking['Total'] = ranking.sum(axis=1)
    ranking = ranking.sort_values('Total', ascending=True) 
    totais_plot = ranking['Total'].copy()
    del ranking['Total']

    fig, ax = plt.subplots(figsize=(12, max(8, len(ranking)*0.4)))
    ranking.plot(kind='barh', stacked=True, ax=ax, color=cores, width=0.8, zorder=3)

    for i, v in enumerate(totais_plot): ax.text(v + 0.2, i, str(v), va='center', fontweight='bold', color='black')

    ax.set_title(f'Notificações Assistenciais por Setor - {tri_atual}º Tri {ano_atual} (Total: {total_geral})', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('')
    ax.set_xlabel('Nº de Notificações')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3, zorder=0)
    if 'Servico Proprio / Servico tercerizado' in df_assist.columns:
        ax.legend(title='Serviço Próprio / Terceirizado', frameon=True, loc='lower right')
    fig.tight_layout()
    return fig

def gerar_analise_ia_bloco_6(df_assist, tri_atual, ano_atual):
    total_geral = len(df_assist)
    if 'Servico Proprio / Servico tercerizado' in df_assist.columns:
        total_proprio = len(df_assist[df_assist['Servico Proprio / Servico tercerizado'].astype(str).str.contains('proprio', case=False, na=False)])
        total_terceiro = total_geral - total_proprio
        df_terc = df_assist[df_assist['Servico Proprio / Servico tercerizado'].astype(str).str.contains('tercerizado', case=False, na=False)]
    else:
        total_proprio, total_terceiro, df_terc = total_geral, 0, pd.DataFrame()

    top_setores = df_assist['Setor_Match'].value_counts().head(6).to_dict()
    stats_classificacao = df_assist['Classificação da Notificação'].value_counts().head(5).to_dict()
    stats_incidentes = df_assist['Incidente'].value_counts().head(8).to_dict()

    resumo_terc = ""
    descricoes_terceiros = []
    if not df_terc.empty:
        for setor, grupo in df_terc.groupby('Setor_Match'):
            resumo_terc += f"- {setor} ({len(grupo)} casos): {', '.join(grupo['Incidente'].value_counts().head(2).index.tolist())}.\n"
        descricoes_terceiros = df_terc['Descrição do incidente'].dropna().head(5).tolist()

    top_incidente = list(stats_incidentes.keys())[0] if stats_incidentes else "N/A"
    descricoes_top = df_assist[df_assist['Incidente'] == top_incidente]['Descrição do incidente'].dropna().head(5).tolist()

    prompt = f"""Atue como Especialista em Qualidade. Escreva a Análise de Setores Assistenciais do {tri_atual}º Trimestre de {ano_atual}.
    Totais: {total_geral} ({total_proprio} próprios, {total_terceiro} terceiros). Top Setores: {top_setores}. Natureza: {stats_classificacao}. Falhas: {stats_incidentes}. Terceiros: {resumo_terc}.
    Descrições reais da falha '{top_incidente}': {descricoes_top}. Descrições Terceiros: {descricoes_terceiros}.
    Estrutura: 1. Introdução. 2. Top Setores. 3. Natureza (Cultura Preventiva vs Dano). 4. Processos (Justifique com descrições reais). 5. Terceirizados e Conclusão."""
    try:
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        return f"*(Análise modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
    except Exception as e: return f"Erro IA: {e}"

# --- BLOCO 7 (NOVO: MAPEAMENTO SETORES ADMINISTRATIVOS) ---
def preparar_dados_bloco_7(df, df_setores):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual, tri_atual = df['Data da notificação'].max().year, df['Data da notificação'].max().quarter
    df_atual = df[(df['Data da notificação'].dt.year == ano_atual) & (df['Data da notificação'].dt.quarter == tri_atual)].copy()

    # Prepara para cruzar
    df_atual['Setor_Match'] = df_atual['Setor Responsável'].astype(str).str.strip()
    df_setores['Setor'] = df_setores['Setor'].astype(str).str.strip()
    
    # Validações e merge
    df_validos = df_atual[(df_atual['Setor_Match'].notna()) & (df_atual['Setor_Match'] != "-") & (df_atual['Setor_Match'] != "")].copy()
    total_institucional = len(df_validos)
    
    df_completo = df_validos.merge(df_setores, left_on='Setor_Match', right_on='Setor', how='left')
    
    # Filtra apenas os setores administrativos
    if 'Assistencial/ Administrativo/ Apoio' in df_completo.columns:
        df_admin = df_completo[df_completo['Assistencial/ Administrativo/ Apoio'].astype(str).str.contains('Administrativo', case=False, na=False)].copy()
    else:
        df_admin = df_completo # Fallback
        
    return df_admin, total_institucional, tri_atual, ano_atual

def gerar_grafico_bloco_7(df_admin, tri_atual, ano_atual):
    total_geral = len(df_admin)
    
    if 'Servico Proprio / Servico tercerizado' in df_admin.columns:
        ranking = df_admin.groupby(['Setor_Match', 'Servico Proprio / Servico tercerizado']).size().unstack(fill_value=0)
        cores = ['#4472c4' if 'proprio' in str(c).lower() else '#ed7d31' for c in ranking.columns]
    else:
        ranking = df_admin.groupby(['Setor_Match']).size().to_frame(name='Total')
        cores = ['#4472c4']

    ranking['Total'] = ranking.sum(axis=1)
    ranking = ranking.sort_values('Total', ascending=True) 
    totais_plot = ranking['Total'].copy()
    del ranking['Total']

    fig, ax = plt.subplots(figsize=(12, max(5, len(ranking)*0.5)))
    ranking.plot(kind='barh', stacked=True, ax=ax, color=cores, width=0.8, zorder=3)

    for i, v in enumerate(totais_plot):
        ax.text(v + 0.1, i, str(v), va='center', fontweight='bold', color='black')

    ax.set_title(f'Notificações Administrativas por Setor - {tri_atual}º Tri {ano_atual} (Total: {total_geral})', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('')
    ax.set_xlabel('Nº de Notificações')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3, zorder=0)
    if 'Servico Proprio / Servico tercerizado' in df_admin.columns:
        ax.legend(title='Serviço Próprio / Terceirizado', frameon=True, loc='lower right')
    fig.tight_layout()
    
    return fig

def gerar_analise_ia_bloco_7(df_admin, total_institucional, tri_atual, ano_atual):
    total_admin = len(df_admin)
    pct_admin = (total_admin / total_institucional) * 100 if total_institucional > 0 else 0
    qtd_setores = df_admin['Setor_Match'].nunique()
    top_setores = df_admin['Setor_Match'].value_counts().head(5).to_dict()

    # Radar de Problemas
    top_problemas = df_admin['Incidente'].value_counts()
    texto_detalhe_prob = "Sem dados de incidentes."
    descricoes_top_prob = []
    
    if not top_problemas.empty:
        problema_principal = top_problemas.index[0]
        df_prob1 = df_admin[df_admin['Incidente'] == problema_principal]
        causadores_prob1 = df_prob1['Setor_Match'].value_counts().head(3).to_dict()
        texto_detalhe_prob = f"O problema '{problema_principal}' ocorreu mais nos setores: {causadores_prob1}"
        descricoes_top_prob = df_prob1['Descrição do incidente'].dropna().head(5).tolist()

    # Risco vs Dano
    risco = df_admin[df_admin['Classificação da Notificação'].astype(str).str.contains('Risco|Sem dano', case=False, na=False)]
    pct_risco = (len(risco) / total_admin) * 100 if total_admin > 0 else 0
    danos = df_admin[~df_admin.index.isin(risco.index)]
    
    resumo_danos = danos['Incidente'].value_counts().head(3).to_dict() if not danos.empty else "Nenhum evento com dano."
    descricoes_danos = danos['Descrição do incidente'].dropna().head(3).tolist() if not danos.empty else []

    prompt = f"""
    Atue como Especialista em Qualidade. Escreva a análise das Áreas Administrativas do {tri_atual}º Trimestre de {ano_atual}.

    DADOS ESTATÍSTICOS ADMINISTRATIVOS:
    - Total: {total_admin} registros ({pct_admin:.1f}% do total institucional). Áreas envolvidas: {qtd_setores}.
    - Top 5 Setores mais notificados: {top_setores}
    - Principais Problemas: {top_problemas.head(5).to_dict()}
    - Detalhe do problema Nº 1: {texto_detalhe_prob}
    - Classificação Preventiva: {pct_risco:.1f}% são Risco ou Sem dano.
    - Ocorrências com Dano: {resumo_danos}

    CONTEXTO QUALITATIVO (DESCRIÇÕES REAIS DE PRONTUÁRIOS):
    - Justificativas reais do problema Nº 1: {descricoes_top_prob}
    - Descrições reais dos eventos que geraram Dano (se houver): {descricoes_danos}

    ESTRUTURA OBRIGATÓRIA (5 Parágrafos):
    1. INTRODUÇÃO: Volume total, % representativa e diversidade de setores envolvidos.
    2. DESTAQUE DOS PROBLEMAS: Analise o problema Nº 1. Use as descrições reais para justificar por que ocorreu (ex: falha de comunicação, comportamento, processo).
    3. CLASSIFICAÇÃO E CULTURA: Enalteça a alta taxa preventiva (Risco/Sem dano) citando as diretrizes da ANVISA/WHO para cultura de notificação.
    4. EVENTOS COM DANO: Se houver dano, use as descrições reais para explicar como uma falha administrativa/apoio gerou impacto no paciente.
    5. CONCLUSÃO: Fechamento técnico focando na integração entre áreas de apoio e assistência direta.
    """
    try:
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        return f"*(Análise de Setores Administrativos gerada pelo modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
    except Exception as e: return f"Erro IA: {e}"


# --- BLOCO 8 (NOVO: MAPEAMENTO SETORES DE APOIO) ---
def preparar_dados_bloco_8(df, df_setores):
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual, tri_atual = df['Data da notificação'].max().year, df['Data da notificação'].max().quarter
    df_atual = df[(df['Data da notificação'].dt.year == ano_atual) & (df['Data da notificação'].dt.quarter == tri_atual)].copy()

    df_atual['Setor_Match'] = df_atual['Setor Responsável'].astype(str).str.strip()
    df_setores['Setor'] = df_setores['Setor'].astype(str).str.strip()
    
    df_validos = df_atual[(df_atual['Setor_Match'].notna()) & (df_atual['Setor_Match'] != "-") & (df_atual['Setor_Match'] != "")].copy()
    total_institucional = len(df_validos)
    
    df_completo = df_validos.merge(df_setores, left_on='Setor_Match', right_on='Setor', how='left')
    
    if 'Assistencial/ Administrativo/ Apoio' in df_completo.columns:
        df_apoio = df_completo[df_completo['Assistencial/ Administrativo/ Apoio'].astype(str).str.contains('Apoio', case=False, na=False)].copy()
    else:
        df_apoio = df_completo
        
    return df_apoio, total_institucional, tri_atual, ano_atual

def gerar_grafico_bloco_8(df_apoio, tri_atual, ano_atual):
    total_geral = len(df_apoio)
    
    if 'Servico Proprio / Servico tercerizado' in df_apoio.columns:
        ranking = df_apoio.groupby(['Setor_Match', 'Servico Proprio / Servico tercerizado']).size().unstack(fill_value=0)
        # Cores: Verde Água (Próprio) e Mostarda (Terceirizado)
        cores = ['#328a8a' if 'proprio' in str(c).lower() else '#c29c36' for c in ranking.columns]
    else:
        ranking = df_apoio.groupby(['Setor_Match']).size().to_frame(name='Total')
        cores = ['#328a8a']

    ranking['Total'] = ranking.sum(axis=1)
    ranking = ranking.sort_values('Total', ascending=True) 
    totais_plot = ranking['Total'].copy()
    del ranking['Total']

    fig, ax = plt.subplots(figsize=(12, max(5, len(ranking)*0.5)))
    ranking.plot(kind='barh', stacked=True, ax=ax, color=cores, width=0.8, zorder=3)

    for i, v in enumerate(totais_plot):
        ax.text(v + 0.1, i, str(v), va='center', fontweight='bold', color='black')

    ax.set_title(f'Notificações em Setores de Apoio - {tri_atual}º Tri {ano_atual} (Total: {total_geral})', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('')
    ax.set_xlabel('Nº de Notificações')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3, zorder=0)
    if 'Servico Proprio / Servico tercerizado' in df_apoio.columns:
        ax.legend(title='Serviço Próprio / Terceirizado', frameon=True, loc='lower right')
    fig.tight_layout()
    
    return fig

def gerar_analise_ia_bloco_8(df_apoio, total_institucional, tri_atual, ano_atual):
    total_apoio = len(df_apoio)
    pct_apoio = (total_apoio / total_institucional) * 100 if total_institucional > 0 else 0
    
    if 'Servico Proprio / Servico tercerizado' in df_apoio.columns:
        total_proprio = len(df_apoio[df_apoio['Servico Proprio / Servico tercerizado'].astype(str).str.contains('proprio', case=False, na=False)])
        total_terceiro = total_apoio - total_proprio
    else:
        total_proprio, total_terceiro = total_apoio, 0

    top_setores_df = df_apoio['Setor_Match'].value_counts().head(5)
    pct_concentracao = (top_setores_df.sum() / total_apoio) * 100 if total_apoio > 0 else 0
    top_setores_lista = top_setores_df.index.tolist()

    risco = df_apoio[df_apoio['Classificação da Notificação'].astype(str).str.contains('Risco|Sem dano|Circunstância', case=False, na=False)]
    pct_risco = (len(risco) / total_apoio) * 100 if total_apoio > 0 else 0

    # Cruzamento Setor + Incidente + Descrições + Taxonomia
    analise_detalhada = ""
    for setor in top_setores_lista:
        df_setor = df_apoio[df_apoio['Setor_Match'] == setor]
        problema_principal = df_setor['Incidente'].value_counts().index[0] if not df_setor.empty else "N/A"
        
        # Tenta achar a taxonomia atrelada a esse problema principal
        df_tax = df_setor[df_setor['Incidente'] == problema_principal]
        tax_principal = df_tax['Taxonomia da OMS'].value_counts().index[0] if not df_tax.empty and 'Taxonomia da OMS' in df_tax.columns else "N/A"
        
        descricoes = df_tax['Descrição do incidente'].dropna().head(3).tolist()
        analise_detalhada += f"- Setor: {setor} | Taxonomia predominante: '{tax_principal}' | Principal Incidente: '{problema_principal}' | Descrições reais: {descricoes}\n"

    prompt = f"""
    Atue como Analista de Qualidade e Estrutura Hospitalar. Escreva a análise das Áreas de Apoio do {tri_atual}º Trimestre de {ano_atual}.

    DADOS ESTATÍSTICOS GERAIS:
    - Total Apoio: {total_apoio} registros ({pct_apoio:.1f}% do total institucional).
    - Origem: {total_proprio} registros de equipes próprias e {total_terceiro} de terceirizadas.
    - Concentração: Os 5 maiores setores ({', '.join(top_setores_lista)}) representam {pct_concentracao:.1f}% das notificações de apoio.
    - Classificação Preventiva: {pct_risco:.1f}% das notificações foram Sem Dano ou Risco.

    CONTEXTO QUALITATIVO (TAXONOMIA E DESCRIÇÕES):
    Use os dados abaixo para detalhar os gargalos operacionais:
    {analise_detalhada}

    ESTRUTURA OBRIGATÓRIA (4 a 5 Parágrafos):
    1. INTRODUÇÃO: Cite o volume ({total_apoio}), a representatividade ({pct_apoio:.1f}%) e a divisão Próprio/Terceirizado. Reforce que segurança assistencial depende de fatores logísticos/estruturais.
    2. CONCENTRAÇÃO: Liste a concentração de {pct_concentracao:.1f}% nos top setores, evidenciando áreas de interação direta com o paciente.
    3. ANÁLISE TAXONÔMICA (O Cérebro do Texto): Use o "Contexto Qualitativo" fornecido. Agrupe os setores por afinidade e crie tópicos. Use as "Descrições reais" para explicar exatamente o que aconteceu (ex: se for rouparia, cite as falhas de enxoval).
    4. CULTURA DE NOTIFICAÇÃO: Cite a diretriz da ANVISA (2023) sobre falhas organizacionais. Relacione isso à alta taxa preventiva de {pct_risco:.1f}%.
    5. CONCLUSÃO: Sugira ações de melhoria focadas nos gargalos logísticos descobertos.
    """
    try:
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        return f"*(Análise de Setores de Apoio gerada pelo modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
    except Exception as e: return f"Erro IA: {e}"


# --- BLOCO 9 (NOVO: INDICADORES DE QUALIDADE) ---
def preparar_dados_bloco_9(arquivo_indicadores, df_principal):
    import pandas as pd
    
    # 1. Leitura dinâmica do cabeçalho da planilha de indicadores
    df_temp = pd.read_excel(arquivo_indicadores, header=None)
    idx_cabecalho = 0
    for idx, row in df_temp.iterrows():
        linha_texto = row.astype(str).str.lower().values
        if any('flebite' in x for x in linha_texto) or any('queda' in x for x in linha_texto):
            idx_cabecalho = idx
            break
            
    # Reseta o ponteiro do arquivo para ler de novo corretamente no Streamlit
    arquivo_indicadores.seek(0)
    df = pd.read_excel(arquivo_indicadores, header=idx_cabecalho)

    # 2. Limpeza de Colunas
    colunas_novas = list(df.columns)
    colunas_novas[0] = 'Ano'
    colunas_novas[1] = 'Mes'
    df.columns = colunas_novas

    # Padronização de nomes
    mapa_colunas = {}
    for col in df.columns:
        col_lower = str(col).lower()
        if 'medic' in col_lower: mapa_colunas[col] = 'Erro de Medicação'
        elif 'flebite' in col_lower: mapa_colunas[col] = 'Flebite'
        elif 'les' in col_lower and 'pele' in col_lower: mapa_colunas[col] = 'Lesão de Pele'
        elif 'queda' in col_lower: mapa_colunas[col] = 'Queda'

    df.rename(columns=mapa_colunas, inplace=True)
    df['Ano'] = df['Ano'].ffill()

    # Conversão de Meses
    mapa_meses = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'MarÃ§o': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6,
                  'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
    
    df['Mes_Num'] = df['Mes'].astype(str).str.strip().apply(lambda x: mapa_meses.get(x) if x in mapa_meses else 0).astype(int)
    df = df[df['Mes_Num'] > 0].copy()
    df['Dia'] = 1
    df['Data'] = pd.to_datetime(df[['Ano', 'Mes_Num', 'Dia']].rename(columns={'Ano': 'year', 'Mes_Num': 'month', 'Dia': 'day'}))

    # Filtro de 3 anos (Automático)
    ultima_data = df['Data'].max()
    ano_atual = ultima_data.year
    tri_num = (ultima_data.month - 1) // 3 + 1
    ano_inicio = ano_atual - 2
    df_grafico = df[df['Data'].dt.year >= ano_inicio].copy()
    
    # 3. Extraindo as "Descrições Reais" da base principal (A Mágica da IA)
    df_principal['Data da notificação'] = pd.to_datetime(df_principal['Data da notificação'])
    df_princ_tri = df_principal[(df_principal['Data da notificação'].dt.year == ano_atual) & (df_principal['Data da notificação'].dt.quarter == tri_num)]
    
    descricoes = {}
    if 'Incidente' in df_princ_tri.columns and 'Descrição do incidente' in df_princ_tri.columns:
        descricoes['Erro de Medicação'] = df_princ_tri[df_princ_tri['Incidente'].astype(str).str.contains('medic|prescrição|dispensação', case=False, na=False)]['Descrição do incidente'].dropna().head(3).tolist()
        descricoes['Flebite'] = df_princ_tri[df_princ_tri['Incidente'].astype(str).str.contains('flebite|acesso', case=False, na=False)]['Descrição do incidente'].dropna().head(3).tolist()
        descricoes['Lesão de Pele'] = df_princ_tri[df_princ_tri['Incidente'].astype(str).str.contains('lesão por pressão|pele', case=False, na=False)]['Descrição do incidente'].dropna().head(3).tolist()
        descricoes['Queda'] = df_princ_tri[df_princ_tri['Incidente'].astype(str).str.contains('queda', case=False, na=False)]['Descrição do incidente'].dropna().head(3).tolist()

    return df_grafico, ano_inicio, tri_num, ano_atual, descricoes

def gerar_grafico_bloco_9(df_grafico, ano_inicio, tri_num, ano_atual):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(15, 7))

    cores = {'Erro de Medicação': '#002060', 'Flebite': '#C00000', 'Lesão de Pele': '#ED7D31', 'Queda': '#7030A0'}
    colunas_indicadores = ['Erro de Medicação', 'Flebite', 'Lesão de Pele', 'Queda']

    for col in colunas_indicadores:
        if col in df_grafico.columns:
            import pandas as pd
            df_grafico[col] = pd.to_numeric(df_grafico[col].astype(str).str.replace(',', '.', regex=False), errors='coerce')
            ax.plot(df_grafico['Data'], df_grafico[col], marker='o', linewidth=2, label=col, color=cores.get(col, 'gray'))

    ax.set_xticks(df_grafico['Data'])
    meses_pt = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
    labels_x = [f"{meses_pt[d.month]}/{str(d.year)[2:]}" for d in df_grafico['Data']]
    ax.set_xticklabels(labels_x, rotation=45, ha='right', fontsize=9)

    ax.set_title(f"Incidência de eventos adversos ({ano_inicio} a {tri_num}º Tri {ano_atual})", fontsize=14, fontweight='bold', pad=40)
    ax.set_ylabel('Taxa de Incidência (por 1.000 ou %)')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=4, frameon=False, fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    return fig

def gerar_analise_ia_bloco_9(df_grafico, tri_num, ano_atual, descricoes):
    import pandas as pd
    colunas_indicadores = ['Erro de Medicação', 'Flebite', 'Lesão de Pele', 'Queda']
    
    medias_anuais = df_grafico.groupby('Ano')[colunas_indicadores].mean().round(2).to_dict()
    
    mes_inicio_tri = (tri_num - 1) * 3 + 1
    data_inicio_tri = pd.Timestamp(year=ano_atual, month=mes_inicio_tri, day=1)
    df_tri_atual = df_grafico[df_grafico['Data'] >= data_inicio_tri]

    resumo_tri = []
    for idx, row in df_tri_atual.iterrows():
        item = {'Mes': row['Mes'], 'Ano': row['Ano']}
        for c in colunas_indicadores:
            if c in row: item[c] = row[c]
        resumo_tri.append(item)

    prompt = f"""
    Atue como Especialista em Qualidade Hospitalar. Escreva a Análise Descritiva de Indicadores para o {tri_num}º TRIMESTRE de {ano_atual}.

    [DADOS MATEMÁTICOS - TAXAS MÉDIAS ANUAIS]:
    {medias_anuais}

    [DADOS MATEMÁTICOS - TRIMESTRE ATUAL]:
    {resumo_tri}

    [CONTEXTO QUALITATIVO - DESCRIÇÕES REAIS DE PRONTUÁRIOS]:
    Use essas descrições para justificar os aumentos ou picos nos indicadores:
    - Erro de Medicação: {descricoes.get('Erro de Medicação', [])}
    - Flebite: {descricoes.get('Flebite', [])}
    - Lesão de Pele: {descricoes.get('Lesão de Pele', [])}
    - Queda: {descricoes.get('Queda', [])}

    ESTRUTURA OBRIGATÓRIA (4 Tópicos e 1 Conclusão):
    I. Incidência de erro de medicação: Comparativo anual. Fechamento do trimestre (cite os meses). Use as descrições para justificar as falhas. Meta: < 5 eventos/1000.
    II. Incidência de Flebite: Tendência. Use as descrições. Meta: < 5%.
    III. Incidência de lesão de pele por pressão: Analise picos. Use descrições. Meta: <= 1.0/1000.
    IV. Incidência de queda: Fechamento. Use descrições. Meta: 0.3 a 0.7/1000.
    V. Conclusão Geral: Resumo focando na gestão das unidades assistenciais.

    Tom: Técnico e Executivo.
    """
    try:
        import google.generativeai as genai
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        return f"*(Análise de Indicadores gerada pelo modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
    except Exception as e: return f"Erro IA: {e}"


# --- BLOCO 10 (NOVO: CUMPRIMENTO DAS ANÁLISES E TRATATIVAS) ---
def preparar_dados_bloco_10(df):
    import pandas as pd
    import numpy as np

    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual = df['Data da notificação'].max().year
    tri_atual = df['Data da notificação'].max().quarter

    # Filtra os últimos 5 anos
    df_historico = df[(df['Data da notificação'].dt.year >= ano_atual - 4) & (df['Data da notificação'].dt.year <= ano_atual)].copy()

    # Nomes das Colunas de Investigação
    col_status = "Status da notificação"
    col_pl = "Unidade responsável pela investigação - PL"
    col_acr = "Unidade responsável pela investigação - ACR"
    col_pac = "Unidade responsável pela investigação - PAC"
    col_efet = "Escala de Efetividade"

    # Previne erros caso a coluna não exista na base enviada
    for c in [col_status, col_pl, col_acr, col_pac, col_efet]:
        if c not in df_historico.columns:
            df_historico[c] = "-"

    # Denominador: Foi encaminhada para tratar?
    def tem_investigacao(row):
        pl = str(row[col_pl]).strip().lower()
        acr = str(row[col_acr]).strip().lower()
        pac = str(row[col_pac]).strip().lower()
        invalidos = ['nan', '-', '', 'nat', 'none']
        return (pl not in invalidos) or (acr not in invalidos) or (pac not in invalidos)

    df_historico['Recebida_Para_Tratar'] = df_historico.apply(tem_investigacao, axis=1)

    # Numerador: Foi realmente concluída?
    def foi_tratada(row):
        status = str(row[col_status]).strip().lower()
        return ('validado' in status) or ('concluído após a investigação' in status)

    df_historico['Tratada'] = df_historico.apply(foi_tratada, axis=1)
    df_historico['Tratada_Real'] = df_historico['Recebida_Para_Tratar'] & df_historico['Tratada']

    # 1. Agrupamento Anual (Barras)
    resumo_anos = df_historico.groupby(df_historico['Data da notificação'].dt.year).agg(
        Recebidas=('Recebida_Para_Tratar', 'sum'), Tratadas=('Tratada_Real', 'sum')
    )
    resumo_anos['Taxa'] = (resumo_anos['Tratadas'] / resumo_anos['Recebidas'] * 100).fillna(0)

    # 2. Agrupamento Mensal do Ano Atual (Linha)
    df_ano_atual = df_historico[df_historico['Data da notificação'].dt.year == ano_atual]
    resumo_mensal = df_ano_atual.groupby(df_ano_atual['Data da notificação'].dt.month).agg(
        Recebidas=('Recebida_Para_Tratar', 'sum'), Tratadas=('Tratada_Real', 'sum')
    )
    resumo_mensal = resumo_mensal.reindex(range(1, 13), fill_value=0)
    resumo_mensal['Taxa'] = (resumo_mensal['Tratadas'] / resumo_mensal['Recebidas'] * 100).fillna(0)

    # 3. Métricas do Trimestre Atual
    mes_inicio_tri = (tri_atual - 1) * 3 + 1
    df_tri = df_ano_atual[df_ano_atual['Data da notificação'].dt.month >= mes_inicio_tri]
    
    tot_rec_tri = df_tri['Recebida_Para_Tratar'].sum()
    tot_trat_tri = df_tri['Tratada_Real'].sum()
    taxa_tri = (tot_trat_tri / tot_rec_tri * 100) if tot_rec_tri > 0 else 0

    # 4. Estatísticas de Ferramentas (PL, ACR, PAC)
    def check_tool(row, col_name):
        return str(row[col_name]).strip().lower() not in ['nan', '-', '', 'nat', 'none']

    stats_ferramentas = {}
    for nome, col in [('Protocolo de Londres', col_pl), ('ACR', col_acr), ('Pareceres (PAC)', col_pac)]:
        rec = df_tri[df_tri.apply(lambda x: check_tool(x, col), axis=1)]
        tot = len(rec)
        trat = rec['Tratada_Real'].sum()
        stats_ferramentas[nome] = {'Recebidas': tot, 'Tratadas': trat, 'Taxa': (trat / tot * 100) if tot > 0 else 0}

    # 5. Efetividade
    df_tri_tratadas = df_tri[df_tri['Tratada_Real'] == True]
    distribuicao_notas = df_tri_tratadas[col_efet].value_counts().sort_index().to_dict() if not df_tri_tratadas.empty else {}

    # 6. ENRIQUECIMENTO DE IA (Descrições Reais)
    descricoes = {}
    # Pega falhas que não foram tratadas
    descricoes['Nao_Tratados'] = df_tri[(df_tri['Recebida_Para_Tratar'] == True) & (df_tri['Tratada_Real'] == False)]['Descrição do incidente'].dropna().head(3).tolist()
    
    # Pega ações tratadas mas inefetivas (Nota <= 2)
    if not df_tri_tratadas.empty:
        df_tri_tratadas[col_efet] = pd.to_numeric(df_tri_tratadas[col_efet], errors='coerce')
        descricoes['Baixa_Efetividade'] = df_tri_tratadas[df_tri_tratadas[col_efet] <= 2]['Descrição do incidente'].dropna().head(3).tolist()

    return resumo_anos, resumo_mensal, ano_atual, tri_atual, tot_rec_tri, tot_trat_tri, taxa_tri, stats_ferramentas, distribuicao_notas, descricoes

def gerar_grafico_bloco_10(resumo_anos, resumo_mensal, ano_atual, tri_atual):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(16, 7))

    # PARTE 1: BARRAS ANUAIS
    x_barras = range(len(resumo_anos))
    cores_barras = ['#1f4e79'] * (len(resumo_anos) - 1) + ['#2E75B6']

    ax.bar(x_barras, resumo_anos['Taxa'], color=cores_barras, width=0.6, label='Histórico Anual')
    for i, v in enumerate(resumo_anos['Taxa']):
        ax.text(i, v + 2, f"{v:.1f}%", ha='center', va='bottom', fontweight='bold', fontsize=10)

    # PARTE 2: LINHA MENSAL (Ano Atual)
    inicio_linha = len(x_barras) + 0.5
    x_linha = [inicio_linha + i for i in range(len(resumo_mensal))]

    ax.plot(x_linha, resumo_mensal['Taxa'], color='#C00000', marker='o', linewidth=2.5, label=f'Detalhe Mensal {ano_atual}')
    for i, v in enumerate(resumo_mensal['Taxa']):
        ax.text(x_linha[i], v + 3, f"{v:.0f}%", ha='center', va='bottom', fontsize=9, color='#C00000', fontweight='bold')

    # Ajustes Eixo X
    labels_anos = [str(ano) for ano in resumo_anos.index]
    meses_pt = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
    labels_mensal = [f"{meses_pt[m]}/{str(ano_atual)[2:]}" for m in resumo_mensal.index]

    ax.set_xticks(list(x_barras) + list(x_linha))
    ax.set_xticklabels(labels_anos + labels_mensal, rotation=45, ha='right')

    ano_inicio = resumo_anos.index[0]
    ax.set_title(f'Cumprimento das análises e tratativas ({ano_inicio}-{ano_atual} + Detalhe Mensal)', fontsize=14, fontweight='bold', pad=30)
    ax.set_ylabel('Taxa de Cumprimento (%)')
    ax.set_ylim(0, 115)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.axvline(x=len(x_barras)-0.25, color='gray', linestyle='--', alpha=0.5)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2, frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    return fig

def gerar_analise_ia_bloco_10(resumo_anos, ano_atual, tri_atual, tot_rec_tri, tot_trat_tri, taxa_tri, stats_ferramentas, distribuicao_notas, descricoes):
    import google.generativeai as genai
    historico_texto = resumo_anos['Taxa'].round(1).to_dict()

    prompt = f"""
    Atue como Especialista em Qualidade Hospitalar. Escreva a análise de "Cumprimento das Análises e Tratativas" para o relatório do {tri_atual}º Trimestre de {ano_atual}.

    [DADOS ESTATÍSTICOS]
    1. Histórico Anual (%): {historico_texto}
    2. {tri_atual}º Trimestre: Recebidas ({tot_rec_tri}) | Tratadas ({tot_trat_tri}) | Taxa ({taxa_tri:.1f}%)
    3. Ferramentas: {stats_ferramentas}
    4. Efetividade das ações tratadas (Notas 1-5, onde 1 é inefetivo e 5 muito efetivo): {distribuicao_notas}

    [CONTEXTO QUALITATIVO - DESCRIÇÕES REAIS DE PRONTUÁRIOS]
    Use esses relatos reais de incidentes para ilustrar os desafios de investigação da instituição:
    - Casos que ficaram SEM tratativa (evidenciando a falta de investigação e inércia): {descricoes.get('Nao_Tratados', [])}
    - Casos COM TRATATIVA, porém ineficientes (Nota baixa): {descricoes.get('Baixa_Efetividade', [])}

    ESTRUTURA OBRIGATÓRIA:
    1. INTRODUÇÃO E HISTÓRICO: Analise a evolução do indicador ao longo dos anos usando os dados do 'Histórico Anual'. Destaque o cenário crítico/estagnação.
    2. DETALHE DO TRIMESTRE: Cite os números do trimestre atual. Mencione a persistência das dificuldades.
    3. FERRAMENTAS: Analise o uso de Protocolo de Londres, ACR e Pareceres. Critique a subutilização de ferramentas estruturadas (PL, ACR) usando os dados numéricos fornecidos.
    4. EFETIVIDADE: Comente a percepção de qualidade das ações (distribuição de notas). USE AS DESCRIÇÕES REAIS FORNECIDAS para exemplificar incidentes sérios que estão sem tratamento ou com tratamento ineficiente.
    5. CONCLUSÃO: Destaque os riscos à cultura de segurança e o possível impacto nas acreditações (ONA, JCI). Sugira intervenções nas ferramentas estruturadas.

    Tom: Crítico, analítico e resolutivo. Aja como o autor do texto.
    """
    try:
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        return f"*(Análise de Cumprimento gerada pelo modelo: {nome_modelo})*\n\n" + genai.GenerativeModel(nome_modelo).generate_content(prompt).text
    except Exception as e: return f"Erro IA: {e}"



# --- BLOCO 11 (NOVO: MAPEAMENTO DE RISCO INSTITUCIONAL - HFMEA & ISHIKAWA) ---
def preparar_dados_bloco_11(df):
    import pandas as pd
    
    df['Data da notificação'] = pd.to_datetime(df['Data da notificação'])
    ano_atual = df['Data da notificação'].max().year
    tri_atual = df['Data da notificação'].max().quarter

    df_tri = df[(df['Data da notificação'].dt.year == ano_atual) & (df['Data da notificação'].dt.quarter == tri_atual)].copy()
    total_notificacoes = len(df_tri)

    # Agrupa os piores incidentes por setor (Foco nos Top 5 Setores para não estourar o limite de leitura da IA)
    resumo_riscos = []
    
    if 'Setor Responsável' in df_tri.columns:
        df_tri['Setor Responsável'] = df_tri['Setor Responsável'].astype(str).str.strip()
        top_setores = df_tri[df_tri['Setor Responsável'] != 'nan']['Setor Responsável'].value_counts().head(5).index.tolist()

        for setor in top_setores:
            df_setor = df_tri[df_tri['Setor Responsável'] == setor]
            top_incidente = df_setor['Incidente'].value_counts().index[0] if not df_setor.empty else "N/A"
            qtd_incidente = df_setor['Incidente'].value_counts().values[0] if not df_setor.empty else 0

            # Tenta pegar descrições, priorizando aquelas com DANO (se a coluna existir)
            if 'Grau do dano' in df_setor.columns:
                com_dano = df_setor[(df_setor['Grau do dano'].notna()) & (~df_setor['Grau do dano'].astype(str).str.contains('Sem dano|Risco', case=False, na=False))]
                if not com_dano.empty:
                    descricoes = com_dano['Descrição do incidente'].dropna().head(4).tolist()
                else:
                    descricoes = df_setor['Descrição do incidente'].dropna().head(4).tolist()
            else:
                descricoes = df_setor['Descrição do incidente'].dropna().head(4).tolist()

            resumo_riscos.append({
                'Setor': setor,
                'Incidente Principal': top_incidente,
                'Quantidade': qtd_incidente,
                'Descricoes Amostra': descricoes
            })

    return resumo_riscos, total_notificacoes, tri_atual, ano_atual


def gerar_analise_ia_bloco_11(resumo_riscos, total_notificacoes, tri_atual, ano_atual):
    import google.generativeai as genai

    prompt = f"""
    Atue como Especialista Master em Gestão de Riscos Hospitalares (Especialista em Metodologia HFMEA e Ishikawa).
    Você está redigindo o capítulo final do relatório: "INTERRELAÇÃO ENTRE AS NOTIFICAÇÕES REALIZADAS E MAPEAMENTO DE RISCO DA INSTITUIÇÃO".

    DADOS DO {tri_atual}º TRIMESTRE DE {ano_atual}:
    - Universo analisado: {total_notificacoes} relatos de incidentes registrados.
    - Top 5 Setores Críticos, seus maiores incidentes e uma amostra de descrições reais relatadas pela equipe:
    {resumo_riscos}

    ESTRUTURA OBRIGATÓRIA DA SUA RESPOSTA:

    1. INTRODUÇÃO: Parágrafo destacando a importância da gestão de riscos proativa e como a "análise inteligente de Processamento de Linguagem Natural (NLP)" sobre os {total_notificacoes} relatos permitiu encontrar clusters de risco.
    
    2. AGRUPAMENTOS DE RISCO: Escolha os 3 riscos mais graves da lista de dados fornecida e estruture EXATAMENTE assim para cada um:
       [Número]. Risco: [Crie um nome técnico para o Risco. Ex: Falha no Protocolo Diagnóstico]
       - Sinalizadores: [Extraia 3 a 5 palavras-chave semânticas das descrições reais enviadas]
       - Setor Foco: [Nome do Setor Real]
       - Volume e Análise: Comece com "Com [X] ocorrências, este cluster indica...". Use as descrições reais para justificar a gravidade. Fale sobre o perigo latente mesmo se não houve dano.

    3. PROPOSTA DE ATUALIZAÇÃO DA MATRIZ DE RISCO (TABELA):
       Crie uma tabela em formato Markdown com exatamente DUAS colunas: "Risco Mapeado" e "Fatores Contribuintes (Ishikawa)".
       Para cada um dos 3 riscos mapeados acima, preencha a coluna de Fatores Contribuintes inventando hipóteses plausíveis usando os 6Ms (Mão de Obra, Método, Material, Máquinas, Meio Ambiente, Medida) que façam sentido com as descrições.
       Use a formatação markdown para tabela. Exemplo: | Risco Mapeado | Fatores Contribuintes (Ishikawa) |

    Tom: Altamente técnico, executivo e com foco em segurança do paciente. Não diga que analisou uma lista, finja que o sistema NLP do hospital gerou isso sozinho.
    """
    try:
        nome_modelo = next((m.name for m in genai.list_models() if 'pro' in m.name.lower() and 'generateContent' in m.supported_generation_methods), "gemini-1.5-flash")
        resposta = genai.GenerativeModel(nome_modelo).generate_content(prompt).text
        return f"*(Mapeamento de Riscos e Tabela de Ishikawa gerados pelo modelo: {nome_modelo})*\n\n" + resposta
    except Exception as e:
        return f"Erro IA: {e}"