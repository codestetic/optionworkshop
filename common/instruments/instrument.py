# -*- coding: utf-8 -*-
from datetime import datetime

import numpy as np

from common.instruments.option_type import *

month_codes = {
    1: "F",
    2: "G",
    3: "H",
    4: "J",
    5: "K",
    6: "M",
    7: "N",
    8: "Q",
    9: "U",
    10: "V",
    11: "X",
    12: "Z"
}


class Instrument:
    def __init__(self, code: str, expiration: datetime = None, parent=None):
        self.code = code
        self.parent = parent
        self.expiration = expiration

    def tte(self):
        if self.expiration is None:
            return None
        return (self.expiration - datetime.now()).total_seconds()/365/24/3600

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not (self == other)


class Underlying(Instrument):

    def __init__(self, code: str, expiration: datetime = None) -> None:
        Instrument.__init__(self, code, expiration)


class Equity(Underlying):

    def __init__(self, code: str):
        Underlying.__init__(self, code)


class Futures(Underlying):

    def __init__(self, underlying: Underlying, expiration: datetime):
        __code_format__ = "{0}{1}{2}"
        self.expiration = expiration
        Underlying.__init__(self, __code_format__.format(underlying.code,
                                                         month_codes[expiration.month],
                                                         expiration.strftime('%y')), expiration)

    def __str__(self):
        return self.code


class OptionSeries:

    def __init__(self, underlying: Underlying, strikes: np.array, expiration: datetime) -> None:
        code_format_string = '{0}-{1:%Y%m%d}'
        self.strikes = strikes
        self.expiration = expiration
        self.underlying = underlying
        self.code = code_format_string.format(underlying.code, expiration)
        self.calls = {}
        self.puts = {}
        for strike in strikes:
            call = Call(self, strike)
            put = Put(self, strike)
            self.calls[strike] = call
            self.puts[strike] = put

    def __str__(self):
        return self.code


class Option(Instrument):
    code_format_string = '{0}-{3:%Y%m%d}-{1}-{2}'

    def __init__(self, series: OptionSeries, strike: float, code: str):
        Instrument.__init__(self, code, series.expiration)
        self.strike = strike
        self.series = series
        self.type = None

    def __str__(self):
        return self.code


class Call(Option):

    def __init__(self, series: OptionSeries, strike: float):
        Option.__init__(self, series, strike,
                        Option.code_format_string.format(series.underlying.code, 'C', strike, series.expiration))
        self.type = OptionType.CALL


class Put(Option):

    def __init__(self, series: OptionSeries, strike: float):
        Option.__init__(self, series, strike,
                        Option.code_format_string.format(series.underlying.code, 'P', strike, series.expiration))
        self.type = OptionType.PUT
