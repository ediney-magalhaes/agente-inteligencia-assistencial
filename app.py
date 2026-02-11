import streamlit as st
import pandas as pd
import google.generativeai as genai
import motor_analise as motor 

# ==========================================
# CONFIGURAÇÃO DA PÁGINA E MENU LATERAL
# ==========================================
st.set_page_config(page_title="Agente - Segurança do Paciente", layout="wide")

st.sidebar.title("⚙️ Configurações Iniciais")
st.sidebar.write("Insira sua chave da API do Google Gemini para habilitar análises em texto.")
api_key_usuario = st.sidebar.text_input("Chave API (Gemini)", type="password")

if api_key_usuario:
    genai.configure(api_key=api_key_usuario)
    st.sidebar.success("✅ Chave API configurada!")

st.sidebar.markdown("---")
st.sidebar.title("🏥 Dados Hospitalares (Censo)")
st.sidebar.write("Insira os dias-paciente para o cálculo de densidade do Bloco 5:")
pacientes_dia_atual = st.sidebar.number_input("Pacientes-dia (Ano Atual)", min_value=0, value=0)
pacientes_dia_anterior = st.sidebar.number_input("Pacientes-dia (Ano Anterior)", min_value=0, value=0)

st.sidebar.markdown("---")
st.sidebar.title("📂 Bases Auxiliares")
arquivo_setores = st.sidebar.file_uploader("1. Carregar 'tabela_setores.xlsx' (Blocos 6 a 8)", type=["xlsx", "csv"])
arquivo_indicadores = st.sidebar.file_uploader("2. Carregar 'indicadores.xlsx' (Bloco 9)", type=["xlsx", "csv"])

# ==========================================
# INTERFACE VISUAL DO STREAMLIT (A Tela)
# ==========================================
st.title("🏥 Agente de Análise - Segurança do Paciente")
st.write("Faça o upload da base de dados de incidentes para gerar a análise.")

arquivo_carregado = st.file_uploader("Carregue a base de dados principal (Notificações)", type=["xlsx", "csv"])

