from datetime import timedelta

import pandas as pd

from common.instruments import *
from marketdata import aws
from marketdata.readers import optionworkshop as ow


class MarketContext:
    def __init__(self, asset_code,
                 data_file_path,
                 futures_dte=60,
                 options_dte=30
                 ):
        filepath = aws.download_dataset(file_name=data_file_path)
        calls, puts, underlying_price = ow.load_series_from_xls(filepath, True)

        strikes = sorted(set(calls['strike'].tolist() + puts['strike'].tolist()))

        self.underlying = Underlying(asset_code)
        self.underlying.futures = []

        fut = Futures(self.underlying, datetime.now() + timedelta(days=futures_dte))
        fut.price = underlying_price

        self.underlying.futures.append(fut)

        self.underlying.futures[0].options = []

        series = OptionSeries(fut, strikes, datetime.now() + timedelta(days=options_dte))

        self.underlying.futures[0].options.append(series)

        for i, row in calls.iterrows():
            strike = row.strike
            if strike not in strikes:
                continue
            series.calls[strike].bid = row.bid
            series.calls[strike].ask = row.ask
            series.calls[strike].mid = 0.5 * (row.bid + row.ask)

        for i, row in puts.iterrows():
            strike = row.strike
            if strike not in strikes:
                continue
            series.puts[strike].bid = row.bid
            series.puts[strike].ask = row.ask
            series.puts[strike].mid = 0.5 * (row.bid + row.ask)
