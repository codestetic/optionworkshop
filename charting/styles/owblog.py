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

rp_line_colors = ['#']
