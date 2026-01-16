import unittest
from unittest.mock import MagicMock
from app.modulos.validaciones import validar_monto_positivo

class TestCaja(unittest.TestCase):
    # Prueba Unittest
    def test_monto_valido(self):
        self.assertIsNone(validar_monto_positivo(100))

    # Prueba con Mock (Simulando Mockito)
    def test_mock_base_datos(self):
        mock_db = MagicMock()
        # Simulamos que la DB devuelve un socio específico
        mock_db.query().filter().first.return_value = {"nombre": "Alberto", "cedula": "1234567890"}
        resultado = mock_db.query().filter().first()
        self.assertEqual(resultado["nombre"], "Alberto")

if __name__ == '__main__':
    unittest.main()
