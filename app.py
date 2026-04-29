import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Sistema de Inteligência Assistencial", layout="wide")

# Renderizar título principal da página
st.title("🏥Sistema de Inteligência Assistencial")

# Criar abas de navegação
aba1, aba2, aba3 = st.tabs(["📋 Relatório", "📊 Painel Epidemiológico", "🤖 Agente IA"])
with aba1:
    sub1, sub2, sub3, sub4, sub5 = st.tabs(["⚙️ Configuração", "📁 Dados EPIMED", "🖼️ Imagens", "📝 Inserir Dados", "📄 Gerar Relatório"])
    with sub1:
        st.write("Configuração")
        st.session_state['trimestre'] = st.selectbox("Trimestre", [1, 2, 3, 4])
        st.session_state['ano'] = st.number_input("Ano", min_value=2020, max_value=2030)
        st.session_state['hospital'] = st.text_input("Nome do Hospital")
    with sub2:
        st.write("Dados")
        st.session_state["arquivo_notificacoes"] = st.file_uploader("Planilha de Notificações", type=["xlsx"])
        st.session_state["arquivo_indicadores"] = st.file_uploader("Planilha de Indicadores", type=["xlsx"])
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
        st.write("Produzir documento")
        st.info(f"Trimestre: {st.session_state['trimestre']} | Ano: {st.session_state['ano']} | Hospital: {st.session_state['hospital']}")
        if st.button("📄 Gerar Relatório"):
            st.warning("Gerador ainda não implementado")
with aba2:
    st.write("Em desenvolvimento — Fase 3")
with aba3:
    st.write("Em desenvolvimento — Fase 5")


