import pandas as pd


def load_series_from_xls(data_file_path: str, clean_zeros: bool = False):
    """
    Loads option series data exported from the OptionWorkshop into xls file via DDE
    :param data_file_path: Path to xls file
    :param clean_zeros: Remove zeros and NaNs from initial data
    :return:
    """
    options_data = pd.read_excel(data_file_path, sheet_name="options")

    calls = options_data[['Strike', 'CallAsk', 'CallBid', 'CallAskVolatility', 'CallBidVolatility']] \
        .rename(columns={'Strike': 'strike',
                         'CallAsk': 'ask',
                         'CallBid': 'bid',
                         'CallAskVolatility': 'ask_iv',
                         'CallBidVolatility': 'bid_iv'
                         })

    puts = options_data[['Strike', 'PutAsk', 'PutBid', 'PutAskVolatility', 'PutBidVolatility']] \
        .rename(columns={'Strike': 'strike',
                         'PutAsk': 'ask',
                         'PutBid': 'bid',
                         'PutAskVolatility': 'ask_iv',
                         'PutBidVolatility': 'bid_iv'
                         })

    if clean_zeros:
        calls = calls[(calls.ask != 0) & (calls.bid != 0)]
        calls = calls[(calls.ask_iv != 0) & (calls.bid_iv != 0)]
        puts = puts[(puts.ask != 0) & (puts.bid != 0)]
        puts = puts[(puts.ask_iv != 0) & (puts.bid_iv != 0)]

    underlying_data = pd.read_excel(data_file_path, sheet_name="underlying")

    underlying = underlying_data[['Underlying']].rename(columns={'Underlying': 'underlying'})

    return calls, puts, underlying.underlying[0]
