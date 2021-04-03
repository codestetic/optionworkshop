from common.execution.fill import Fill
from common.execution.position import Position


class Portfolio:
    def __init__(self, name: str):
        self.name = name
        self.positions = {}

    def add_position(self, *positions: Position):

        for position in positions:
            if position in self.positions:
                return

            self.positions[position.instrument] = position

    def add_fills(self, fills: Fill):
        if hasattr(fills, '__iter__'):
            for fill in fills:
                self.__get_position__(fill).add_fill(fill)
        else:
            fill = fills
            self.__get_position__(fill).add_fill(fill)

    def __get_position__(self, fill):
        pos = self.positions.get(fill.instrument)
        if pos is None:
            pos = Position(fill.instrument)
            self.positions[fill.instrument] = pos
        return pos

    def make_copy(self):
        strategy = Portfolio(self.name)

        for position in self.positions.values():
            strategy.add_position(Position(position.instrument, position.quantity, position.price, position.fixed_pnl))

        return strategy

    def fixed_pnl(self):
        pnl = 0
        for position in self.positions.values():
            pnl += position.fixed_pnl
        return pnl

    def is_closed(self):
        for position in self.positions.values():
            if position.quantity != 0:
                return False
        return True
