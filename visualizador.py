import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap
import numpy as np

# Função para volume das notificações
def grafico_volume_notificacoes(qtde_mensal, qtde_trimestral, trim_atual, ano_atual):

    # Construção da figura e dos eixos
    fig, ax = plt.subplots(figsize=(16, 7))

    # Extrair anos e meses
    anos = qtde_mensal.index.get_level_values(0).unique()
    meses = qtde_mensal.index.get_level_values(1).unique()
    trimestres = qtde_trimestral.index.get_level_values(1).unique()

    # Configuração das posições das barras
    largura = 0.35
    posicoes = np.arange(len(meses))
    posicoes_trimestre = len(meses) + 1 + np.arange(len(trimestres))

    # Lista de cores
    cores = ['#2E75B6', '#1F4E79']

    # Plotar os anos e meses
    for i, ano in enumerate(anos):
        valores = [qtde_mensal.get((ano, mes), 0) for mes in meses]
        deslocamento = (i - len(anos)/2 + 0.5) * largura
        barras = ax.bar(posicoes + deslocamento, valores, largura, color=cores[i], label=str(ano))
        for barra in barras:
            altura = barra.get_height()
            ax.text(
                barra.get_x() + barra.get_width() / 2, # posição do x (centro da barra)
                altura + 2, # posição do y (acima da barra)
                str(int(altura)),
                ha='center', va='bottom', # alinhamento
                fontsize=8, fontweight='bold'
            )
    
    # Plotando os trimestres 
    for i, ano in enumerate(anos):
        valores_tri = [qtde_trimestral.get((ano, tri), 0) for tri in trimestres]
        deslocamento_tri = (i - len(anos) / 2 + 0.5) * largura
        barra_tri = ax.bar(posicoes_trimestre + deslocamento_tri, valores_tri, largura, color=cores[i])
        for bar in barra_tri:
            altura_tri = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                altura_tri + 2,
                str(int(altura_tri)),
                ha='center', va='bottom',
                fontsize=8, fontweight='bold'
            )
    
    # dicionário dos meses
    nomes_meses = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 
               6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 
               11:'Nov', 12:'Dez'}
    
    # dicionário dos trimestres
    nomes_trimestres = {1: '1º Tri', 2: '2º Tri', 3: '3º Tri', 4: '4º Tri'}

    # Nomes dos meses e trimestres
    rotulos_meses = [nomes_meses[mes] for mes in meses]
    rotulos_trimestres = [nomes_trimestres[tri] for tri in trimestres]

    # Concatena as posições aos nomes
    todas_posicoes = np.concatenate([posicoes, posicoes_trimestre])
    todos_rotulos = rotulos_meses + rotulos_trimestres

    # Configuração do eixo X
    ax.set_xticks(todas_posicoes)
    ax.set_xticklabels(todos_rotulos, rotation=0, fontsize=9)

    # Configurando título
    ax.set_title('Número de notificações realizadas', fontsize=14, fontweight='bold', pad=30)

    # Configurando subtítulo
    #anos_texto = ' e '.join([str(a) for a in anos])
    #ax.text(0.5, 1.04, f'Comparativo dos anos de {anos_texto}',
    #        transform=ax.transAxes, ha='center', fontsize=9)
    
    # Separando meses dos trimestres (linha vertical)
    ax.axvline(x=len(meses) + 0.5, color='gray', linestyle='--', alpha=0.5)

    # Grade horizontal
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Remover bordas (superior e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adicionando legenda
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=(len(anos)), frameon=False)

    # Rótulo do eixo Y
    ax.set_ylabel('Nº de notificações', fontsize=10)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()
    return fig

