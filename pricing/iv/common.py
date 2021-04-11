from datetime import datetime
from typing import Union

import numpy as np

from common.instruments import Option


def iv(option: Option, prices: Union[float, int, np.ndarray, list], und_price: float, model: object,
       time: Union[float, datetime]):
    """
    Evaluates implied volatilities for option prices
    :param option: The option descriptor
    :param prices: Options prices to convert into IV space
    :param und_price: An option underlying instrument price, at which we convert prices into IVs
    :param model: Options pricing model
    """
    if isinstance(time, datetime):
        time = (option.expiration - time).total_seconds() / 365 / 24 / 3600

    if isinstance(prices, float) or isinstance(prices, int):
        return _iv_(option, prices, und_price, model, time)

    ivs = []
    for price in prices:
        ivs.append(_iv_(option, price, und_price, model, time))

    return ivs


def _iv_(option: Option, price: float, und_price: float, model: object,
         time: float):
    a_iv, c_iv = 0.001, 10.0
    iter_limit = 50
    tolerance = 10e-5
    i = 0
    a_p = model.price(option.type, option.strike, time, a_iv, und_price) - price
    c_p = model.price(option.type, option.strike, time, c_iv, und_price) - price

    while c_iv - a_iv > tolerance and i < iter_limit:
        b_iv = 0.5 * (a_iv + c_iv)
        b_p = model.price(option.type, option.strike, time, b_iv, und_price) - price

        if a_p * b_p < 0:
            c_iv = b_iv
        elif b_p * c_p < 0:
            a_iv = b_iv
        i = i + 1

    return 0.5 * (a_iv + c_iv)



def convert_strikes_to_moneyness(strikes, underlying_price):
    """
    Converts strikes array into moneyness
    :param strikes:
    :param underlying_price: Current price of the options underlying instrument
    :return:
    """
    return np.array((strikes - underlying_price) / underlying_price)


def calculate_mids_and_errors(bid_ivs, ask_ivs):
    """
    Returns
    :param bid_ivs: Bids implied volatylities
    :param ask_ivs: Asks implied volatylities
    :return:
    """
    return np.array((ask_ivs + bid_ivs) / 2), np.array(ask_ivs - bid_ivs)
