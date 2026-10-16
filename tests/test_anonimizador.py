import logging

from anonimizador import anonimizar_texto

def test_remove_cpf():
    texto = '00295651139 ou 004.666.888-39'
    resultado = anonimizar_texto(texto)
    assert '00295651139' not in resultado
    assert '004.666.888-39' not in resultado
    assert '[CPF]' in resultado

def test_remove_telefone():
    texto = '(65) 99999-1234'
    resultado =  anonimizar_texto(texto)
    assert '(65) 99999-1234' not in resultado
    assert '[TELEFONE]' in resultado

def test_remove_email():
    texto = 'eusou@email.com'
    resultado =  anonimizar_texto(texto)
    assert 'eusou@email.com' not in resultado
    assert '[EMAIL]' in resultado

def test_remove_nome_apos_gatilho():
    texto = 'filho Pedro Lima ligou'
    resultado =  anonimizar_texto(texto)
    assert 'Pedro Lima' not in resultado
    assert '[NOME]' in resultado

def test_nao_altera_texto_sem_dado_pessoal():
    texto = 'A filha informou que o paciente caiu no banheiro'
    resultado =  anonimizar_texto(texto)
    assert resultado == texto

def test_remove_nome_sem_gatilho():
    texto = 'PACIENTE RELATA QUE MARIA DA SILVA CAIU NO BANHEIRO'
    resultado = anonimizar_texto(texto)
    assert 'MARIA' not in resultado
    assert 'SILVA' not in resultado
    assert '[NOME]' in resultado
    assert 'CAIU' in resultado

def test_log_nao_contem_texto(caplog):
    with caplog.at_level(logging.INFO):
        resultado = anonimizar_texto('Paciente CPF 123.456.789-09, filho Pedro Lima ligou')
    assert 'Pedro' not in caplog.text
    assert '123.456.789-09' not in caplog.text
    assert '[CPF]' in caplog.text
