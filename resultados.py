import streamlit as st
import visualizador
import agente_ia


def _exibir_bloco(titulo, chave_dados, chave_ia, fn_grafico, fn_ia, session_state, imagem=None):
    st.markdown(f"## {titulo}")
    if imagem and session_state.get(imagem):
        st.image(session_state[imagem], caption="Fonte: EPIMED")
    dados = session_state[chave_dados]
    fig = fn_grafico(dados) if fn_grafico else None
    if fig:
        st.pyplot(fig)
    st.divider()
    if st.button(f"🤖 Gerar Análise IA — {titulo}", key=f"ia_{chave_dados}"):
        with st.spinner("Analisando..."):
            st.session_state[chave_ia] = fn_ia(dados)
    if chave_ia in st.session_state:
        st.write(st.session_state[chave_ia])
    st.divider()


def exibir(session_state):
    _exibir_bloco("Gráfico 1 — Quantidade de Notificações", 'bloco1', 'ia_bloco1', visualizador.gerar_grafico_bloco1, agente_ia.analisar_bloco1, session_state)
    _exibir_bloco("Gráfico 2 — Turno", 'bloco2', 'ia_bloco2', None, agente_ia.analisar_bloco2, session_state, imagem='img_grafico2')
    _exibir_bloco("Gráfico 3 — Classificação", 'bloco3', 'ia_bloco3', visualizador.gerar_grafico_bloco3, agente_ia.analisar_bloco3, session_state)
    _exibir_bloco("Gráfico 4 — Eventos Adversos", 'bloco4', 'ia_bloco4', visualizador.gerar_grafico_bloco4, agente_ia.analisar_bloco4, session_state, imagem='img_grafico4_2')
    _exibir_bloco("Gráfico 5 — Setores Notificantes", 'bloco5', 'ia_bloco5', None, agente_ia.analisar_bloco_setores, session_state, imagem='img_grafico5')
    _exibir_bloco("Gráfico 6 — Setores Notificados", 'bloco6', 'ia_bloco6', None, agente_ia.analisar_bloco_setores, session_state, imagem='img_grafico6')
    _exibir_bloco("Gráfico 7 — Índices de Qualidade", 'bloco7', 'ia_bloco7', visualizador.gerar_grafico_bloco7, agente_ia.analisar_bloco7, session_state)
    _exibir_bloco("Gráfico 8 — Cumprimento de Análises", 'bloco8', 'ia_bloco8', visualizador.gerar_grafico_bloco8, agente_ia.analisar_bloco8, session_state)
    _exibir_bloco("Seção 5 — Protocolos Gerenciados", 'bloco9', 'ia_bloco9', None, agente_ia.analisar_bloco9, session_state)
    _exibir_bloco("Seção 10 — Interrelação e Mapeamento de Risco", 'bloco10', 'ia_bloco10', None, agente_ia.analisar_interrelacao, session_state)