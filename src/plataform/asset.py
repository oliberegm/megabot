import time
from datetime import datetime


from src.plataform.candle import Candle
from src.plataform.iq_options import ManagerIqOption
import logging

class Asset:
    def __init__(self, api:ManagerIqOption, asset_name):
        self.size_candles = 60
        self.count_candles = 1000
        self._api = api
        self._asset_name = asset_name
        self._last_loaded_time = 0  # Tiempo de la última carga
        self._cached_candles = None  # Almacena los datos de los candles
        self._init_candles()

    def get_asset(self):
        return self._asset_name

    def _transform_candle_data(self, candles):
        transformed_candles = []
        for candle in candles:
            candle_type = 'green' if candle['close'] > candle['open'] else 'red'
            candle_test = candle['close'] > candle['open']
            transformed_candles.append(Candle(
                candle_type=candle_type,
                candle_test=candle_test,
                max_value=candle['max'],
                min_value=candle['min'],
                open_value=candle['open'],
                close_value=candle['close'],
                volume=candle['volume']
            ))
        return transformed_candles

    def load_candles(self, count):
        current_minute = datetime.now().minute
        if current_minute != self._last_loaded_time or self._cached_candles is None:
            candles = self._get_candles(count)
            self._cached_candles = self._transform_candle_data(candles)  # Actualizar el cache con los nuevos datos
            self._last_loaded_time = current_minute  # Actualizar el tiempo de la última carga
            logging.debug(f"load candles {self._asset_name}")
        # Devolver los datos almacenados (nuevos o en cache si fue invocado dentro del mismo minuto)

            # Verificamos que la cantidad de velas devuelta sea la correcta
        if len(self._cached_candles) != count:
            logging.debug(f"Expected {count} candles, but received {len(self._cached_candles)}")
            self._cached_candles = self._cached_candles[-count:]
        return self._cached_candles

    def _get_candles(self, count):
        resp = self._api.get_realtime_candles(self._asset_name, self.size_candles)
        candles = list(resp.values())
        return candles[len(candles)-count-1: len(candles)-1]

    def is_active_for_operation(self):
        # falta agregar la logica cuando no este activo el instrumento debe devolver false
        return True

    def buy(self, amount):
        return self._api.buy(amount, self._asset_name, 'call', 1)

    def sell(self, amount):
        return self._api.buy(amount, self._asset_name, 'put', 1)

    def _init_candles(self):
        self._api.start_candles_stream(self._asset_name, self.size_candles, self.count_candles)

    def get_position_status_profit(self, id_operation):
        result = self._api.get_digital_position(id_operation)
        return result['msg']['position']['status'], result['msg']['position']['close_effect_amount']

    def __del__(self):
        self._api.stop_candles_stream(self._asset_name, self.size_candles)
