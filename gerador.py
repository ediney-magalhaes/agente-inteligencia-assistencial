from docx import Document
import pandas as pd
import processador
import utils

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
    total_atual, total_tri_anterior, total_ano_anterior, qtde_mensal, qtde_trimestral, var_tri, var_ano, trimestre_atual, ano_atual, trimestre_anterior, ano_anterior, df_atual, df_tri_anterior = processador.preparar_bloco1(df_corrigido, trimestre, ano)

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