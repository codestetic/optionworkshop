from typing import Union, Iterable

from common.instruments import *
from .primitives import *


def price(option_type: OptionType, strike: float, time_to_exp: float,
          iv: float, und_price: Union[np.ndarray,  float], interest_rate: float = 0) -> tuple:
    return __price__(option_type, und_price, strike, time_to_exp, interest_rate, iv)


def delta(option_type: OptionType, strike: float, time_to_exp: float,
          iv: float, und_price: Union[np.ndarray, float], interest_rate: float = 0) -> tuple:
    if isinstance(und_price, float) or isinstance(und_price, int):
        return __delta__(option_type, und_price, strike, time_to_exp, interest_rate, iv)
    else:
        ln = len(und_price)
        delta = np.zeros(ln)

        i = 0
        for x in und_price:
            delta[i] = __delta__(option_type, x, strike, time_to_exp, interest_rate, iv)
            i = i + 1

        return delta


def __black__(option_type: OptionType, und_price: float, strike: float, time_to_exp: float,
              interest_rate: float, iv: float) -> tuple:
    if time_to_exp <= 0:
        return _expired_option_values_(option_type, und_price, strike)

    tsqrt = sqrt(time_to_exp)
    ert = exp(-interest_rate * time_to_exp)
    d1 = log(und_price / strike) / (iv * tsqrt) + 0.5 * iv * tsqrt
    d2 = d1 - iv * tsqrt
    cnd_d1 = cnd(d1)
    cnd_d2 = cnd(d2)
    cnd_minus_d1 = cnd(-d1)
    cnd_minus_d2 = cnd(-d2)
    nd_d1 = nd(d1)

    if option_type == OptionType.CALL:
        price = und_price * ert * cnd_d1 - strike * ert * cnd_d2
        delta = cnd_d1 * ert
        gamma = (nd_d1 * ert) / (und_price * iv * tsqrt)
        vega = und_price * ert * nd_d1 * tsqrt / 100
        theta = (und_price * ert * nd_d1 * iv) / (
                2 * tsqrt) - interest_rate * und_price * ert * cnd_d1 + interest_rate * strike * ert * cnd_d2
        theta /= 365
    elif option_type == OptionType.PUT:
        price = strike * ert * cnd_minus_d2 - und_price * ert * cnd_minus_d1
        delta = -cnd_minus_d1 * ert
        gamma = (nd_d1 * ert) / (und_price * iv * tsqrt)
        vega = und_price * ert * nd_d1 * tsqrt / 100
        theta = (und_price * ert * nd_d1 * iv) / (
                2 * tsqrt) - interest_rate * und_price * ert * cnd_minus_d1 + interest_rate * strike * ert * cnd_minus_d2
        theta /= 365

    return price, delta, gamma, vega, theta


def __price__(option_type: OptionType, und_price: float, strike: float, time_to_exp: float,
              interest_rate: float, iv: float) -> tuple:

    if time_to_exp <= 0:
        return _expired_option_values_(option_type, und_price, strike)

    tsqrt = sqrt(time_to_exp)
    ert = exp(-interest_rate * time_to_exp)
    d1 = np.log(und_price / strike) / (iv * tsqrt) + 0.5 * iv * tsqrt
    d2 = d1 - iv * tsqrt
    cnd_d1 = cnd(d1)
    cnd_d2 = cnd(d2)
    cnd_minus_d1 = cnd(-d1)
    cnd_minus_d2 = cnd(-d2)
    price = 0

    if option_type == OptionType.CALL:
        price = und_price * ert * cnd_d1 - strike * ert * cnd_d2
    elif option_type == OptionType.PUT:
        price = strike * ert * cnd_minus_d2 - und_price * ert * cnd_minus_d1

    return price


def __delta__(option_type: OptionType, und_price: float, strike: float, time_to_exp: float,
              interest_rate: float, iv: float) -> tuple:
    if time_to_exp <= 0:
        return _expired_option_values_(option_type, und_price, strike)

    tsqrt = sqrt(time_to_exp)
    ert = exp(-interest_rate * time_to_exp)
    d1 = log(und_price / strike) / (iv * tsqrt) + 0.5 * iv * tsqrt
    d2 = d1 - iv * tsqrt
    cnd_d1 = cnd(d1)
    cnd_minus_d1 = cnd(-d1)

    delta = 0

    if option_type == OptionType.CALL:
        delta = cnd_d1 * ert
    elif option_type == OptionType.PUT:
        delta = -cnd_minus_d1 * ert

    return delta


def __gamma__(option_type: OptionType, und_price: float, strike: float, time_to_exp: float,
              interest_rate: float, iv: float) -> tuple:
    if time_to_exp <= 0:
        return _expired_option_values_(option_type, und_price, strike)

    tsqrt = sqrt(time_to_exp)
    ert = exp(-interest_rate * time_to_exp)
    d1 = log(und_price / strike) / (iv * tsqrt) + 0.5 * iv * tsqrt
    d2 = d1 - iv * tsqrt
    nd_d1 = nd(d1)
    gamma = 0

    if option_type == OptionType.CALL:
        gamma = (nd_d1 * ert) / (und_price * iv * tsqrt)
    elif option_type == OptionType.PUT:
        gamma = (nd_d1 * ert) / (und_price * iv * tsqrt)

    return gamma


def __vega__(option_type: OptionType, und_price: float, strike: float, time_to_exp: float,
             interest_rate: float, iv: float) -> tuple:
    if time_to_exp <= 0:
        return _expired_option_values_(option_type, und_price, strike)

    tsqrt = sqrt(time_to_exp)
    ert = exp(-interest_rate * time_to_exp)
    d1 = log(und_price / strike) / (iv * tsqrt) + 0.5 * iv * tsqrt
    d2 = d1 - iv * tsqrt
    nd_d1 = nd(d1)
    vega = 0

    if option_type == OptionType.CALL:
        vega = und_price * ert * nd_d1 * tsqrt / 100
    elif option_type == OptionType.PUT:
        vega = und_price * ert * nd_d1 * tsqrt / 100

    return vega


def __theta__(option_type: OptionType, und_price: float, strike: float, time_to_exp: float,
              interest_rate: float, iv: float) -> tuple:
    if time_to_exp <= 0:
        return _expired_option_values_(option_type, und_price, strike)

    tsqrt = sqrt(time_to_exp)
    ert = exp(-interest_rate * time_to_exp)
    d1 = log(und_price / strike) / (iv * tsqrt) + 0.5 * iv * tsqrt
    d2 = d1 - iv * tsqrt
    cnd_d1 = cnd(d1)
    cnd_d2 = cnd(d2)
    cnd_minus_d1 = cnd(-d1)
    cnd_minus_d2 = cnd(-d2)
    nd_d1 = nd(d1)
    theta = 0

    if option_type == OptionType.CALL:
        theta = (und_price * ert * nd_d1 * iv) / (
                2 * tsqrt) - interest_rate * und_price * ert * cnd_d1 + interest_rate * strike * ert * cnd_d2
        theta /= 365
    elif option_type == OptionType.PUT:
        theta = (und_price * ert * nd_d1 * iv) / (
                2 * tsqrt) - interest_rate * und_price * ert * cnd_minus_d1 + interest_rate * strike * ert * cnd_minus_d2
        theta /= 365

    return theta


def _expired_option_values_(call_put: str, underlying_price: float, strike: float):
    if call_put == 'c':
        return max(0.0, underlying_price - strike), 0, 0, 0, 0
    else:
        return max(0.0, strike - underlying_price), 0, 0, 0, 0