# Função para o gráfico de comparação das classificações
def grafico_classificacoes(tabela_classificacao, trim_atual, ano_atual):
    # Criando a figura
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Extraindo as classificações
    classificacoes = tabela_classificacao.index

    # Lista de cores e largura
    cores = ['#2E75B6', '#1F4E79']
    largura = 0.35

    # Definindo posição das barras
    posicoes = np.arange(len(classificacoes))

    # Plotando barras do ano anterior
    barras_ant = ax.bar(posicoes - largura/2, tabela_classificacao['Trimestre anterior'], largura, color=cores[0], label=str(ano_atual - 1))

    # Configurando os rótulos
    for barra in barras_ant:
        altura = barra.get_height()
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            altura + 2,
            str(int(altura)),
            ha='center', va='bottom',
            fontsize=8, fontweight='bold'
        )

    # Plotando barras do ano atual
    barras_atual = ax.bar(posicoes + largura/2, tabela_classificacao['Trimestre atual'], largura, color=cores[1], label=str(ano_atual))

    # Configurando os rótulos
    for bar in barras_atual:
        altura_atual = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            altura_atual + 2,
            str(int(altura_atual)),
            ha='center', va='bottom',
            fontsize=8, fontweight='bold'
        )

    # Configurando eixo X
    ax.set_xticks(posicoes)
    ax.set_xticklabels(classificacoes, rotation=15, ha='right', fontsize=8)

    # Configurando título
    ax.set_title('Número de notificações realizadas por tipo de classificação', fontsize=14, fontweight='bold', pad=30)

    # Configurando subtítulo
    #anos_texto = ' e '.join([str(a) for a in anos])
    ax.text(0.5, 1.04, f'Comparativo do {trim_atual}º trimestre dos anos {ano_atual - 1} e {ano_atual}',
            transform=ax.transAxes, ha='center', fontsize=9)
    
    # Adicionando legenda
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False)

    # Grade horizontal
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Remover bordas (superior e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Rótulo do eixo Y
    ax.set_ylabel('Nº de notificações', fontsize=10)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()
    return fig

# Função para gráficos top 3 por classificação
def gerar_grafico_top3(dicionario, classificacao):
    tabela = dicionario[classificacao].iloc[::-1]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.barh(tabela.index, tabela['Frequência'])

    for patch in ax.patches:
        valor = patch.get_width()
        posicao_x = valor
        posicao_y = patch.get_y() + patch.get_height() / 2
        ax.text(posicao_x, posicao_y, str(int(valor)), ha='left', va='center')

    nome_ajustado = textwrap.fill(classificacao, 40)
    # Configurando título
    ax.set_title(f'Top 3 notificações mais realizadas - {nome_ajustado}', fontsize=14, fontweight='bold', pad=30)

    # Remover bordas (superior e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Rótulo do eixo Y
    ax.set_ylabel('Tipo de incidentes', fontsize=10)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()
    return fig

# Função para gráfico Eventos Adversos
def gerar_grafico_bloco4_1(tabela_top3_eventos):
    tabela_ordenada = tabela_top3_eventos.iloc[::-1]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.barh(tabela_ordenada.index, tabela_ordenada['Frequência'])

    for patch in ax.patches:
        valor = patch.get_width()
        posicao_x = valor
        posicao_y = patch.get_y() + patch.get_height() / 2
        ax.text(posicao_x, posicao_y, str(int(valor)), ha='left', va='center')

    # Configurando título
    ax.set_title('Top 3 Eventos Adversos mais notificados', fontsize=14, fontweight='bold', pad=30)

    # Remover bordas (superior e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Rótulo do eixo X
    ax.set_ylabel('Tipo de eventos', fontsize=10)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()
    return fig

# Função para gerar gráficos: Flebite, Erro de medicação, LPP e Queda
def gerar_grafico_bloco7(df_ano_atual, df_ano_anterior, indicador, trim_atual, ano_atual):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plotando o ano atual
    ax.plot(df_ano_atual['Mês'], df_ano_atual[indicador], label=ano_atual)

    # Plotando o ano anterior
    ax.plot(df_ano_anterior['Mês'], df_ano_anterior[indicador], label=(ano_atual - 1))

    # Configurando título
    ax.set_title(f'Índices de {indicador}', fontsize=14, fontweight='bold', pad=30)

    # Remover bordas (superior e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adicionando legenda
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False)

    # Rótulo do eixo Y e X
    ax.set_ylabel('Nº notificações', fontsize=10)
    ax.set_xlabel('Período', fontsize=10)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()
    return fig

# Função para gráfico trimestral dos indicadores de qualidade
def gerar_grafico_bloco7_geral(medias, metas):
    nomes = list(medias.keys())

    lista_atual = []
    lista_anterior = []
    # Extrair valore das médias trimestrais
    for atual, anterior in medias.values():
        lista_atual.append(atual)
        lista_anterior.append(anterior)

    fig, ax = plt.subplots(figsize=(14, 6))

    # Configurando posição dos grupos no eixo
    posicoes = np.arange(len(nomes))
    largura = 0.35
    
    # Lista de cores e largura
    cores = ['#2E75B6', '#1F4E79']
    
    # Barra trimestre atual
    barra_atual = ax.bar(posicoes - largura / 2, lista_atual, largura, color=cores[1], label='Trimestre atual')

    # Barra trimestre anterior
    barra_anterior = ax.bar(posicoes + largura / 2, lista_anterior, largura, color=cores[0], label='Trimestre anterior')

    # Rótulos
    ax.bar_label(barra_atual, padding=3, fmt='%.2f', fontsize=9)
    ax.bar_label(barra_anterior, padding=3, fmt='%.2f', fontsize=9)

    # Configurando eixo X
    ax.set_xticks(posicoes)
    ax.set_xticklabels(nomes)

    # Configurando título
    ax.set_title('Índices de qualidade — Comparativo trimestral', fontsize=14, fontweight='bold', pad=30)

    # Remover bordas (superior e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adicionando legenda
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=2, frameon=False)

    # Rótulo do eixo Y e X
    ax.set_ylabel('Índices', fontsize=10)
    ax.set_xlabel('Classificações', fontsize=10)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()
    return fig

