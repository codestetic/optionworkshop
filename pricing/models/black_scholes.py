from .primitives import *
from common import *


def bs(option_type: OptionType, underlying_price: float, strike: float, time_to_exp: float, interest_rate: float,
       iv: float) -> tuple:
    try:
        if time_to_exp == 0:
            if option_type == 'c':
                return max(0, underlying_price - strike)
            else:
                return max(0, strike - underlying_price)

        d1 = (log(underlying_price / strike) + (interest_rate + iv * iv / 2.) * time_to_exp) / (iv * sqrt(time_to_exp))
        d2 = d1 - iv * sqrt(time_to_exp)
        if option_type == 'c':
            return underlying_price * cnd(d1) - strike * exp(-interest_rate * time_to_exp) * cnd(d2)
        else:
            return strike * exp(-interest_rate * time_to_exp) * cnd(-d2) - underlying_price * cnd(-d1)

    except Exception as exception:
        print('Error in Black-Scholes formula: {0}'.format(exception))
        return None
