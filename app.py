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
    sub1, sub2, sub3, sub4, sub5 = st.tabs(["⚙️ Configuração", "📁 Dados EPIMED", "🖼️ Imagens", "📝 Inserir Dados", "📄 Resultados"])
    with sub1:
        st.write("Configuração")
        st.session_state['trimestre'] = st.selectbox("Trimestre", [1, 2, 3, 4])
        st.session_state['ano'] = st.number_input("Ano", min_value=2020, max_value=2030)
        st.session_state['hospital'] = st.text_input("Nome do Hospital")
    with sub2:
        st.write("Dados")
        st.session_state["arquivo_notificacoes"] = st.file_uploader("Planilha de Notificações", type=["xlsx"])
        st.session_state["arquivo_indicadores"] = st.file_uploader("Planilha de Indicadores", type=["xlsx"])
        if st.session_state["arquivo_notificacoes"] and st.session_state["arquivo_indicadores"]:
            if st.button("⚙️ Processar Dados"):
                with st.spinner("Processando dados..."):
                    try:
                        df_validado = processador.carregar_validar(
                            st.session_state["arquivo_notificacoes"]
                        )
                        st.session_state['bloco1'] = processador.preparar_bloco1(df_validado)
                        st.session_state['bloco2'] = processador.preparar_bloco2(df_validado)
                        st.session_state['bloco3'] = processador.preparar_bloco3(df_validado)
                        st.session_state['bloco4'] = processador.preparar_bloco4(df_validado)
                        st.session_state['bloco5'] = processador.preparar_bloco_setores(df_validado, 'notificante')
                        st.session_state['bloco6'] = processador.preparar_bloco_setores(df_validado, 'notificado')
                        st.session_state['bloco7'] = processador.preparar_bloco7(df_validado, st.session_state["arquivo_indicadores"])
                        st.session_state['bloco8'] = processador.preparar_bloco8(df_validado)
                        st.session_state['bloco9'] = processador.preparar_bloco9(df_validado)
                        st.session_state['bloco10'] = processador.preparar_bloco10(df_validado)
                        st.session_state['dados_processados'] = True
                        st.success("Dados processados com sucesso.")
                    except Exception as e:
                        st.error("Erro ao processar os dados.")
                        st.code(traceback.format_exc())
    with sub3:
        st.write("Upload gráficos")
        st.session_state["img_grafico2"] = st.file_uploader("Gráfico do Turno das Notificações", type=["png", "jpg", "jpeg"])
        st.session_state["img_grafico4_2"] = st.file_uploader("Gráfico da Gravidade dos Incidentes", type=["png", "jpg", "jpeg"])
        st.session_state["img_grafico5"] = st.file_uploader("Gráfico dos Setores Notificantes", type=["png", "jpg", "jpeg"])
        st.session_state["img_grafico6"] = st.file_uploader("Gráfico dos Setores Notificados", type=["png", "jpg", "jpeg"])
        st.session_state["img_grafico9"] = st.file_uploader("Gráfico da Auditoria de ROPs", type=["png", "jpg", "jpeg"])
        st.session_state["img_grafico10"] = st.file_uploader("Gráfico da Comissão de Prontuário", type=["png", "jpg", "jpeg"])
    with sub4:
        st.write("Input de dados")
        st.session_state['texto_obitos'] = st.text_area("Comissão de Óbitos", height=150)
        st.session_state['texto_prontuarios'] = st.text_area("Comissão de Prontuários", height=150)
        st.session_state['arquivo_psp'] = st.file_uploader("Plano de Segurança do Paciente (importar tabela)", type=["xlsx"])
        st.markdown("**Ações Táticas e Estratégicas**")
        if 'acoes_taticas' not in st.session_state:
            st.session_state['acoes_taticas'] = []
        if st.button("+ Adicionar Ação"):
            st.session_state['acoes_taticas'].append({"acao": '', "status": '', "responsavel": ''})
        for i, item in enumerate(st.session_state['acoes_taticas']):
            col1, col2, col3 = st.columns(3)
            with col1:
                item['acao'] = st.text_input("Ação", value=item['acao'], key=f"acao_{i}")
            with col2:
                item['status'] = st.text_input("Status", value=item['status'], key=f"status_{i}")
            with col3:
                item['responsavel'] = st.text_input("Responsável", value=item['responsavel'], key=f"responsavel_{i}")
    with sub5:
        if not st.session_state.get('dados_processados'):
            st.info("Processe os dados na aba 'Dados EPIMED' para visualizar os resultados.")
        else:
            resultados.exibir(st.session_state)
with aba2:
    st.write("Em desenvolvimento — Fase 3")
with aba3:
    st.write("Em desenvolvimento — Fase 5")


