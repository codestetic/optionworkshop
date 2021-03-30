from .primitives import *
from common import *


def black(option_type: OptionType, s: float, x: float, time_to_exp: float, interest_rate: float,
          iv: float) -> tuple:
    if time_to_exp <= 0:
        return _expired_option_values_(option_type, s, x)

    tsqrt = sqrt(time_to_exp)
    ert = exp(-interest_rate * time_to_exp)
    d1 = log(s / x) / (iv * tsqrt) + 0.5 * iv * tsqrt
    d2 = d1 - iv * tsqrt
    cnd_d1 = cnd(d1)
    cnd_d2 = cnd(d2)
    cnd_minus_d1 = cnd(-d1)
    cnd_minus_d2 = cnd(-d2)
    nd_d1 = nd(d1)

    if option_type == OptionType.CALL:
        price = s * ert * cnd_d1 - x * ert * cnd_d2
        delta = cnd_d1 * ert
        gamma = (nd_d1 * ert) / (s * iv * tsqrt)
        vega = s * ert * nd_d1 * tsqrt / 100
        theta = (s * ert * nd_d1 * iv) / (
                2 * tsqrt) - interest_rate * s * ert * cnd_d1 + interest_rate * x * ert * cnd_d2
        theta /= 365
    elif option_type == OptionType.PUT:
        price = x * ert * cnd_minus_d2 - s * ert * cnd_minus_d1
        delta = -cnd_minus_d1 * ert
        gamma = (nd_d1 * ert) / (s * iv * tsqrt)
        vega = s * ert * nd_d1 * tsqrt / 100
        theta = (s * ert * nd_d1 * iv) / (
                2 * tsqrt) - interest_rate * s * ert * cnd_minus_d1 + interest_rate * x * ert * cnd_minus_d2
        theta /= 365

    return price, delta, gamma, vega, theta


def _expired_option_values_(call_put: str, underlying_price: float, strike: float):
    if call_put == 'c':
        return max(0.0, underlying_price - strike), 0, 0, 0, 0
    else:
        return max(0.0, strike - underlying_price), 0, 0, 0, 0
