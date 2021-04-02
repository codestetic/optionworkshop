# -*- coding: utf-8 -*-
from datetime import datetime


class Instrument:
    def __init__(self, code: str, expiration: datetime, parent=None):
        self.code = code
        self.parent = parent
        self.expiration = expiration

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not (self == other)


class Underlying(Instrument):

    def __init__(self, code: str, expiration: datetime) -> None:
        Instrument.__init__(self, code, expiration)


class Equity(Underlying):

    def __init__(self, code: str):
        Underlying.__init__(self, code)


class Futures(Underlying):

    def __init__(self, code: str, expiration: datetime):
        Underlying.__init__(self, code, expiration)
        self.expiration = expiration

    def __str__(self):
        return self.code


class OptionSeries:
    code_format_string = '{0}-{1:%Y%m%d}'

    def __init__(self, underlying: Underlying, strikes: np.array, expiration: datetime) -> None:
        self.strikes = strikes
        self.expiration = expiration
        self.underlying = underlying
        self.code = OptionSeries.code_format_string.format(underlying.code, expiration)
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

    def __str__(self):
        return self.code


class Call(Option):

    def __init__(self, series: OptionSeries, strike: float):
        Option.__init__(self, series, strike,
                        Option.code_format_string.format(series.underlying.code, 'C', strike, series.expiration))


class Put(Option):

    def __init__(self, series: OptionSeries, strike: float):
        Option.__init__(self, series, strike,
                        Option.code_format_string.format(series.underlying.code, 'P', strike, series.expiration))
