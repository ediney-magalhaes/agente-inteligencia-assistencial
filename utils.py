#---------------------------------------------------
# Script que guarda as funções auxiliares do sistema
# Criado por: Ediney Magalhães
# Data: 17/04/2026
#---------------------------------------------------

# Constantes
COL_DATA = 'Data da notificação'
COL_CLASSIFICACAO = 'Classificação da Notificação'
COL_STATUS = 'Status da notificação'
COL_PL = 'Unidade responsável pela investigação - PL'
COL_ACR = 'Unidade responsável pela investigação - ACR'
COL_PAC = 'Unidade responsável pela investigação - PAC'
COL_CAT = 'Categoria do incidente'
COL_INCIDENTE = 'Incidente'
COL_TIPO_SETOR = 'Assistencial/ Administrativo/ Apoio'
COL_EFETIVO = 'Escala de Efetividade'
COL_DESCRICAO = 'Descrição do incidente'
COL_TAXON = 'Taxonomia da OMS'
COL_SETOR = 'Setor Responsável'
COL_GRAU = 'Grau do dano'
COL_OPCAO = 'Opção'
COL_TURNO = 'Turno'

# Mapeamento das colunas
MAPEAMENTO_COLUNAS = {
    COL_DATA: [],
    COL_CLASSIFICACAO: [],
    COL_TAXON: ['Taxonomia'],
    COL_SETOR: ['Responsável'],
    COL_GRAU: [],
    COL_CAT: [],
    COL_INCIDENTE: [],
    COL_OPCAO: [],
    COL_TURNO: [],
    COL_DESCRICAO: [],
    COL_TIPO_SETOR: [],
    COL_PL: [],
    COL_ACR: [],
    COL_PAC: [],
    COL_STATUS: [],
    COL_EFETIVO: []
}

# Função para atualizar colunas conforme dataframe
def atualizacao_schema(df):
    lista = []

    for nome, alternativa in MAPEAMENTO_COLUNAS.items():
        if nome in df.columns:
            pass
        else:
            for i in alternativa:
                if i in df.columns:
                    df.rename(columns= {i:nome},inplace=True)
                    break
            else:
                lista.append(nome)
    return df, lista

# Função para cálculo da variação de notificações em relação ao trimestre anterior
def texto_variacao(valor):
    if valor > 0: return f"um aumento de {valor:.1f}%"
    elif valor < 0: return f"uma redução de {abs(valor):.1f}%" 
    else: return "uma estabilidade"


# Denominador: Foi encaminhada para tratar?
def tem_investigacao(row):
    pl = str(row[COL_PL]).strip().lower()
    acr = str(row[COL_ACR]).strip().lower()
    pac = str(row[COL_PAC]).strip().lower()
    invalidos = ['nan', '-', '', 'nat', 'none']
    return (pl not in invalidos) or (acr not in invalidos) or (pac not in invalidos)


# Numerador: Foi realmente concluída?
def foi_tratada(row):
    status = str(row[COL_STATUS]).strip().lower()
    return ('validado' in status) or ('concluído após a investigação' in status)

# Estatísticas de Ferramentas (PL, ACR, PAC)
def check_tool(row, col_name):
    return str(row[col_name]).strip().lower() not in ['nan', '-', '', 'nat', 'none']