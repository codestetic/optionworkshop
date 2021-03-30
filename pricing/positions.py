from common import *
import numpy as np

from .containers import StrategyCalculatedParams
from .instruments import *


def calc_strategy_params(strategy: Strategy, underlying_price: object,
                         time: datetime = datetime.now()):

    params = StrategyCalculatedParams(strategy, underlying_price)
    params_exp = StrategyCalculatedParams(strategy, underlying_price)
    options_only_params = StrategyCalculatedParams(strategy, underlying_price)
    options_only_params_exp = StrategyCalculatedParams(strategy, underlying_price)

    for position in strategy.positions.values():
        position_params = calc_position_params(position, underlying_price, time)
        position_params_exp = calc_position_params(position, underlying_price,
                                                   position.instrument.expiration)
        params.append_position_params(*position_params)
        params_exp.append_position_params(*position_params_exp)

        if isinstance(position.instrument, Option):
            options_only_params.append_position_params(*position_params)
            options_only_params_exp.append_position_params(*position_params_exp)

    return params, params_exp, options_only_params, options_only_params_exp


def calc_position_params(position: Position, underlying_price: object, time: datetime = datetime.now()):
    if isinstance(position.instrument, Option):
        price, delta, gamma, vega, theta = calc_option_params(position.instrument, underlying_price, time)
    elif isinstance(position.instrument, Futures):
        price, delta, gamma, vega, theta = calc_futures_params(position.instrument, underlying_price, time)

    price *= position.quantity
    pnl = price - position.quantity * position.price + position.fixed_pnl
    delta *= position.quantity
    gamma *= position.quantity
    vega *= position.quantity
    theta *= position.quantity

    return price, pnl, delta, gamma, vega, theta


def _gen_empty_arrays_(n: int):
    return np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n),
