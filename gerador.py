from docx import Document
import pandas as pd
import processador
import visualizador
import utils
import tempfile
from docx.shared import Inches
import os

def gerar_relatorio(trimestre,
                    ano,
                    hospital,
                    arquivo_notificacoes,
                    arquivo_indicadores,
                    imagens,
                    texto_obitos,
                    texto_prontuarios,
                    arquivo_psp,
                    acoes_taticas):
    document = Document()

    # Lendo os arquivos importados
    df_notificacoes = pd.read_excel(arquivo_notificacoes)
    df_indicadores = pd.read_excel(arquivo_indicadores)

    # Chamando a função para validar a planilha carregada
    df_corrigido = processador.carregar_validar(df_notificacoes)

    # Chamada da função do bloco 1
    total_atual, total_tri_anterior, total_ano_anterior, qtde_mensal, qtde_trimestral, var_tri, var_ano, trimestre_atual, ano_atual, trimestre_anterior, ano_anterior, df_atual, df_tri_anterior = processador.preparar_bloco1(df_corrigido)

    # Chamada da função do bloco 2
    tabela_bloco2, contexto_ia_bloco2 = processador.preparar_bloco2(df_atual, df_tri_anterior)

    # Chamada da função do bloco 3
    tabela_bloco3, dicionario_bloco3, contexto_ia_bloco3 = processador.preparar_bloco3(df_atual, df_tri_anterior)

    # Chamada da função do bloco 4
    tabela_bloco4, tabela_top3_bloco4, status_eventos_bloco4, contexto_ia_bloco4 = processador.preparar_bloco4(df_atual, df_tri_anterior)

    # Chamada da função do bloco 5
    tab_tri_atual_bloco5, tab_tri_anterior_bloco5, tab_analise_IA_bloco5 = processador.preparar_bloco_setores(df_atual, df_tri_anterior, utils.COL_SETOR_NOTIFICANTE)

    # Chamada da função do bloco 6
    tab_tri_atual_bloco6, tab_tri_anterior_bloco6, tab_analise_IA_bloco6 = processador.preparar_bloco_setores(df_atual, df_tri_anterior, utils.COL_SETOR)

    # Chamada da função do bloco 7 (Queda)
    df_ano_atual_queda, df_ano_anterior_queda, media_tri_atual_queda, media_tri_anterior_queda, (grau_dano_queda, local_queda, tipo_queda) = processador.preparar_bloco7(df_atual, df_indicadores, utils.INDICADOR_QUEDA, trimestre, ano)

    # Chamada da função do bloco 7 (LPP)
    df_ano_atual_lpp, df_ano_anterior_lpp, df_media_tri_atual_lpp, df_media_tri_anterior_lpp, df_contexto_ia_lpp = processador.preparar_bloco7(df_atual, df_indicadores, utils.INDICADOR_LPP, trimestre, ano)

    # Chamada da função do bloco 7 (Flebite)
    df_ano_atual_fle, df_ano_anterior_fle, df_media_tri_atual_fle, df_media_tri_anterior_fle, df_contexto_ia_fle = processador.preparar_bloco7(df_atual, df_indicadores, utils.INDICADOR_FLEBITE, trimestre, ano)

    # Chamada da função do bloco 7 (Erro Medicação)
    df_ano_atual_med, df_ano_anterior_med, df_media_tri_atual_med, df_media_tri_anterior_med, df_contexto_ia_med = processador.preparar_bloco7(df_atual, df_indicadores, utils.INDICADOR_MEDICACAO, trimestre, ano)

    # Chamada da função do bloco 8
    tabela_tri_atual_bloco8, tabela_tri_anterior_bloco8, tabela_mensal_bloco8, tabela_mensal_anterior_bloco8, df_contexto_ia_bloco8 = processador.preparar_bloco8(df_corrigido)

    # Chamada da função visualização para o gráfico 1
    fig1 = visualizador.grafico_volume_notificacoes(qtde_mensal, qtde_trimestral, trimestre_atual, ano_atual)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig1.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3
    fig2 = visualizador.grafico_classificacoes(tabela_bloco3, trimestre_atual, ano_atual)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig2.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3.1 (Circunstância de Risco)
    fig3 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Incidente (circunstância de risco ou condições inseguras)')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig3.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3.2 (Near Miss)
    fig4 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Near miss')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig4.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3.3 (Incidente Sem Dano)
    fig5 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Incidente sem dano')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig5.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3.4 (Evento Sentinela)
    fig6 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Never event/Evento sentinela (ANVISA/JCI)')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig6.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3.5 (Queixas Técnicas)
    fig7 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Queixa técnica')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig7.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3.6 (Segurança Ocupacional)
    fig8 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Segurança do Trabalho')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig8.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 3.7 (Outra Natureza)
    fig9 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Outra natureza')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig9.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    fig_10 = visualizador.gerar_grafico_top3(dicionario_bloco3, 'Evento adverso')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig_10.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 4.1 (Eventos Adversos - Top 3)
    fig11 = visualizador.gerar_grafico_bloco4_1(tabela_top3_bloco4)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig11.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 7 (Indicadores qualidade)
    medias = {
    'Queda': (media_tri_atual_queda, media_tri_anterior_queda),
    'Lesão de Pele': (df_media_tri_atual_lpp, df_media_tri_anterior_lpp),
    'Flebite': (df_media_tri_atual_fle, df_media_tri_anterior_fle),
    'Erro de medicação': (df_media_tri_atual_med, df_media_tri_anterior_med)
    }
    fig12 = visualizador.gerar_grafico_bloco7_geral(medias, None)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig12.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 7.1 (Erro de Medicação)
    fig13 = visualizador.gerar_grafico_bloco7(df_ano_atual_med, df_ano_anterior_med,utils.INDICADOR_MEDICACAO, None, ano_atual)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig13.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 7.2 (Lesão por Pressão)
    fig14 = visualizador.gerar_grafico_bloco7(df_ano_atual_lpp, df_ano_anterior_lpp,utils.INDICADOR_LPP, None, ano_atual)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig14.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 7.3 (Flebite)
    fig15 = visualizador.gerar_grafico_bloco7(df_ano_atual_fle, df_ano_anterior_fle,utils.INDICADOR_FLEBITE, None, ano_atual)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig15.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 7.4 (Queda)
    fig16 = visualizador.gerar_grafico_bloco7(df_ano_atual_queda, df_ano_anterior_queda,utils.INDICADOR_QUEDA, None, ano_atual)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig16.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)

    # Chamada da função visualização para o gráfico 8 (Cumprimento das Análises)
    fig17 = visualizador.gerar_grafico_bloco8(tabela_tri_atual_bloco8, tabela_tri_anterior_bloco8, tabela_mensal_bloco8, tabela_mensal_anterior_bloco8, ano_atual)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        fig17.savefig(tmp.name)
        document.add_picture(tmp.name)
    os.remove(tmp.name)


    # Montagem do documento Word
    document.add_heading('Relatório Trimestral de Segurança do Paciente', level=0)
    document.add_heading(f'Trimestre {trimestre}, de {ano} no {hospital}', level=1)

    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
        document.save(tmp.name)
    return tmp.name