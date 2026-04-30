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