# Gráfico para cumprimento das análises
def gerar_grafico_bloco8(tabela_tri_atual, tabela_tri_anterior, tabela_mensal,tabela_mensal_anterior, ano_atual):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Extrair anos e meses
    anos = [ano_atual - 1, ano_atual]
    meses = tabela_mensal_anterior.index
    trimestres = tabela_tri_anterior.index

    # Configuração das posições das barras no eixo X
    largura = 0.35
    posicoes = np.arange(len(meses))
    posicoes_trimestre = len(meses) + 1 + np.arange(len(trimestres))

    # Lista de cores
    cores = ['#2E75B6', '#1F4E79']

    # Selecionar tabelas e valores para plotagem
    for i, ano in enumerate(anos):
        if i == 0:
            tabela_mes = tabela_mensal_anterior
            tabela_tri = tabela_tri_anterior
        else:
            tabela_mes = tabela_mensal
            tabela_tri = tabela_tri_atual
        valores = [tabela_mes['Taxa de cumprimento'].get(mes, np.nan) for mes in meses]
        valores_tri = [tabela_tri['Taxa de cumprimento'].get(tri, np.nan) for tri in trimestres]
        deslocamento = (i - len(anos)/2 + 0.5) * largura
        barras = ax.bar(posicoes + deslocamento, valores, largura, color=cores[i], label=str(ano))
        for barra in barras:
            altura = barra.get_height()
            if altura > 0:
                ax.text(
                    barra.get_x() + barra.get_width() / 2, # posição do x (centro da barra)
                    altura + 2, # posição do y (acima da barra)
                    f'{altura:.1f}%',
                    ha='center', va='bottom', # alinhamento
                    fontsize=8, fontweight='bold'
                )
        # Plotando os trimestres 
            valores_tri = [tabela_tri['Taxa de cumprimento'].get(tri, np.nan) for tri in trimestres]
            deslocamento_tri = (i - len(anos) / 2 + 0.5) * largura
            barra_tri = ax.bar(posicoes_trimestre + deslocamento_tri, valores_tri, largura, color=cores[i])
            for bar in barra_tri:
                altura_tri = bar.get_height()
                if altura_tri > 0:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        altura_tri + 2,
                        f'{altura_tri:.1f}%',
                        ha='center', va='bottom',
                        fontsize=8, fontweight='bold'
                    )

    # dicionário dos meses
    nomes_meses = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 
               6:'Jun', 7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 
               11:'Nov', 12:'Dez'}
    
    # dicionário dos trimestres
    nomes_trimestres = {1: '1º Tri', 2: '2º Tri', 3: '3º Tri', 4: '4º Tri'}

    # Nomes dos meses e trimestres
    rotulos_meses = [nomes_meses[mes] for mes in meses]
    rotulos_trimestres = [nomes_trimestres[tri] for tri in trimestres]

    # Concatena as posições aos nomes
    todas_posicoes = np.concatenate([posicoes, posicoes_trimestre])
    todos_rotulos = rotulos_meses + rotulos_trimestres

    # Configuração do eixo X
    ax.set_xticks(todas_posicoes)
    ax.set_xticklabels(todos_rotulos, rotation=0, fontsize=9)

    # Configurando título
    ax.set_title('Taxa de Cumprimento das Análises das Notificações', fontsize=14, fontweight='bold', pad=30)
    
    # Separando meses dos trimestres (linha vertical)
    ax.axvline(x=len(meses) + 0.5, color='gray', linestyle='--', alpha=0.5)

    # Grade horizontal
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Remover bordas (superior e direita)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Adicionando legenda
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=(len(anos)), frameon=False)

    # Rótulo do eixo Y
    ax.set_ylabel('Taxa', fontsize=10)

    fig.subplots_adjust(top=0.85)
    fig.tight_layout()
    return fig