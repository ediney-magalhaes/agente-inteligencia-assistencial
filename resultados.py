import streamlit as st
import visualizador
import agente_ia


def exibir(session_state):
    tri = session_state['trimestre']
    ano = session_state['ano']

    # Gráfico 1 — Quantidade de Notificações
    st.markdown("## Gráfico 1 — Quantidade de Notificações")
    b1 = session_state['bloco1']
    st.pyplot(visualizador.grafico_volume_notificacoes(b1[3], b1[4], b1[7], b1[8]))
    if st.button("🤖 Gerar Análise IA — Gráfico 1", key="btn_ia_b1"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b1'] = agente_ia.analisar_bloco1(b1[0], b1[1], b1[5], b1[3], b1[4])
    if 'ia_b1' in st.session_state:
        st.write(st.session_state['ia_b1'])
    st.divider()

    # Gráfico 2 — Turno
    st.markdown("## Gráfico 2 — Turno de Maior Notificação")
    if session_state.get("img_grafico2"):
        st.image(session_state["img_grafico2"], caption="Fonte: EPIMED")
    b2 = session_state['bloco2']
    st.dataframe(b2[0])
    if st.button("🤖 Gerar Análise IA — Gráfico 2", key="btn_ia_b2"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b2'] = agente_ia.analisar_bloco2(b2[0], b2[1])
    if 'ia_b2' in st.session_state:
        st.write(st.session_state['ia_b2'])
    st.divider()

    # Gráfico 3 — Classificação
    st.markdown("## Gráfico 3 — Classificação das Notificações")
    b3 = session_state['bloco3']
    st.pyplot(visualizador.grafico_classificacoes(b3[0], tri, ano))
    st.markdown("### Top 3 por Subcategoria")
    ordem_classificacoes = [
        'Incidente (circunstância de risco ou condições inseguras)',
        'Near miss',
        'Incidente sem dano',
        'Never event/Evento sentinela (ANVISA/JCI)',
        'Queixa técnica',
        'Segurança do Trabalho',
        'Outra natureza'
    ]
    for classificacao in ordem_classificacoes:
        if classificacao in b3[1]:
            st.markdown(f"**{classificacao}**")
            st.pyplot(visualizador.gerar_grafico_top3(b3[1], classificacao))
    if st.button("🤖 Gerar Análise IA — Gráfico 3", key="btn_ia_b3"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b3'] = agente_ia.analisar_bloco3(b3[0], b3[2])
    if 'ia_b3' in st.session_state:
        st.write(st.session_state['ia_b3'])
    st.divider()

    # Gráfico 4 — Eventos Adversos
    st.markdown("## Gráfico 4.1 — Top 3 Eventos Adversos")
    b4 = session_state['bloco4']
    st.pyplot(visualizador.gerar_grafico_bloco4_1(b4[1]))
    st.dataframe(b4[0])
    if b4[2] is not None and not b4[2].empty:
        st.markdown("**Eventos Graves e Óbitos**")
        st.dataframe(b4[2])
    st.markdown("### 4.2 — Grau do Dano")
    if session_state.get("img_grafico4_2"):
        st.image(session_state["img_grafico4_2"], caption="Fonte: EPIMED")
    if st.button("🤖 Gerar Análise IA — Gráfico 4", key="btn_ia_b4"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b4'] = agente_ia.analisar_bloco4(b4[0], b4[1], b4[2], b4[3])
    if 'ia_b4' in st.session_state:
        st.write(st.session_state['ia_b4'])
    st.divider()

    # Gráfico 5 — Setores Notificantes
    st.markdown("## Gráfico 5 — Setores Notificantes")
    if session_state.get("img_grafico5"):
        st.image(session_state["img_grafico5"], caption="Fonte: EPIMED")
    b5 = session_state['bloco5']
    st.dataframe(b5[0])
    st.dataframe(b5[1])
    if st.button("🤖 Gerar Análise IA — Gráfico 5", key="btn_ia_b5"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b5'] = agente_ia.analisar_bloco_setores(b5[0], b5[1], b5[2], "notificantes")
    if 'ia_b5' in st.session_state:
        st.write(st.session_state['ia_b5'])
    st.divider()

    # Gráfico 6 — Setores Notificados
    st.markdown("## Gráfico 6 — Setores Notificados")
    if session_state.get("img_grafico6"):
        st.image(session_state["img_grafico6"], caption="Fonte: EPIMED")
    b6 = session_state['bloco6']
    st.dataframe(b6[0])
    st.dataframe(b6[1])
    if st.button("🤖 Gerar Análise IA — Gráfico 6", key="btn_ia_b6"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b6'] = agente_ia.analisar_bloco_setores(b6[0], b6[1], b6[2], "notificados")
    if 'ia_b6' in st.session_state:
        st.write(st.session_state['ia_b6'])
    st.divider()

    # Gráfico 7 — Índices de Qualidade
    medias = {
        "Erro de Medicação": (session_state['bloco7_medicacao'][2], session_state['bloco7_medicacao'][3]),
        "Lesão de Pele": (session_state['bloco7_lpp'][2], session_state['bloco7_lpp'][3]),
        "Flebite": (session_state['bloco7_flebite'][2], session_state['bloco7_flebite'][3]),
        "Queda": (session_state['bloco7_queda'][2], session_state['bloco7_queda'][3])
    }
    st.pyplot(visualizador.gerar_grafico_bloco7_geral(medias, {}))
    st.markdown("## Gráfico 7 — Índices de Qualidade")

    st.markdown("### Queda")
    b7q = session_state['bloco7_queda']
    st.pyplot(visualizador.gerar_grafico_bloco7(b7q[0], b7q[1], "Queda", tri, ano))
    if st.button("🤖 Gerar Análise IA — Queda", key="btn_ia_b7q"):
        with st.spinner("Analisando..."):
            ctx = b7q[4]
            st.session_state['ia_b7q'] = agente_ia.analisar_bloco7_queda(ctx[0], ctx[1], ctx[2], b7q[0], b7q[2], b7q[3])
    if 'ia_b7q' in st.session_state:
        st.write(st.session_state['ia_b7q'])

    st.markdown("### Lesão por Pressão")
    b7l = session_state['bloco7_lpp']
    st.pyplot(visualizador.gerar_grafico_bloco7(b7l[0], b7l[1], "Lesão de Pele", tri, ano))
    if st.button("🤖 Gerar Análise IA — LPP", key="btn_ia_b7l"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b7l'] = agente_ia.analisar_bloco7_lpp(b7l[2], b7l[3], b7l[0], b7l[4])
    if 'ia_b7l' in st.session_state:
        st.write(st.session_state['ia_b7l'])

    st.markdown("### Erro de Medicação")
    b7m = session_state['bloco7_medicacao']
    st.pyplot(visualizador.gerar_grafico_bloco7(b7m[0], b7m[1], "Erro de Medicação", tri, ano))
    if st.button("🤖 Gerar Análise IA — Erro de Medicação", key="btn_ia_b7m"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b7m'] = agente_ia.analisar_bloco7_medicacao(b7m[2], b7m[3], b7m[0], b7m[4])
    if 'ia_b7m' in st.session_state:
        st.write(st.session_state['ia_b7m'])

    st.markdown("### Flebite")
    b7f = session_state['bloco7_flebite']
    st.pyplot(visualizador.gerar_grafico_bloco7(b7f[0], b7f[1], "Flebite", tri, ano))
    if st.button("🤖 Gerar Análise IA — Flebite", key="btn_ia_b7f"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b7f'] = agente_ia.analisar_bloco7_flebite(b7f[2], b7f[3], b7f[0], b7f[4])
    if 'ia_b7f' in st.session_state:
        st.write(st.session_state['ia_b7f'])
    st.divider()

    # Gráfico 8 — Cumprimento de Análises
    st.markdown("## Gráfico 8 — Cumprimento de Análises")
    b8 = session_state['bloco8']
    st.pyplot(visualizador.gerar_grafico_bloco8(b8[0], b8[1], b8[2], b8[3], ano))
    if st.button("🤖 Gerar Análise IA — Gráfico 8", key="btn_ia_b8"):
        with st.spinner("Analisando..."):
            st.session_state['ia_b8'] = agente_ia.analisar_bloco8(b8[0], b8[1], b8[2], b8[3], b8[4])
    if 'ia_b8' in st.session_state:
        st.write(st.session_state['ia_b8'])
    st.divider()

    # Seção 5 — Protocolos Gerenciados
    st.markdown("## Seção 5 — Protocolos Gerenciados")
    if 'bloco9' in session_state:
        if st.button("🤖 Gerar Análise IA — Protocolos", key="btn_ia_b9"):
            with st.spinner("Analisando..."):
                st.session_state['ia_b9'] = agente_ia.analisar_bloco9(session_state['bloco9'])
        if 'ia_b9' in st.session_state:
            st.write(st.session_state['ia_b9'])
    st.divider()

    # Seção 10 — Interrelação
    st.markdown("## Seção 10 — Interrelação e Mapeamento de Risco")
    if 'bloco10' in session_state:
        if st.button("🤖 Gerar Análise IA — Interrelação", key="btn_ia_b10"):
            with st.spinner("Analisando..."):
                b10 = session_state['bloco10']
                st.session_state['ia_b10'] = agente_ia.analisar_interrelacao(b10[0], tri, ano, b10[1])
        if 'ia_b10' in st.session_state:
            st.write(st.session_state['ia_b10'])