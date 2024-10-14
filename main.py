import threading
import time
import logging

from pocketoptionapi.ws.client import logger
from src.plataform.asset import Asset
from src.plataform.iq_options import ManagerIqOption
from src.repository.operation_record import OperationRecorder
from src.strategies.consecutive_candles import CandlesConsecutiveStrategy
from src.strategies.medias import MediasMovileStrategy

# ver errores
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')







iqoption = ManagerIqOption()
db = OperationRecorder()
"""
_, id_operacion = iqoption.api.buy_digital_spot('EURUSD-OTC', 1, 'put', 1)
print(id_operacion)
i = 0
while True:
    resultado_operacion = iqoption.api.get_digital_position(id_operacion)
    if resultado_operacion['msg']['position']['status'] != 'open':
        print(resultado_operacion)
        print(resultado_operacion['msg']['position']['close_effect_amount'])
        break
    time.sleep(1)
    print(f"no ha cerrado {i+1}")
#resultado_operacion = iqoption.api.get_digital_position(id_operacion)

print(resultado_operacion)
print(resultado_operacion['msg']['status'])



print("final")
#print(iqoption.api.get_digital_position(19344239981))
"""
#      get_digital_spot_profit_after_sale(11995637739))
# asset = Asset(iqoption, "EURUSD-OTC")
# estrategia1 = MediasMovileStrategy(iqoption, asset, db, 6)
# thread = threading.Thread(target=estrategia1.generate_money)
# thread.start()
# estra = CandlesConsecutiveStrategy(iqoption, asset, 4)
# estra.evaluate_strategy()

#
assets = iqoption.get_api().get_binary_option_detail()
#
count = 0
threads = []  # Almacenar los hilos creados para luego controlarlos
#
list_asset = ["EURUSD-OTC", "USDCAD-OTC", "GBPUSD-OTC", "EURCAD-OTC"]
list_asset = ["EURUSD"]
for key in list_asset:
        try:
            asset = Asset(iqoption, key)
            estrategia1 = MediasMovileStrategy(iqoption, asset, db, 6)
            #estrategia1.generate_money()
            thread = threading.Thread(target=estrategia1.generate_money)
            thread.start()  # Iniciar el hilo
            threads.append(thread)  # Añadir el hilo a la lista
            count += 1
        except Exception as inst:
            logger.error(f"no poder obtener candles {key} {inst}")

for t in threads:
            t.join()