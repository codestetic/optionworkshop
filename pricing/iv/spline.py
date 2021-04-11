# IV curve with linear tails and spline in the center

import numpy as np
from scipy.interpolate import splev, splrep, CubicSpline

from .common import convert_strikes_to_moneyness, calculate_mids_and_errors


class IvCurve:
    def __init__(self, center_spline):
        self.center_spline = center_spline

    def iv(self, strike_or_moneyness, current_underlying_price=None) -> float:
        if current_underlying_price is not None:
            strike_or_moneyness = (strike_or_moneyness - current_underlying_price) / current_underlying_price
        else:
            x = strike_or_moneyness
            return splev(x, self.center_spline)

        return self.iv(strike_or_moneyness)


def fit(strikes, bid_ivs, ask_ivs, underlying_price, spl_deg=3) -> IvCurve:
    """
    Фитит рыночные значения волатильностей полиномиальной кривой
    :param strikes:
    :param bid_ivs:
    :param ask_ivs:
    :param underlying_price:
    :param weighted:
    :return:
    """
    x = convert_strikes_to_moneyness(strikes, underlying_price)
    ivs, errors = calculate_mids_and_errors(bid_ivs, ask_ivs)

    spl = splrep(x, ivs, k=spl_deg, s=0.025)
    return IvCurve(spl)
