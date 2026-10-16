from prompts import frase_apresentacao

# teste para identificação do nome do hospital
def test_nome_hospital():
    texto = 'Hospital XX'
    resultado = frase_apresentacao(texto)
    assert 'Hospital XX' in resultado

# teste para verificação de espaço na frase de apresentação
def test_espaco_na_frase():
    texto = 'Hospital YY'
    resultado = frase_apresentacao(texto)
    assert 'implantado. Uma' in resultado