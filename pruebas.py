import threading
import time
import logging

from pocketoptionapi.ws.client import logger
from repetir_anterior import RepeatLastStrategy
from src.plataform.asset import Asset
from src.plataform.iq_options import ManagerIqOption
from src.repository.operation_record import OperationRecorder
from src.strategies.consecutive_candles import CandlesConsecutiveStrategy
from src.strategies.medias import MediasMovileStrategy

# ver errores
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')



list_asset = ['EURUSD', 'EURJPY', 'GBPUSD', 'NZDUSD']
list_asset = ['USDMXM-OCT', ]

iqoption = ManagerIqOption()
assets = iqoption.get_api().get_binary_option_detail()
amout_total = 0
db = OperationRecorder()
logger.info(db.get_total_results())
# for key, data in assets.items():
#     try:
#         asset = Asset(iqoption, key)
#         amout_total += MediasMovileStrategy(iqoption, asset, 6).evaluate_strategy()
#     except:
#         logger.debug(f"error en {key}")
# logger.info(f"total: {amout_total}")
# CandlesConsecutiveStrategy(iqoption, asset, 2).evaluate_strategy()
# CandlesConsecutiveStrategy(iqoption, asset, 3).evaluate_strategy()
# CandlesConsecutiveStrategy(iqoption, asset, 4).evaluate_strategy()
# CandlesConsecutiveStrategy(iqoption, asset, 5).evaluate_strategy()
# CandlesConsecutiveStrategy(iqoption, asset, 6).evaluate_strategy()
# CandlesConsecutiveStrategy(iqoption, asset, 7).evaluate_strategy()
# CandlesConsecutiveStrategy(iqoption, asset, 8).evaluate_strategy()
# RepeatLastStrategy(iqoption, asset).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 3).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 4).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 5).evaluate_strategy()
#MediasMovileStrategy(iqoption, asset, 6).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 7).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 8).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 9).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 10).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 11).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 12).evaluate_strategy()
# MediasMovileStrategy(iqoption, asset, 13).evaluate_strategy()