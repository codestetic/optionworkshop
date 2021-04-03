from datetime import datetime

from common.instruments import Instrument
from .fill import Fill


class Position:
    def __init__(self, instrument: Instrument, quantity: int = 0, price: float = 0, fixed_pnl: float = 0):
        self.instrument = instrument
        self.fills = []
        self.fixed_pnl = fixed_pnl
        self.quantity = 0
        self.price = 0
        self.volume = 0

        if quantity != 0:
            self.add_fill(Fill(instrument, price, quantity, datetime.now()))

    def add_fill(self, fill: Fill):
        if fill.instrument != self.instrument:
            raise Exception('Position and fill must have same instrument')

        if fill in self.fills:
            return

        self.fills.append(fill)

        if len(self.fills) == 1:
            self.quantity = fill.quantity
            self.price = fill.price
            self.volume = -fill.price * fill.quantity
            return

        new_quantity = self.quantity + fill.quantity

        if self.quantity == 0:
            self.quantity = fill.quantity
            self.price = fill.price
            self.volume = -fill.price * fill.quantity
            return

        # если сделка закрывает позицию
        if new_quantity == 0:
            self.fixed_pnl += -fill.quantity * (fill.price - self.price)
            self.volume = 0
            self.quantity = 0
            self.price = 0

        # если сделка не меняет знак позиции
        elif new_quantity * self.quantity > 0:

            # если сделка увеличивает позицию
            if self.quantity * fill.quantity > 0:
                self.volume += -fill.quantity * fill.price
                self.quantity = new_quantity
                self.price = abs(self.volume / self.quantity)

            # если сделка закрывает часть позиции
            else:
                self.volume += -fill.quantity * fill.price
                self.fixed_pnl += -fill.quantity * (fill.price - self.price)
                # self.price = fill.price
                self.quantity = new_quantity

        # если сделка переворачивает позицию
        elif new_quantity * self.quantity < 0:
            closing_quantity = abs(self.quantity) * (fill.quantity / abs(fill.quantity))
            opening_quantity = fill.quantity - closing_quantity
            self.volume += -closing_quantity * fill.price
            self.fixed_pnl += self.volume
            self.price = fill.price
            self.quantity = opening_quantity
            self.volume = -self.quantity * self.price

    def __str__(self):
        return "{0} {1} {2}".format(self.instrument.code, self.quantity, self.price)
