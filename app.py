import streamlit as st
import traceback
import pandas as pd
import processador
import resultados

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Sistema de Inteligência Assistencial", layout="wide")

# Renderizar título principal da página
st.title("🏥Sistema de Inteligência Assistencial")

# Criar abas de navegação
aba1, aba2, aba3 = st.tabs(["📋 Relatório", "📊 Painel Epidemiológico", "🤖 Agente IA"])
with aba1:
    sub1, sub2, sub5 = st.tabs(["⚙️ Configuração", "📁 Dados EPIMED", "📊 Resultados"])
    with sub1:
        st.write("Configuração")
        st.session_state['trimestre'] = st.selectbox("Trimestre", [1, 2, 3, 4])
        st.session_state['ano'] = st.number_input("Ano", min_value=2020, max_value=2030)
        st.session_state['hospital'] = st.text_input("Nome do Hospital")
    with sub2:
        arquivo_notificacoes = st.file_uploader("Planilha de Notificações", type=["xlsx"])
        arquivo_indicadores = st.file_uploader("Planilha de Indicadores", type=["xlsx"])

        if arquivo_notificacoes:
            st.session_state["arquivo_notificacoes"] = arquivo_notificacoes
        if arquivo_indicadores:
            st.session_state["arquivo_indicadores"] = arquivo_indicadores

        if st.session_state.get("arquivo_notificacoes") and st.session_state.get("arquivo_indicadores"):
            if st.button("⚙️ Processar Dados"):
                with st.spinner("Processando dados..."):
                    try:
                        df_validado = processador.carregar_validar(
                            st.session_state["arquivo_notificacoes"]
                        )
                        tri = st.session_state['trimestre']
                        ano = st.session_state['ano']

                        st.session_state['bloco1'] = processador.preparar_bloco1(df_validado)
                        df_atual = st.session_state['bloco1'][11]
                        df_anterior = st.session_state['bloco1'][12]

                        st.session_state['bloco2'] = processador.preparar_bloco2(df_atual, df_anterior)
                        st.session_state['bloco3'] = processador.preparar_bloco3(df_atual, df_anterior)
                        st.session_state['bloco4'] = processador.preparar_bloco4(df_atual, df_anterior)
                        st.session_state['bloco5'] = processador.preparar_bloco_setores(df_atual, df_anterior, 'Setor Responsável')
                        st.session_state['bloco6'] = processador.preparar_bloco_setores(df_atual, df_anterior, 'Local de ocorrência')

                        df_indicadores = pd.read_excel(st.session_state["arquivo_indicadores"])
                        st.session_state['bloco7_queda'] = processador.preparar_bloco7(df_atual, df_indicadores, 'Queda', tri, ano)
                        st.session_state['bloco7_lpp'] = processador.preparar_bloco7(df_atual, df_indicadores, 'Lesão de Pele', tri, ano)
                        st.session_state['bloco7_medicacao'] = processador.preparar_bloco7(df_atual, df_indicadores, 'Erro de Medicação', tri, ano)
                        st.session_state['bloco7_flebite'] = processador.preparar_bloco7(df_atual, df_indicadores, 'Flebite', tri, ano)

                        st.session_state['bloco8'] = processador.preparar_bloco8(df_validado)
                        st.session_state['bloco9'] = processador.preparar_bloco9(df_atual)
                        st.session_state['bloco10'] = processador.preparar_bloco10(df_atual)
                        st.session_state['dados_processados'] = True
                        st.success("Dados processados com sucesso.")
                    except Exception as e:
                        st.error("Erro ao processar os dados.")
                        st.code(traceback.format_exc())
    with sub5:
        if not st.session_state.get('dados_processados'):
            st.info("Processe os dados na aba 'Dados EPIMED' para visualizar os resultados.")
        else:
            resultados.exibir(st.session_state)
with aba2:
    st.write("Em desenvolvimento — Fase 3")
with aba3:
    st.write("Em desenvolvimento — Fase 5")


