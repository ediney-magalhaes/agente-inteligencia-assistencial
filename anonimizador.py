#---------------------------------------------------
# Script que realiza a anonimização dos dados pessoais
# Criado por: Ediney Magalhães
# Data: 13/10/2026
#---------------------------------------------------

import re
import spacy
import logging

logger = logging.getLogger(__name__)

# carrega modelo
NLP = spacy.load('pt_core_news_sm')

# constantes
PADRAO_CPF = r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}'
PADRAO_TELEFONE = r'\(?\d{2}\)? ?9?\d{4}-?\d{4}'
PADRAO_EMAIL = r'[\w.+-]+@[\w-]+\.[\w.]+'
PADRAO_NUMERO = r'\d{6,}|\d{4}-\d{4}'

# gatilhos de 'pronomes' para nomes de pessoas
GATILHOS = [
    'filh[oa]',
    'espos[oa]',
    'marido',
    'm[ãa]e',
    'pai',
    'irm[ãa]o?',
    'net[oa]',
    'cuidadora?',
    'acompanhante',
    'dra?',
    'doutora?',
    'enfermeir[oa]',
    't[eé]cnic[oa]',
    'sra?',
]

# lista de palavras 'pré' nomes
PALAVRAS_COMUNS = [
    'que', 'de', 'da', 'do', 'das', 'dos', 'e', 'a', 'o',
    'com', 'sem', 'em', 'na', 'no', 'para', 'por', 'ao',
    'foi', 'est[aá]', 'estava', 'n[aã]o',
    'informou', 'relatou', 'disse', 'referiu',
    'mas', 'ou', 'porém', 'se', 'como', 'mais', 'muito',
    'também', 'já', 'ainda', 'um', 'uma', 'aos', 'às', 'nos',
    'nas', 'pelo', 'pela', 'pelos', 'pelas', 'sobre', 'entre',
    'até', 'após', 'quando', 'onde', 'tem', 'teve', 'era', 'ficou',
]

#
NAO_COMUM = r'(?!(?:' + '|'.join(PALAVRAS_COMUNS) + r')\b)'

# idenfiticação de nomes nas frases
PADRAO_NOME = r'\b(?:' + '|'.join(GATILHOS) + r')\b' + r'\.?' + r'\s+' + NAO_COMUM + r'\w+' + r'(?:\s+' + NAO_COMUM + r'\w+)?'

# camadas regex
CAMADAS = [
    (PADRAO_CPF, '[CPF]'),
    (PADRAO_TELEFONE, '[TELEFONE]'),
    (PADRAO_EMAIL, '[EMAIL]'),
    (PADRAO_NUMERO, '[NUMERO]'),
    (PADRAO_NOME, '[NOME]')
]

# função para anonimização 
def anonimizar_texto(texto, origem='não informada'):
    contagem = {}
    for padrao, rotulo in CAMADAS:
        texto, qtde = re.subn(padrao, rotulo, texto, flags=re.IGNORECASE)
        contagem[rotulo] = qtde
    trechos = localizar_nomes(texto)
    for inicio, fim in sorted(trechos, reverse=True):
        texto = texto[:inicio] + '[NOME]' + texto[fim:]
    contagem['NOME-SPACY'] = len(trechos)
    logger.info(f'Origem: {origem}. Itens removidos por camada: {contagem} - o tamanho final do texto foi de {len(texto)} caracteres.')
    return texto

def localizar_nomes(texto):
    doc = NLP(texto.title())
    doc_min = NLP(texto.lower())
    if len(doc) != len(doc_min):
        raise ValueError('Textos distintos!')
    trechos = []
    for ent in doc.ents:
        if ent.label_ == 'PER':
            indices = [i for i in range(ent.start, ent.end) if doc_min[i].pos_ == 'PROPN']
            if indices:
                inicio = doc[indices[0]].idx
                fim = doc[indices[-1]].idx + len(doc[indices[-1]])
                trechos.append((inicio, fim))
    return trechos