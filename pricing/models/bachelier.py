from typing import Union, Iterable

from common.instruments import *
from .primitives import *


def bachelier(option_type: OptionType, strike: float, time_to_exp: float,
              iv: float, und_price: Union[np.ndarray, Iterable, float]):
    tsqrt = sqrt(time_to_exp)
    d1 = (und_price - strike) / (iv * tsqrt)

    if option_type is OptionType.CALL:
        return (und_price - strike) * cnd(d1) + iv * tsqrt * nd(d1)
    elif option_type is OptionType.PUT:
        return (strike - und_price) * cnd(-d1) + iv * tsqrt * nd(d1)
