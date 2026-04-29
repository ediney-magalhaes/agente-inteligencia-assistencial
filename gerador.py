from docx import Document
import pandas as pd
import processador

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

    df_notificacoes = pd.read_excel(arquivo_notificacoes)
    df_indicadores = pd.read_excel(arquivo_indicadores)

    df_corrigido = processador.carregar_validar(df_notificacoes)

    total_atual, total_tri_anterior, total_ano_anterior, qtde_mensal, qtde_trimestral, var_tri, var_ano, trimestre_atual, ano_atual, trimestre_anterior, ano_anterior, df_atual, df_tri_anterior = processador.preparar_bloco1(df_corrigido, trimestre, ano)