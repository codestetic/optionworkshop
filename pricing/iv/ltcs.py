# IV curve with linear tails and spline in the center
import math

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
            strike_or_moneyness=(strike_or_moneyness - current_underlying_price) / current_underlying_price
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


def fit(strikes, bid_ivs, ask_ivs, underlying_price, weighted=False) -> IvCurve:
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

    left_tail, right_tail = __prefit_linear_tails__(x, ivs, bid_ivs, ask_ivs)
    x_l = left_tail[0]
    x_r = right_tail[0]
    idx = np.where((x_l <= x) & (x <= x_r))
    x_center = x[idx]
    y_center = ivs[idx]
    # w_center = 1 / self.errors[idx]
    # w_center = w_center / w_center.sum()
    spl = splrep(x_center, y_center, k=3, s=0.025)  # , w=w_center
    (knots, coeffs, k_fact) = spl
    unique_knots = list(set(knots))
    unique_knots.sort()
    yy = splev(unique_knots, spl)
    yy[0] = np.polyval(left_tail[1], unique_knots[0])
    yy[-1] = np.polyval(right_tail[1], unique_knots[-1])
    bc_type = ((1, left_tail[1][0]), (1, right_tail[1][0]))
    cs = CubicSpline(unique_knots, yy, bc_type=bc_type)
    return IvCurve(left_tail, cs, right_tail)


def __prefit_linear_tails__(x, ivs, bid_ivs, ask_ivs):
    """
    Предварительный фиттинг хвостов линейной функцией
    :return:
    """
    left_tail = __prefit_linear_tail__(x, ivs, bid_ivs, ask_ivs)
    right_tail = __prefit_linear_tail__(-1 * np.flip(x), np.flip(ivs),
                                        np.flip(bid_ivs), np.flip(ask_ivs))
    right_tail = (-1 * right_tail[0], (-1 * right_tail[1][0], right_tail[1][1]))
    return left_tail, right_tail


def __prefit_linear_tail__(X, Y, bid_ivs, ask_ivs):
    linear_tail_start = None
    tail_length_limit = math.floor(X.size / 4)
    p_result = None
    for tail_length in range(2, tail_length_limit):
        x = X[:tail_length]
        y = Y[:tail_length]
        bids = bid_ivs[:tail_length]
        asks = ask_ivs[:tail_length]
        err = asks - bids
        w = 1 / err
        w = w / w.sum()
        p = np.polyfit(x, y, deg=1, w=w)
        yy = np.polyval(p, x)
        success, edge = __check_linear_fit__(x, yy, bids, asks)

        if success:
            linear_tail_start = edge
            p_result = p
        else:
            break

    return linear_tail_start, p_result


def __check_linear_fit__(x, y, bids, asks):
    result = True
    tail_start = None
    for i in range(0, x.size):
        tail_start = x[i]
        if y[i] < bids[i] or y[i] > asks[i]:
            result = False
            break
    return result, tail_start
