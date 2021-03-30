from numpy import polyfit, polyval

from .common import convert_strikes_to_moneyness, calculate_mids_and_errors


class IvCurve:
    def __init__(self, p):
        self.p = p

    def iv(self, strike_or_moneyness, current_underlying_price=None) -> float:
        if current_underlying_price is not None:
            strike_or_moneyness = (strike_or_moneyness - current_underlying_price) / current_underlying_price
            return self.iv(strike_or_moneyness)
        else:
            return polyval(self.p, strike_or_moneyness)


def fit(strikes, bid_ivs, ask_ivs, underlying_price, poly_degree=2, weighted=False) -> IvCurve:
    """
    Фитит рыночные значения волатильностей полиномиальной кривой
    :param strikes:
    :param bid_ivs:
    :param ask_ivs:
    :param underlying_price:
    :param weighted:
    :return:
    """
    strikes_m = convert_strikes_to_moneyness(strikes, underlying_price)
    mids, errors = calculate_mids_and_errors(bid_ivs, ask_ivs)
    p = polyfit(strikes_m, mids, deg=poly_degree)
    return IvCurve(p)
