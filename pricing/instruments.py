from common import *
from datetime import datetime
from .models.black import black
import numpy as np


def calc_option_params(option: Option, underlying_price: object, time: datetime = datetime.now()) -> tuple:
    call_put = 'c' if type(option) is Call else 'p'
    tte = (option.series.expiration - time).total_seconds() / (365*24*3600)

    if type(underlying_price) is np.ndarray:
        return _calc_option_range_params_(call_put, underlying_price, option.strike, option.iv, tte)
    else:
        return black(call_put, underlying_price, option.strike, tte, 0, option.iv)


def calc_futures_params(futures: Futures, underlying_price: object, time: datetime = datetime.now()) -> tuple:

    if type(underlying_price) is np.ndarray:
        zeros = np.zeros(len(underlying_price))
        # return zeros, zeros, zeros, zeros, zeros
        return np.copy(underlying_price), zeros, zeros, zeros, zeros
    else:
        return underlying_price, 0, 0, 0, 0


def _calc_option_range_params_(call_put: str, underlying_price: np.ndarray, strike: float, iv: float,
                               tte: float) -> tuple:
    n = len(underlying_price)
    price = np.zeros(n)
    delta = np.zeros(n)
    gamma = np.zeros(n)
    vega = np.zeros(n)
    theta = np.zeros(n)

    for i in range(n):
        price[i], delta[i], gamma[i], vega[i], theta[i] = black(call_put, underlying_price[i], strike, tte, 0, iv)

    return price, delta, gamma, vega, theta