if arquivo_carregado is not None:
    st.success("Arquivo de notificações carregado com sucesso!")
    if arquivo_carregado.name.endswith('.csv'): 
        df_usuario = pd.read_csv(arquivo_carregado)
    else: 
        df_usuario = pd.read_excel(arquivo_carregado)
        
    if 'Data da notificação' not in df_usuario.columns:
        st.error("ERRO: Colunas necessárias não encontradas na planilha principal.")
    else:
        # --- BLOCO 1 ---
        st.subheader("📝 Bloco 1: Visão Geral")
        st.info(motor.analisar_bloco_1(df_usuario))
        
        # --- BLOCO 2 ---
        st.subheader("📊 Bloco 2: Gráfico Comparativo Anual")
        st.pyplot(motor.gerar_grafico_bloco_2(df_usuario))
        st.divider()
        
        # --- BLOCO 3 ---
        st.subheader("📊 Bloco 3: Análise por Classificação da Notificação")
        st.pyplot(motor.gerar_grafico_bloco_3(df_usuario))
        if api_key_usuario:
            if st.button("🤖 Gerar Análise com IA (Bloco 3)"):
                with st.spinner('Gerando análise...'): 
                    st.session_state['texto_bloco_3'] = motor.gerar_analise_ia_bloco_3(df_usuario, api_key_usuario)
            if 'texto_bloco_3' in st.session_state: 
                st.write(st.session_state['texto_bloco_3'])
        st.divider()

        # --- BLOCO 4 ---
        st.subheader("📋 Bloco 4: Tabela Comparativa e Raio-X de Turnos")
        tabela_comp, df_turnos, df_atual_completo, vilao_g, t_atual, a_atual, a_ant = motor.preparar_dados_bloco_4(df_usuario)
        col1, col2 = st.columns(2)
        with col1: st.dataframe(tabela_comp, use_container_width=True)
        with col2: st.dataframe(df_turnos, use_container_width=True)
        
        if api_key_usuario:
            if st.button("🤖 Gerar Análise com IA (Bloco 4)"):
                with st.spinner('Gerando análise...'): 
                    st.session_state['texto_bloco_4'] = motor.gerar_analise_ia_bloco_4(tabela_comp, df_turnos, df_atual_completo, vilao_g, t_atual, a_atual, a_ant)
            if 'texto_bloco_4' in st.session_state: 
                st.write(st.session_state['texto_bloco_4'])
        st.divider()

        # --- BLOCO 5 ---
        st.subheader("⚠️ Bloco 5: Gravidade do Dano e Taxonomia OMS")
        tab_gravidade, tab_taxonomia, dens_atual, dens_ant, tot_ea, df_atual_b5, tri_b5, ano_b5, ano_ant_b5 = motor.preparar_dados_bloco_5(df_usuario, pacientes_dia_atual, pacientes_dia_anterior)
        
        st.markdown(f"**Indicador de Qualidade:** Densidade de {dens_atual:.2f} incidentes por 1.000 pacientes/dia (Anterior: {dens_ant:.2f}).")
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"**Tabela 2: Gravidade do Dano ({tri_b5}º Tri {ano_b5})**")
            st.dataframe(tab_gravidade, use_container_width=True)
        with col4:
            st.markdown(f"**Tabela 3: Top Taxonomia OMS ({tri_b5}º Tri {ano_b5})**")
            st.dataframe(tab_taxonomia.head(10), use_container_width=True)
            
        if api_key_usuario:
            if st.button("🤖 Gerar Análise com IA (Bloco 5)"):
                with st.spinner('A IA está lendo a gravidade, a taxonomia e as descrições...'):
                    st.session_state['texto_bloco_5'] = motor.gerar_analise_ia_bloco_5(tab_gravidade, tab_taxonomia, dens_atual, dens_ant, tot_ea, df_atual_b5, tri_b5, ano_b5, ano_ant_b5)
            if 'texto_bloco_5' in st.session_state: 
                st.write(st.session_state['texto_bloco_5'])
        st.divider()

        # --- BLOCOS 6 E 7 E 8 ---
        st.subheader("🏥 Mapeamento de Setores (Assistencial, Administrativo e Apoio)")
        if arquivo_setores is not None:
            if arquivo_setores.name.endswith('.csv'): df_setores_usuario = pd.read_csv(arquivo_setores)
            else: df_setores_usuario = pd.read_excel(arquivo_setores)
            
            if 'Setor' not in df_setores_usuario.columns or 'Assistencial/ Administrativo/ Apoio' not in df_setores_usuario.columns:
                st.error("ERRO: A tabela de setores deve conter as colunas 'Setor' e 'Assistencial/ Administrativo/ Apoio'.")
            else:
                # BLOCO 6
                st.markdown("### Bloco 6: Setores Assistenciais")
                df_assistencial, tri_b6, ano_b6 = motor.preparar_dados_bloco_6(df_usuario, df_setores_usuario)
                st.pyplot(motor.gerar_grafico_bloco_6(df_assistencial, tri_b6, ano_b6))
                if api_key_usuario:
                    if st.button("🤖 Gerar Análise com IA (Bloco 6)"):
                        with st.spinner('Analisando setores assistenciais...'):
                            st.session_state['texto_bloco_6'] = motor.gerar_analise_ia_bloco_6(df_assistencial, tri_b6, ano_b6)
                    if 'texto_bloco_6' in st.session_state: st.write(st.session_state['texto_bloco_6'])
                
                st.divider()
                
                # BLOCO 7
                st.markdown("### Bloco 7: Setores Administrativos")
                df_administrativo, total_institucional, tri_b7, ano_b7 = motor.preparar_dados_bloco_7(df_usuario, df_setores_usuario)
                if not df_administrativo.empty:
                    st.pyplot(motor.gerar_grafico_bloco_7(df_administrativo, tri_b7, ano_b7))
                    if api_key_usuario:
                        if st.button("🤖 Gerar Análise com IA (Bloco 7)"):
                            with st.spinner('Analisando setores administrativos...'):
                                st.session_state['texto_bloco_7'] = motor.gerar_analise_ia_bloco_7(df_administrativo, total_institucional, tri_b7, ano_b7)
                        if 'texto_bloco_7' in st.session_state: st.write(st.session_state['texto_bloco_7'])
                else:
                    st.info("Nenhuma notificação para Áreas Administrativas.")
                    
                st.divider()
                
                # BLOCO 8
                st.markdown("### Bloco 8: Setores de Apoio")
                df_apoio, total_institucional, tri_b8, ano_b8 = motor.preparar_dados_bloco_8(df_usuario, df_setores_usuario)
                if not df_apoio.empty:
                    st.pyplot(motor.gerar_grafico_bloco_8(df_apoio, tri_b8, ano_b8))
                    if api_key_usuario:
                        if st.button("🤖 Gerar Análise com IA (Bloco 8)"):
                            with st.spinner('Analisando setores de apoio...'):
                                st.session_state['texto_bloco_8'] = motor.gerar_analise_ia_bloco_8(df_apoio, total_institucional, tri_b8, ano_b8)
                        if 'texto_bloco_8' in st.session_state: st.write(st.session_state['texto_bloco_8'])
                else:
                    st.info("Nenhuma notificação para Áreas de Apoio.")
                    
        else:
            st.warning("⚠️ Faça o upload da 'tabela_setores.xlsx' no menu lateral para visualizar os Blocos 6, 7 e 8.")

        st.divider()

        # --- BLOCO 9 ---
        st.subheader("📈 Bloco 9: Indicadores de Qualidade (Série Histórica)")
        if arquivo_indicadores is not None:
            df_grafico_b9, ano_ini_b9, tri_b9, ano_b9, descricoes_b9 = motor.preparar_dados_bloco_9(arquivo_indicadores, df_usuario)
            
            st.pyplot(motor.gerar_grafico_bloco_9(df_grafico_b9, ano_ini_b9, tri_b9, ano_b9))
            
            if api_key_usuario:
                if st.button("🤖 Gerar Análise com IA (Bloco 9)"):
                    with st.spinner('Analisando tendências, picos e descrições dos incidentes...'):
                        st.session_state['texto_bloco_9'] = motor.gerar_analise_ia_bloco_9(df_grafico_b9, tri_b9, ano_b9, descricoes_b9)
                if 'texto_bloco_9' in st.session_state:
                    st.success("Análise de Indicadores concluída:")
                    st.write(st.session_state['texto_bloco_9'])
        else:
            st.warning("⚠️ Faça o upload da planilha 'indicadores.xlsx' no menu lateral para gerar o gráfico histórico.")
        
        # --- BLOCO 10 ---
        st.subheader("🎯 Bloco 10: Cumprimento das Análises e Tratativas")
        resumo_anos_b10, resumo_mensal_b10, ano_atual_b10, tri_atual_b10, tot_rec_tri, tot_trat_tri, taxa_tri, stats_ferramentas, distribuicao_notas, descricoes_b10 = motor.preparar_dados_bloco_10(df_usuario)
        
        st.pyplot(motor.gerar_grafico_bloco_10(resumo_anos_b10, resumo_mensal_b10, ano_atual_b10, tri_atual_b10))
        
        if api_key_usuario:
            if st.button("🤖 Gerar Análise com IA (Bloco 10)"):
                with st.spinner('A IA está avaliando as ferramentas (ACR, PL, PAC) e cruzando com a eficácia das ações...'):
                    st.session_state['texto_bloco_10'] = motor.gerar_analise_ia_bloco_10(
                        resumo_anos_b10, ano_atual_b10, tri_atual_b10, tot_rec_tri, tot_trat_tri, taxa_tri, stats_ferramentas, distribuicao_notas, descricoes_b10
                    )
            if 'texto_bloco_10' in st.session_state:
                st.success("Análise de Tratativas e Ferramentas concluída:")
                st.write(st.session_state['texto_bloco_10'])
        st.divider()

        # --- BLOCO 11 ---
        st.subheader("🧠 Bloco 11: Mapeamento de Risco da Instituição (HFMEA & Ishikawa)")
        st.write("Análise preditiva baseada nas descrições clínicas dos incidentes do trimestre atual.")

        if api_key_usuario:
            if st.button("🤖 Gerar Mapeamento de Risco com IA (Bloco 11)"):
                with st.spinner('A IA está varrendo os relatos para extrair agrupamentos de risco e montar a tabela de Ishikawa...'):
                    resumo_riscos_b11, tot_notif_b11, tri_b11, ano_b11 = motor.preparar_dados_bloco_11(df_usuario)
                    st.session_state['texto_bloco_11'] = motor.gerar_analise_ia_bloco_11(resumo_riscos_b11, tot_notif_b11, tri_b11, ano_b11)
            
            if 'texto_bloco_11' in st.session_state:
                st.success("Matriz de Risco e Fatores de Ishikawa concluídos com sucesso:")
                st.write(st.session_state['texto_bloco_11'])
        else:
            st.warning("⚠️ Insira a Chave API do Gemini no menu lateral para gerar o mapeamento preditivo de riscos.")
            
        st.divider()
        st.markdown("<h4 style='text-align: center; color: #1f4e79;'>🏁 Relatório Executivo Concluído!</h4>", unsafe_allow_html=True)