import os
import sys
from os import path

import numpy as np
import pandas as pd
from matplotlib import pyplot as pp

from charting.styles import owblog as stl
from marketdata import aws
from marketdata.readers.optionworkshop import load_series_from_xls
from pricing.iv import ltcs, polynomial, spline

global market_data_root
global output_path
global image_format
global width

image_format = "svg"
width = 13


def validate_cli_args():
    global market_data_root
    global output_path

    if len(sys.argv) < 3:
        print(f'Please specify path to marketdata folder and output folder for images')
        raise Exception("Wrong args")

    market_data_root = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(market_data_root):
        print(f"Market data folder {market_data_root} doesn't exist")
        raise Exception("Wrong args")

    if not os.path.exists(output_path):
        print(f"Creating output folder {output_path}")
        try:
            os.mkdir(output_path)
        except OSError as err:
            print(f"Failed to create {output_path}. Error message: {err}")
            raise Exception("Wrong args")
        else:
            print(f"Folder {output_path} created")


def get_real_data(asset):
    global market_data_root

    if asset == "ES":
        filepath = aws.download_dataset("ES_20210618_20210302_1650.xls")
        calls, puts, underlying = load_series_from_xls(
            path.join(market_data_root, filepath), True)
    elif asset == "CL":
        filepath = aws.download_dataset("CL_20210517_20210322_1530.xls")
        calls, puts, underlying = load_series_from_xls(path.join(market_data_root, filepath), True)

    options = pd.concat([puts[puts.strike < underlying], calls[calls.strike > underlying]])
    strikes = np.array(options['strike'])
    ask_ivs = np.array(options['ask_iv'])
    bid_ivs = np.array(options['bid_iv'])
    return strikes, bid_ivs, ask_ivs, underlying


def __configure_fig__(fig):
    fig.set_size_inches((width, 1080 * width / 1920), forward=False)


def __plot_extrapolation__(asset, strikes, bid_ivs, ask_ivs, underlying, algo_name, curve):
    global output_path

    fig = pp.figure()
    __configure_fig__(fig)
    pp.grid(True)
    min_strike = min(strikes)
    max_strike = max(strikes)
    xx = np.arange(0.7 * min_strike, 1.2 * max_strike, 0.1)
    iv_f = curve.iv(xx, underlying)
    pp.plot(strikes, bid_ivs, 'g^', strikes, ask_ivs, 'rv', **stl.iv_marker)
    pp.plot(xx, iv_f, 'k--', lw=1)
    pp.xlabel('Strikes')
    pp.ylabel('Volatility')

    if image_format is None:
        pp.show()
    else:
        pp.savefig(f'{output_path}\\volatility-curve-fitting-extrapolated-{algo_name}-{asset}.{image_format}',
                   transparent=False, pad_inches=0.1, bbox_inches='tight')
    pp.close(fig)


def __plot_abstract_charts__(asset, strikes, bid_ivs, ask_ivs, underlying, curve):
    global output_path
    fig = pp.figure()
    __configure_fig__(fig)
    pp.grid(True)

    pp.plot(strikes, bid_ivs, 'g^', strikes, ask_ivs, 'rv', **stl.iv_marker)

    min_strike = min(strikes)
    max_strike = max(strikes)
    xx = np.arange(min_strike, max_strike, 0.1)
    iv_f = curve.iv(xx, underlying)
    pp.plot(xx, iv_f, 'k--', lw=1)
    pp.xlabel('Strikes')
    pp.ylabel('Volatility')

    if image_format is None:
        pp.show()
    else:
        pp.savefig(f'{output_path}\\volatility-curve-fitted-{asset}.{image_format}',
                   transparent=False, pad_inches=0.1, bbox_inches='tight')

    pp.close(fig)


def __plot_basic_charts__(asset, strikes, bid_ivs, ask_ivs, underlying, algo_name, curve):
    global output_path
    fig = pp.figure()
    __configure_fig__(fig)

    ax = [pp.subplot2grid((5, 1), (0, 0), rowspan=4),
          pp.subplot2grid((5, 1), (4, 0), rowspan=1)]

    ax[0].grid(True)
    ax[1].grid(True)
    pp.setp(ax[0].get_xticklabels(), visible=False)
    pp.subplots_adjust(hspace=.1)

    min_strike = min(strikes)
    max_strike = max(strikes)
    xx = np.arange(min_strike, max_strike, 0.1)
    iv_f = curve.iv(xx, underlying)
    iv_f_in_strikes = curve.iv(strikes, underlying)
    iv_real = (ask_ivs + bid_ivs) / 2
    err = iv_f_in_strikes - iv_real

    ax[0].plot(strikes, bid_ivs, 'g^', strikes, ask_ivs, 'rv', **stl.iv_marker)
    ax[0].plot(xx, iv_f, 'k--', lw=1)
    pp.ylabel('Volatility')
    ax[1].plot(strikes, err, 'r.-', lw=1)
    pp.xlabel('Strikes')
    pp.ylabel('Error')

    # fig = pp.gcf()
    dpi = 155
    if image_format is None:
        pp.show()
    else:
        pp.savefig(f'{output_path}\\volatility-curve-fitting-basic_{algo_name}-{asset}.{image_format}',
                   transparent=False, pad_inches=0.1, bbox_inches='tight')

    pp.close(fig)


def main():
    validate_cli_args()

    assets = ["ES", "CL"]
    # assets = ["ES"]

    for asset in assets:
        strikes, bid_ivs, ask_ivs, underlying = get_real_data(asset)

        curves = [
            ("ltcs", ltcs.fit(strikes, bid_ivs, ask_ivs, underlying)),
            ("spline", spline.fit(strikes, bid_ivs, ask_ivs, underlying)),
            ("poly2", polynomial.fit(strikes, bid_ivs, ask_ivs, underlying, poly_degree=2)),
            ("poly5", polynomial.fit(strikes, bid_ivs, ask_ivs, underlying, poly_degree=5))
        ]

        __plot_abstract_charts__(asset, strikes, bid_ivs, ask_ivs, underlying, curves[0][1])

        for algo_name, curve in curves:
            pass
            __plot_basic_charts__(asset, strikes, bid_ivs, ask_ivs, underlying, algo_name, curve)
            __plot_extrapolation__(asset, strikes, bid_ivs, ask_ivs, underlying, algo_name, curve)


if __name__ == "__main__":
    main()
