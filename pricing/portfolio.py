from typing import Union

from common.execution import *
from common.instruments import *
# from .containers import StrategyCalculatedParams
from .context import *


def risk_profile(portfolio: Portfolio, underlying_price: Union[np.ndarray, float, int],
                 context: PricingContext):
    theor_price = None
    theor_pnl = None
    exp_pnl = None
    for position in portfolio.positions.values():
        pos_price, pos_pnl, pos_exp_pnl = __position_risk_profile__(position, underlying_price, context)
        if theor_price is None:
            theor_price = pos_price
            theor_pnl = pos_pnl
            exp_pnl = pos_exp_pnl
        else:
            theor_price = theor_price + pos_price
            theor_pnl = theor_pnl + pos_pnl
            exp_pnl = exp_pnl + pos_exp_pnl

    return theor_price, theor_pnl, exp_pnl


def __position_risk_profile__(position: Position, underlying_price: Union[np.ndarray, float, int],
                              context: PricingContext):
    model = context.model
    q = position.quantity
    if isinstance(position.instrument, Option):
        option = position.instrument
        strike = option.strike
        price = model.price(option.type, strike, option.tte(), context.iv(strike, underlying_price),
                            underlying_price)
        expiration_pnl = np.maximum(0, underlying_price - strike) if option.type == OptionType.CALL else np.maximum(0,
            strike - underlying_price)
        expiration_pnl = q * (expiration_pnl - position.price)
        return q * price, q * (price - position.price), expiration_pnl
    else:
        price = q * underlying_price
        pnl = q * (underlying_price - position.price)
        return price, pnl, pnl


def calc_strategy_params(strategy: Portfolio, underlying_price: object,
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
