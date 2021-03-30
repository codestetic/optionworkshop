import numpy as np


def convert_strikes_to_moneyness(strikes, underlying_price):
    """
    Converts strikes array into moneyness
    :param strikes:
    :param underlying_price: Current price of the options underlying instrument
    :return:
    """
    return np.array((strikes - underlying_price) / underlying_price)


def calculate_mids_and_errors(bid_ivs, ask_ivs):
    """
    Returns
    :param bid_ivs: Bids implied volatylities
    :param ask_ivs: Asks implied volatylities
    :return:
    """
    return np.array((ask_ivs + bid_ivs) / 2), np.array(ask_ivs - bid_ivs)
