# IV curve with linear tails and spline in the center

import numpy as np
from scipy.interpolate import splev, splrep, CubicSpline

from .common import convert_strikes_to_moneyness, calculate_mids_and_errors


class IvCurve:
    def __init__(self, left_tail, center_spline, right_tail):
        self.x_l = left_tail[0]
        self.x_r = right_tail[0]
        self.left_poly = left_tail[1]
        self.right_poly = right_tail[1]
        self.center_spline = center_spline

    def iv(self, strike_or_moneyness, current_underlying_price=None) -> float:
        if current_underlying_price is not None:
            strike_or_moneyness = (strike_or_moneyness - current_underlying_price) / current_underlying_price
        else:
            x = strike_or_moneyness
            if np.isscalar(x):
                if x < self.x_l:
                    return self.L(x)
                elif x > self.x_r:
                    return self.R(x)
                else:
                    return self.C(x)
            else:
                left = self.L(x)
                center = self.C(x)
                right = self.R(x)
                return np.concatenate((left, center, right), axis=0)

        return self.iv(strike_or_moneyness)

    def C(self, x):
        cs = self.center_spline
        if not (np.isscalar(x)):
            x = x[(self.x_l <= x) & (x <= self.x_r)]
        return cs(x)

    def R(self, x):
        if not (np.isscalar(x)):
            x = x[x > self.x_r]
        return np.polyval(self.right_poly, x)

    def L(self, x):
        if not (np.isscalar(x)):
            x = x[x < self.x_l]
        return np.polyval(self.left_poly, x)


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
    (knots, coeffs, k_fact) = spl
    unique_knots = list(set(knots))
    unique_knots.sort()
    yy = splev(unique_knots, spl)
    yy[0] = np.polyval(left_tail[1], unique_knots[0])
    yy[-1] = np.polyval(right_tail[1], unique_knots[-1])
    bc_type = ((1, left_tail[1][0]), (1, right_tail[1][0]))
    cs = CubicSpline(unique_knots, yy, bc_type=bc_type)
    return IvCurve(left_tail, cs, right_tail)
