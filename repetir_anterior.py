from datetime import datetime

from pocketoptionapi.ws.client import logger
from src.plataform.asset import Asset
from src.plataform.iq_options import ManagerIqOption


class RepeatLastStrategy:
    def __init__(self, api:ManagerIqOption, asset:Asset):
        self.api = api
        self.asset = asset
        self._last_minute = None
        #self.statistics = statistics
        self.sec_win = 0
        self.max_win = -1
        self.sec_lose = 0
        self.max_lose = -1

    def generate_money(self):
        logger.info(f"estamos haciendo dinero {self.asset.get_asset()}")
        while True:
            self.start()


    def start(self):
        current_second = datetime.now().second
        current_minute = datetime.now().minute
        if (current_second == 0 and (
                self._last_minute is None or self._last_minute != current_minute)
                and self.asset.is_active_for_operation()):
            self._last_minute = current_minute
            candles = self.asset.load_candles(2)
            is_operation, direction = self.strategy(candles)
            if is_operation:
                self.execute_trade(direction)

    def execute_trade(self, direction):
        amount = self.calculate_amount()
        if direction:
            self.asset.buy(amount)
            logger.info(f"ha comprar {self.asset.get_asset()}")
        else:
            self.asset.sell(amount)
            logger.info(f"ha vender {self.asset.get_asset()}")

    def calculate_amount(self):
        return 1


    def strategy(self, candles):
        return True,not candles[-1].test

    def evaluate_strategy(self):
        size = 990
        candles = self.asset.load_candles(size)
        logger.info(f"cantidad: {len(candles)}")
        winner = 0
        lose = 0
        for k in range (1, size - 2):
            candle_eval = candles[k:k+2]
            """p1 = " ".join(str(candle.test) for candle in candle_eval)
            p2 = candles[k+self.n_candles].test
            logger.info(f"{p1} {p2}")"""
            res, direc =self.strategy(candle_eval)
            if res:
                if direc == candles[k+2].test:
                    winner += 1
                    self.sec_win += 1
                    if self.sec_win > self.max_win:
                        self.max_win = self.sec_win
                    self.sec_lose = 0
                else:
                    lose += 1
                    self.sec_win = 0
                    self.sec_lose += 1
                    if self.sec_lose > self.max_lose:
                        self.max_lose = self.sec_lose
        logger.error(f"resultado para {self.asset.get_asset()}: winrate: {winner - lose} total oper: {winner + lose} winner: {winner} lose: {lose} max_sec_win: {self.max_win} max_sec_lose: {self.max_lose}")
        return winner, lose



