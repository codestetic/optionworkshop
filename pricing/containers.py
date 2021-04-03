from typing import Union

import numpy as np


class StrategyCalculatedParams:

    def __init__(self, strategy: Strategy, grid: Union[np.ndarray, float]):
        self.grid = grid
        self.strategy = strategy

        if isinstance(grid, np.ndarray):
            self.length = len(grid)
        else:
            self.length = 1

        self.price = None
        self.pnl = None
        self.delta = None
        self.gamma = None
        self.vega = None
        self.theta = None

    def append_position_params(self, price, pnl, delta, gamma, vega, theta):

        if self.price is None:
            if self.length > 1:
                self.price = np.copy(price)
                self.pnl = np.copy(pnl)
                self.delta = np.copy(delta)
                self.gamma = np.copy(gamma)
                self.vega = np.copy(vega)
                self.theta = np.copy(theta)
            else:
                self.price = price
                self.pnl = pnl
                self.delta = delta
                self.gamma = gamma
                self.vega = vega
                self.theta = theta
        else:
            self.price += price
            self.pnl += pnl
            self.delta += delta
            self.gamma += gamma
            self.vega += vega
            self.theta += theta
