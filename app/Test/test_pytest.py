import pytest
from app.modulos.validaciones import validar_cedula

def test_cedula_correcta():
    assert validar_cedula("1712345678") is None

def test_cedula_corta_error():
    with pytest.raises(Exception):
        validar_cedula("123") # Debe fallar porque no tiene 10 dígitos
