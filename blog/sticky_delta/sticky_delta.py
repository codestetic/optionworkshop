import matplotlib.pyplot as plt
from charting.styles import owblog as stl
from common.execution import *
from marketcontext import *
from pricing import wrappers as pw, PricingContext
import pricing.models.black as black76


# market = MarketContext('ES', 'CL_20210517_20210322_1530.xls', options_dte=56)
market = MarketContext('ES', 'ES_20210618_20210302_1650.xls', options_dte=108)
context = PricingContext(market, time=108/365)

fut = market.underlying.futures[0]
series = fut.options[0]
strikes = series.strikes

strike1 = series.gns(fut.price, -1)
strike2 = series.gns(fut.price, 1)
options = [series.calls[strike1], series.calls[strike2]]

n_options = 1

iv = context.iv(options[0].strike, fut.price)
tp = pw.price(options[0], context, fut.price, 108/365)

print(fut.price, options[0].strike, iv, tp, options[0].bid, options[0].ask)
exit(1)

pos1 = Position(options[0], quantity=n_options, price=pw.price(options[0], context, fut.price))
pos2 = Position(options[1], quantity=-n_options, price=pw.price(options[1], context, fut.price))
pos_fut = Position(fut, +1, strikes[0])

strategy = Portfolio('strangle')
strategy.add_position(pos1)
strategy.add_position(pos2)
# strategy.add_position(pos_fut)

x = np.arange(fut.price*0.95, fut.price*1.05, 1)
price, pnl, exp_pnl = pw.risk_profile(strategy, x, context)

# context.current_underlying_price = strikes[0]
# price1, pnl1, exp_pnl1 = pp.risk_profile(strategy, x, context)

# ivs = context.iv_curve.iv(strikes, fut.price)
# plt.plot(strikes, ivs)
# plt.grid(True)
# plt.show()
# exit(1)

plt.plot(x, pnl)
# plt.plot(x, pnl1)
plt.plot(x, exp_pnl, **stl.exp_line)
plt.grid(True)
plt.axhline(linewidth=0.5, color='k')
# plt.vlines(fut.price, ymin=-10, ymax=10)
plt.show()
