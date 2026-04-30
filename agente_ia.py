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