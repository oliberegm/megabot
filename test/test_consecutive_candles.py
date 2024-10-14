import unittest
from unittest.mock import Mock
from src.plataform.asset import Asset
from src.plataform.iq_options import ManagerIqOption
from src.strategies.consecutive_candles import CandlesConsecutiveStrategy


class TestCandlesConsecutiveStrategy(unittest.TestCase):
    def setUp(self):
        # Creamos un mock para el api y el asset
        self.api_mock = ManagerIqOption()
        self.asset_mock = Asset(self.api_mock, "")

        # Inicializamos la estrategia con los mocks y 4 candles
        self.strategy = CandlesConsecutiveStrategy(self.api_mock, self.asset_mock, 4)

    def test_strategy_all_candles_same_except_first(self):
        # Simulamos la respuesta de load_candles con datos de prueba
        self.asset_mock.load_candles.return_value = [
            Mock(test=False),  # first candle
            Mock(test=True),   # rest candles (all same)
            Mock(test=True),
            Mock(test=True),
            Mock(test=True),
        ]

        # Ejecutamos el método strategy
        is_operation, direction = self.strategy.strategy()

        # Verificamos que la estrategia detecte una operación
        self.assertTrue(is_operation)
        self.assertEqual(direction, True)

        # Verificamos que load_candles se haya llamado con el valor correcto
        self.asset_mock.load_candles.assert_called_once_with(5)

    def test_strategy_candles_not_all_equal(self):
        # Simulamos la respuesta de load_candles con datos de prueba
        self.asset_mock.load_candles.return_value = [
            Mock(test=False),  # first candle
            Mock(test=True),   # rest candles (not all same)
            Mock(test=False),
            Mock(test=True),
            Mock(test=False),
        ]

        # Ejecutamos el método strategy
        is_operation, direction = self.strategy.strategy()

        # Verificamos que la estrategia no detecte operación
        self.assertFalse(is_operation)
        self.assertIsNone(direction)

        # Verificamos que load_candles se haya llamado con el valor correcto
        self.asset_mock.load_candles.assert_called_once_with(5)


if __name__ == "__main__":
    unittest.main()
