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
    return "Todos os modelos tentados falharam na chamada!"