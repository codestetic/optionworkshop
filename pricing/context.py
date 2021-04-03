from datetime import datetime

from pricing.models import black


class PricingContext:
    def __init__(self, iv_curve: object, time: datetime = None, current_underlying_price: float = None, model: object = None):
        self.time = datetime.now() if time is None else time
        self.model = black if model is None else model
        self.iv_curve = iv_curve
        self.current_underlying_price = current_underlying_price

    def iv(self, strike_or_moneyness, current_underlying_price=None):

        cup = self.current_underlying_price if self.current_underlying_price is not None else current_underlying_price
        return self.iv_curve.iv(strike_or_moneyness, cup)
