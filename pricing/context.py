from typing import Union

from marketcontext import *
from pricing.iv import ltcs
from pricing.iv.common import iv
from pricing.models import black


class PricingContext:
    def __init__(self, market: MarketContext, time: datetime = None, current_underlying_price: float = None,
                 model: object = None):
        self.time = datetime.now() if time is None else time
        self.model = black if model is None else model

        self.current_underlying_price = current_underlying_price
        self.iv_curves = {}

        for fut in market.underlying.futures:
            for os in fut.options:
                bid_ivs = []
                ask_ivs = []

                for strike in os.strikes:
                    option = os.puts[strike] if strike <= fut.price else os.calls[strike]
                    ivs = iv(option, [option.bid, option.ask], fut.price, self.model, time)
                    bid_ivs.append(ivs[0])
                    ask_ivs.append(ivs[1])

                self.iv_curves[os] = ltcs.fit(os.strikes, bid_ivs, ask_ivs, fut.price)

    def iv(self, strike_or_moneyness, current_underlying_price=None, option_or_series: Union[Option, OptionSeries] = None):

        if option_or_series is None:
            iv_curve = next(iter(self.iv_curves.values()))
        elif isinstance(option_or_series, OptionSeries):
            iv_curve = self.iv_curves[option_or_series]
        elif isinstance(option_or_series, Option):
            iv_curve = self.iv_curves[option_or_series.series]

        cup = self.current_underlying_price if self.current_underlying_price is not None else current_underlying_price
        return iv_curve.iv(strike_or_moneyness, cup)
