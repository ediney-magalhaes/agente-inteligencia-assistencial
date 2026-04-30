import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Leitura da chave API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configuração do cliente google
genai.configure(api_key=GEMINI_API_KEY)

# Função padrão de chamada da API
def chamar_gemini(prompt):
    lista_modelos = ['gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro']
    for ia in lista_modelos:
        try:
            modelo = genai.GenerativeModel(ia)
            resposta = modelo.generate_content(prompt)
            return resposta.text
        except Exception as e:
            print(f'Modelo {ia} não disponível! Erro {e}')
    return "Todos os modelos tentados falharam na chamada! Tenta novamente."

# Função para análise do gráfico 1 (Nº notificações)
def analisar_bloco1(total_atual, total_tri_anterior, var_tri, qtde_mensal, qtde_trimestral):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas."
    instrucao = "realizar a comparação entre os meses do ano atual, os meses do ano anterior e o trimestre avaliado. Nesse" \
    "momento a análise deve focar exclusivamente na variação do número de notificações (aumento ou redução) e possíveis tendências."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS DO TRIMESTRE:
    - Total de notificações do trimestre atual: {total_atual}
    - Total de notificações do trimestre anterior: {total_tri_anterior}
    - Variação trimestral: {var_tri}
    - Quantidade mensal: {qtde_mensal}
    - Quantidade trimestral: {qtde_trimestral}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico 2 (Nº notificações por turno)
