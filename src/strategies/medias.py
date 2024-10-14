import time
from datetime import datetime
from time import sleep

import pandas as pd
from pocketoptionapi.ws.client import logger
from src.plataform.asset import Asset
from src.plataform.iq_options import ManagerIqOption
from src.repository.operation_record import OperationRecorder


class MediasMovileStrategy:
    def __init__(self, api: ManagerIqOption, asset: Asset, db: OperationRecorder, period=10):
        self.init_time = datetime.now()
        self.order_id = None
        self.profit_index = None
        self.api = api
        self.asset = asset
        self.period = period  # Número de velas para calcular la media móvil
        self._last_minute = None
        self.db = db
        self.sec_win = 0
        self.max_win = -1
        self.sec_lose = 0
        self.max_lose = -1
        self.id_buy = None
        self.ant_dir = None

    def generate_money(self):
        logger.info(f"estamos haciendo dinero con {self.asset.get_asset()}")
        while True:
            self.start()

    def start(self):
        current_second = datetime.now().second
        current_minute = datetime.now().minute
        if current_second < 10 and (self._last_minute is None or self._last_minute != current_minute):
            self._last_minute = current_minute
            candles = self.asset.load_candles(self.period + 1)  # Cargar suficientes velas para calcular la media móvil
            is_operation, direction = self.strategy(candles)
            if is_operation:
                self.execute_trade(direction)

    def execute_trade(self, direction):
        try:
            amount = self.calculate_amount()
            if direction:
                res, self.order_id = self.asset.buy(amount)
                logger.debug(f"ha comprar {self.asset.get_asset()}")
            else:
                res, self.order_id = self.asset.sell(amount)
                logger.debug(f"ha vender {self.asset.get_asset()}")
            self.db.record_operation(self.asset.get_asset(), self.order_id, 'buy' if direction else 'sell', amount,
                                     0, int(time.time()))
        except:
            logger.error(f"ERROR AL OPERAR: {self.asset.get_asset()}")

    def martin(self):
        if self.order_id is None:
            self.profit_index = 0
            return
        while True:
            status, profit = self.asset.get_position_status_profit(self.order_id)
            if status == 'closed':
                self.db.update_result_by_id_operation(self.order_id, profit)
                if profit > 0:
                    self.profit_index = 0
                else:
                    self.profit_index += 1
                return
            time.sleep(1)


    def calculate_amount(self):
        amounts = [1, 2]
        amount = amounts[0] if self.profit_index == 0 else amounts[self.profit_index % len(amounts)]
        return amount * 1

    def strategy(self, candles):
        self.martin()
        logger.info(f"{self.asset.get_asset()} monto generado: {self.db.get_total_results_in_range(self.init_time, datetime.now())}")
        # Convertir lista de objetos Candle en una lista de diccionarios
        data = [
            {
                'type': candle.type,
                'max': candle.max,
                'min': candle.min,
                'open': candle.open,
                'close': candle.close,
                'volume': candle.volume
            }
            for candle in candles
        ]
        # Crear un DataFrame con los datos de las velas
        df = pd.DataFrame(data)
        # Calcular la media móvil simple (o EMA si lo prefieres) con el período dado
        df['ma'] = df['close'].rolling(window=self.period).mean()

        # La última vela
        current_candle = df.iloc[-1]

        # Comparar si el precio de cierre de la última vela está por encima o por debajo de la media móvil
        if current_candle['close'] > current_candle['ma']:
            return True, True  # Operación de compra
        else:
            return True, False  # Operación de venta

    def evaluate_strategy(self):
        size = 990
        candles = self.asset.load_candles(size)
        winner = 0
        lose = 0
        amount = 0
        for k in range(1, size - self.period -1):
            candle_eval = candles[k:k + self.period +1]
            res, direc = self.strategy(candle_eval)
            if res:
                if direc == candles[k + 2].test:
                    winner += 1
                    amount += self.calculate_amount(self.sec_lose)*0.84
                    self.sec_win += 1
                    if self.sec_win > self.max_win:
                        self.max_win = self.sec_win
                    self.sec_lose = 0
                else:
                    amount -= self.calculate_amount(self.sec_lose)
                    lose += 1
                    self.sec_win = 0
                    self.sec_lose += 1
                    if self.sec_lose > self.max_lose:
                        self.max_lose = self.sec_lose
        logger.info(
            f"{self.asset.get_asset()} resultado {"{:05.2f}".format(amount)}: winrate: {winner - lose} total oper: {winner + lose} winner: {winner} lose: {lose} max_sec_win: {self.max_win} max_sec_lose: {self.max_lose}")
        return amount

