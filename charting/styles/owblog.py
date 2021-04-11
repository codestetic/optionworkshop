import pathlib

from matplotlib import pyplot as pp

file_path = pathlib.Path.joinpath(pathlib.Path(__file__).parent.absolute(), 'owblog.mplstyle')
pp.style.use(file_path)

exp_line_color = '#333333'
exp_line_style = '--'
exp_line_width = 3

exp_line = {'c': exp_line_color,
            'linewidth': exp_line_width,
            'linestyle': exp_line_style
            }

iv_marker_bid_style = '^'
iv_marker_ask_style = 'v'
iv_marker_alpha = 0.5
iv_marker_size = 5

iv_marker = {
    'markersize': iv_marker_size,
    'alpha': iv_marker_alpha,
    'linewidth': 0
}
