from iqoptionapi.stable_api import IQ_Option

from src.utils.load_credential import LoadCredential


class ManagerIqOption:
    def __init__(self):
        self.credentials:LoadCredential = LoadCredential()
        self.api:IQ_Option = self._init_api()

    def _init_api(self):
        api = IQ_Option(self.credentials.get_user(),self.credentials.get_pass())
        api.connect()
        return api

    def get_api(self):
        return self.api

    def list_binaries(self):
        resp = self.api.get_all_init()
        inst = {}

        for key, active in resp['result']['turbo']['actives'].items():
            ticker = active.get('ticker')
            enabled = active.get('enabled')
            commission = active['option']['profit'].get('commission')
            exp_time = active['option'].get('exp_time')
            inst[ticker] = {
                'ticker': ticker,
                'enabled': enabled,
                'commission': commission,
                'exp_time': exp_time,
                'top_traders_enabled': active.get('top_traders_enabled')
            }
        return inst

    def get_candles(self, ACTIVES, interval, count, endtime):
        return self.api.get_candles(ACTIVES, interval, count, endtime)

    def buy(self, amount, ACTIVES, action, duration):
        return self.api.buy_digital_spot(ACTIVES, amount, action, duration)

    def start_candles_stream(self, ACTIVE, size, maxdict):
        return self.api.start_candles_stream(ACTIVE, size, maxdict)

    def stop_candles_stream(self, ACTIVE, size):
        return self.api.stop_candles_stream( ACTIVE, size)

    def get_realtime_candles(self, ACTIVE, size):
        return self.api.get_realtime_candles(ACTIVE, size)

    def get_position(self, buy_order_id):
        return self.api.get_position(buy_order_id)

    def get_digital_position(self, id_operation):
        return self.api.get_digital_position(id_operation)



