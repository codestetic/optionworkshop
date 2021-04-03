from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd

from common.execution import *
from common.instruments import *
from marketdata import aws
from marketdata.readers import optionworkshop as ow
from pricing import portfolio as pp, PricingContext
from pricing.iv import ltcs

filepath = aws.download_dataset(file_name='ES_20210618_20210302_1650.xls')
calls, puts, underlying = ow.load_series_from_xls(filepath, True)

options = pd.concat([puts[puts.strike < underlying], calls[calls.strike > underlying]])
strikes = np.array(options['strike'])
ask_ivs = np.array(options['ask_iv']) / 100
bid_ivs = np.array(options['bid_iv']) / 100
iv_curve = ltcs.fit(strikes, bid_ivs, ask_ivs, underlying)

context = PricingContext(iv_curve)

und = Underlying("ES")
fut = Futures(und, datetime.now() + timedelta(days=60))
strikes = [4005, 4010]
series = OptionSeries(fut, strikes, datetime.now() + timedelta(days=30))

n_options = 1
pos1 = Position(series.calls[strikes[0]], n_options, 65)
pos2 = Position(series.calls[strikes[1]], -n_options, 62)
pos_fut = Position(fut, +1, strikes[0])

strategy = Portfolio('strangle')
strategy.add_position(pos1)
strategy.add_position(pos2)
# strategy.add_position(pos_fut)

x = np.arange(3800, 4200, 1)
price, pnl, exp_pnl = pp.risk_profile(strategy, x, context)

context.current_underlying_price = strikes[0]
price1, pnl1, exp_pnl1 = pp.risk_profile(strategy, x, context)

plt.plot(x, pnl, x, pnl1, x, exp_pnl)
plt.grid(True)
plt.show()
