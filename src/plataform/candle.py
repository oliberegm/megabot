
class Candle:
    def __init__(self, candle_type, candle_test, max_value, min_value, open_value, close_value, volume):
        self.type = candle_type
        self.test = candle_test
        self.max = max_value
        self.min = min_value
        self.open = open_value
        self.close = close_value
        self.volume = volume

    def __repr__(self):
        return f"Candle(type={self.type}, max={self.max}, min={self.min}, open={self.open}, close={self.close}, volume={self.volume})"
