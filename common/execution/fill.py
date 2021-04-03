from common.instruments import Instrument
from datetime import datetime


class Fill:

    def __init__(self, instrument: Instrument, price: float, quantity: int, time: datetime):
        self.price = price
        self.quantity = quantity
        self.instrument = instrument
        self.time = time
