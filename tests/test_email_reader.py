import pytest
from email_reader import limpar_html

def test_limpar_html_remove_tags():
    texto = '<b>Teste</b> com <a href="#">tags</a>.'
    resultado = limpar_html(texto)
    assert resultado == 'Teste com tags.'

def test_limpar_html_sem_tags():
    texto = 'Texto limpo.'
    resultado = limpar_html(texto)
    assert resultado == 'Texto limpo.'