def analisar_bloco2(tabela, df_contexto_ia):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas. " \
    "Os colaboradores realizam as notificações em diversos horários e esse registro fica gravado no sistema de notificações Epimed."
    instrucao = "analisar o volume das notificações de acordo com os turnos em que foram registrados. Identificar indicíos onde" \
    "os eventos podem estar ocorrendo ou a equipe tem tempo livre para fazer registro! Utilizar a tabela com as descrições detalhadas" \
    "de cada notificação por turno e sua classificação. Usando as descrições realizadas pelos notificadores para encontrar os incidentes" \
    "de maior gravidade e ocorrência em cada turno." \
    "Analisar também o volume e a variação do número de notificações (aumento ou redução) em cada turno do trimestre atual e o anterior."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Tabela comparativa de notificações por tunos e trimestres: {tabela.to_string(index=False)}
    - Dataset com turnos, classificação e descrição das notificações: {df_contexto_ia.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico 3 (Nº notificações por classificação)
def analisar_bloco3(tabela_comparativa, df_contexto_ia):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas. " \
    "As notificações seguem a taxonomia de classificação definida pela OMS."
    instrucao = "analisar o volume e as variações das notificações do trimestre atual e anterior de acordo com as classificações. Usar a tabela de contexto" \
    "para identificar o motivo das variações segundo o grau do incidente, setor de ocorrência, turno e as descrições de cada notificação" \
    "para encontrar possíveis relações e estabelecer alguma causa e efeito."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Tabela comparativa de notificações por classificações e variação: {tabela_comparativa.to_string(index=False)}
    - Dataset com turnos, classificação, setor de ocorrência, grau dos incidentes e descrição das notificações: {df_contexto_ia.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico 3.1 a 3.7 (Nº notificações por classificação)
def analisar_top3_bloco3(dicionario, classificacao, df_contexto_ia):
    dados = dicionario[classificacao].to_string(index=False)
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas. " \
    "As notificações seguem a taxonomia de classificação definida pela OMS."
    instrucao = "analisar os três principais tipos de notificações por cada classificação e usar a tabela de contexto para compreensão dos casos."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Tabela comparativa de notificações por classificações e variação: {dados}
    - Classificação analisada: {classificacao}
    - Dataset com turnos, classificação, setor de ocorrência, grau dos incidentes e descrição das notificações: {df_contexto_ia.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico 4 (Nº eventos adversos notificados)
def analisar_bloco4(tabela_comparativa, tabela_top3_eventos, status_eventos, df_contexto_ia):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas. " \
    "As notificações seguem a taxonomia de classificação definida pela OMS."
    instrucao = "analisar o volume e as variações dos eventos adversos por grau de dano e os três principais tipos de notificações por grau." \
    "Usar o Dataset para compreender os motivos avaliando turno, setor de ocorrência, grau do dano, detalhe da classificação por Opção" \
    "assim como as descrições de cada caso."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Tabela comparativa de notificações por classificações e variação: {tabela_comparativa.to_string(index=False)}
    - Tabela com top 3 dos eventos: {tabela_top3_eventos.to_string(index=False)}
    - Dataset com status dos danos e contexto: {status_eventos.to_string(index=False)}
    - Dataset com turnos, setor de ocorrência, grau dos incidentes e descrição das notificações: {df_contexto_ia.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise dos gráficos 5 e 6 (Nº notificações por notificante e notificado)
def analisar_bloco_setores(tab_tri_atual, tab_tri_anterior, tab_analise_IA, setor):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas. " \
    "As notificações seguem a taxonomia de classificação definida pela OMS."
    instrucao = "analisar o volume de notificações por setor notificante e por setor notificado para identificar setores proativos" \
    "e locais de ocorrências dos incidentes."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Tipo de setor analisado: {setor}
    - Tabela do trimestre atual com volume de notificações por tipo de setor e variação: {tab_tri_atual.to_string(index=False)}
    - Tabela do trimestre anterior com volume de notificações por tipo de setor e variação: {tab_tri_anterior.to_string(index=False)}
    - Dataset com setor (notificante ou notificado) e a descrição das notificações: {tab_analise_IA.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico 7 (Indicadores qualidade)
def analisar_bloco7_geral(medias):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas. " \
    "As notificações seguem a taxonomia de classificação definida pela OMS."
    instrucao = "analisar o volume e variações de notificações do trimestre do ano anterior e desse ano quanto a incidência de cada" \
    "evento adverso: erro de medicação, lesão, queda e flebite."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Médias dos índices: {str(medias)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico de Queda
def analisar_bloco7_queda(qtde_grau_dano, qtde_local_queda, qtde_tipo_queda, df_indicador, df_media_tri_atual, df_media_tri_anterior):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises quantitativas" \
    "e qualitativas sobre a cultura de segurança do paciente através da ótica do número de notificações realizadas. " \
    "As notificações seguem a taxonomia de classificação definida pela OMS."
    instrucao = "analisar os casos de notificações de queda, avaliando o volume por local e tipo da queda. Utilize o " \
    "Dataset de contexto para compreender cada caso. Avalie as médias entre os trimestres e suas variações"
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Tabela grau das quedas: {qtde_grau_dano.to_string(index=False)}
    - Tabela local das quedas: {qtde_local_queda.to_string(index=False)}
    - Tabela tipo das quedas: {qtde_tipo_queda.to_string(index=False)}
    - Média do trimestre atual: {df_media_tri_atual.to_string(index=False)}
    - Média do trimestre anterior: {df_media_tri_anterior.to_string(index=False)}
    - Dataset com taxonomia, categoria, classificação, incidente, opção e descrição das notificações: {df_indicador.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico de Lesão por Pressão (LPP)
def analisar_bloco7_lpp(df_media_tri_atual, df_media_tri_anterior, df_mensal, df_indicador):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises " \
    "quantitativas e qualitativas sobre a cultura de segurança do paciente. " \
    "Lesão por Pressão (LPP) pode ser classificada como ADMITIDA — quando o paciente já chegou ao hospital com a lesão — " \
    "ou ADQUIRIDA — quando a lesão surgiu durante a internação. Apenas as lesões ADQUIRIDAS são de responsabilidade " \
    "do hospital e devem ser consideradas como indicador de qualidade assistencial."
    instrucao = "Realize a análise em duas etapas sequenciais: " \
    "ETAPA 1 — Leia cada registro do Dataset de contexto. Avalie a coluna de nota do classificador e a descrição " \
    "de cada caso para determinar se a lesão é ADMITIDA ou ADQUIRIDA. " \
    "ETAPA 2 — Com base na sua classificação da Etapa 1, analise o volume de lesões ADQUIRIDAS, " \
    "sua evolução mensal e a variação entre o trimestre atual e o anterior. " \
    "Destaque se houve aumento ou redução e aponte os casos de maior gravidade identificados nas descrições."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Média do trimestre atual: {df_media_tri_atual}
    - Média do trimestre anterior: {df_media_tri_anterior}
    - Evolução mensal do indicador: {df_mensal.to_string(index=False)}
    - Dataset com nota do classificador e descrição de cada caso: {df_indicador.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

# Função para análise do gráfico de Flebite
def analisar_bloco7_flebite(df_media_tri_atual, df_media_tri_anterior, df_mensal, df_indicador):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises " \
    "quantitativas e qualitativas sobre a cultura de segurança do paciente. " \
    "Flebite é a inflamação de uma veia, frequentemente associada à punção venosa periférica. " \
    "É um indicador de qualidade assistencial relacionado à técnica de inserção e manutenção de acessos venosos."
    instrucao = "Analise os casos de flebite notificados no trimestre. " \
    "Avalie a evolução mensal das taxas e a variação entre o trimestre atual e o anterior. " \
    "Utilize o Dataset de contexto para identificar os setores com maior ocorrência, " \
    "o grau de gravidade dos casos e possíveis padrões nas descrições que indiquem causa raiz. " \
    "Destaque se houve aumento ou redução e aponte recomendações baseadas nos padrões identificados."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Média do trimestre atual: {df_media_tri_atual}
    - Média do trimestre anterior: {df_media_tri_anterior}
    - Evolução mensal do indicador: {df_mensal.to_string(index=False)}
    - Dataset com setor, grau do incidente e descrição de cada caso: {df_indicador.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)


# Função para análise do gráfico de Erro de Medicação
def analisar_bloco7_medicacao(df_media_tri_atual, df_media_tri_anterior, df_mensal, df_indicador):
    papel = "Especialista em qualidade e segurança do paciente no ambiente hospitalar"
    contexto = "O hospital Santa Rosa possui o Núcleo de Segurança do Paciente implantado. Uma de suas atribuições é " \
    "elaborar o Relatório Trimestral de Segurança do Paciente. Esse relatório tem por objetivo trazer análises " \
    "quantitativas e qualitativas sobre a cultura de segurança do paciente. " \
    "Erro de medicação abrange toda a cadeia do medicamento — prescrição, dispensação, preparo e administração. " \
    "É um dos indicadores mais críticos de segurança do paciente pois pode causar danos diretos e imediatos."
    instrucao = "Analise os casos de erro de medicação notificados no trimestre. " \
    "Avalie a evolução mensal das taxas e a variação entre o trimestre atual e o anterior. " \
    "Utilize o Dataset de contexto para identificar em qual etapa da cadeia do medicamento os erros estão " \
    "concentrados — armazenamento, recebimento, prescrição, dispensação, preparo ou administração — e os setores mais afetados. " \
    "Identifique padrões nas descrições que indiquem causa raiz e destaque casos de maior gravidade. " \
    "Aponte recomendações focadas na etapa da cadeia com maior concentração de erros."
    prompt = f"""
    Você é {papel}.

    CONTEXTO:
    {contexto}

    DADOS:
    - Média do trimestre atual: {df_media_tri_atual}
    - Média do trimestre anterior: {df_media_tri_anterior}
    - Evolução mensal do indicador: {df_mensal.to_string(index=False)}
    - Dataset com setor, grau do incidente e descrição de cada caso: {df_indicador.to_string(index=False)}

    INSTRUÇÃO:
    {instrucao}
    """
    return chamar_gemini(prompt)

