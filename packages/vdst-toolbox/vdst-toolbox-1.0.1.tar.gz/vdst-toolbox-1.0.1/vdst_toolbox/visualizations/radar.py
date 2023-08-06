# encoding: windows-1254

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import math


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.1f%s' % (num, ['', 'K', 'M'][magnitude])

def _scale_data(data, ranges):
    (x1, x2) = ranges[0]
    d = data[0]
    return [(d - y1) / (y2 - y1) * (x2 - x1) + x1 for d, (y1, y2) in zip(data, ranges)]

class RadarChart():
    def __init__(self, df, i_cols = 3,font_size = 22,n_ordinate_levels = 6, min_max=False):
        self.min_max = min_max
        self.df = df
        self.font_size = font_size
        self.i_cols = i_cols
        self.n_ordinate_levels = n_ordinate_levels

    def plot(self, data, *args, **kw):
        font_size = self.font_size
        sdata = _scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    def scatter_plot(self, data, *args, **kw):
        font_size = self.font_size
        sdata = _scale_data(data, self.ranges)
        self.ax.scatter(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

    def legend(self, *args, **kw):
        self.ax.legend(*args, **kw)
        
    def title(self, title, *args, **kw):
        self.ax.text(0.9, 1, title, transform = self.ax.transAxes, *args, **kw)

    def create_chart(self):
        print('Chart initialized...')

        if self.min_max:
            try:
                df = self.df.swaplevel(axis=1)
            except TypeError:
                raise TypeError(
                    """
-------- min - max colums not found -------

DataFrame Object should have the following structure:



        Rakip/Vestel                 Marka_Çe?itlili?i               Vestel_Oran?               AB_Grubu               TP_Grubu               ?l_Statüsü              
                 min   max      mean               min max      mean          min max      mean      min max      mean      min max      mean        min max      mean
cluster                                                                                                                                                               
0           1.000000  10.0  3.614638                 1   4  2.857143            1   2  1.158730        1   3  2.174603        0   6  2.433862          1   3  2.449735
1           0.000000   0.5  0.011944                 0   1  0.026059            3   4  3.973941        1   2  1.599349        0   3  0.723127          1   3  1.628664
2           0.333333   5.0  1.428962                 1   4  1.477752            1   3  2.011710        1   2  1.782201        0   3  0.871194          1   3  1.629977
3           0.000000   2.0  1.040026                 0   3  1.228346            2   4  2.496063        2   3  2.173228        0   5  2.551181          2   3  2.818898
"""
                )
                
            df_min = df['min']
            df_max = df['max']
            df = df['mean']
            ranges = [[0, math.ceil(round(df_max[i].max(), -math.ceil(math.log10(df_max[i].max())) + 2) *.1 + round(df_max[i].max(), -math.ceil(math.log10(df_max[i].max())) + 2))] for i in df.columns]

        else:
            df = self.df
            ranges = [[0, math.ceil(round(df[i].max(), -math.ceil(math.log10(df[i].max())) + 2) *.1 + round(df[i].max(), -math.ceil(math.log10(df[i].max())) + 2))] for i in df.columns]

        font_size = self.font_size
        n_ordinate_levels = self.n_ordinate_levels
        index  = df.index.tolist()
        attributes = df.columns.tolist()
        matplotlib.rcParams.update({'font.size': font_size})

        fig = plt.figure(figsize=(28, 50))
        n_groups = len(index)
        i_cols = self.i_cols
        i_rows = n_groups//i_cols
        size_x, size_y = (1/(i_cols)), (1/(i_rows))
        size_x, size_y = 0.6, 0.3

        for ind in range(n_groups):
            ix = ind%i_cols ; iy = i_rows - ind//i_cols
            pos_x = ix*(size_x + 0.05) ; pos_y = iy*(size_y + 0.05)            
            location = [pos_x, pos_y]  ; sizes = [size_x, size_y]
            variables = df.columns
            angles = np.arange(0, 360, 360./len(variables))

            ix, iy = location[:] ; size_x, size_y = sizes[:]
            axes = [fig.add_axes([ix, iy, size_x, size_y], polar = True, 
            label = "axes{}".format(i)) for i in range(len(variables))]

            _, text = axes[0].set_thetagrids(angles, labels = variables)
            for txt, angle in zip(text, angles):
                if angle > -1 and angle < 181:
                    txt.set_rotation(angle - 90)
                else:
                    txt.set_rotation(angle - 270)

                if txt.get_text() in attributes:
                    txt.set_position((txt.get_position()[0] - 0.1, txt.get_position()[1] - 0.1))
                    #print(dir(txt))
                    txt.set_weight('bold')
                    

            for ax in axes[1:]:
                ax.patch.set_visible(False)
                ax.xaxis.set_visible(False)
                ax.grid("off")
            
            for i, ax in enumerate(axes):
                grid = np.linspace(*ranges[i],num = n_ordinate_levels)
                grid_label = [""]+[human_format(x).replace('.0', '') for x in grid[1:]]
                ax.set_rgrids(grid, labels = grid_label, angle = angles[i])
                ax.set_ylim(*ranges[i])
            
            self.angle = np.deg2rad(np.r_[angles, angles[0]])
            self.ranges = ranges
            self.ax = axes[0] 
            #______________________________________________________
            data = np.array(df.loc[index[ind], attributes])

            self.plot(data, color = 'b', linewidth=2.0)
            self.fill(data, alpha = 0.2, color = 'b')
            if self.min_max:
                s = 250
                data_max = np.array(df_max.loc[index[ind], attributes])
                data_min = np.array(df_min.loc[index[ind], attributes])   
                self.scatter_plot(data_max, color = 'g', marker="^", s=s)
                self.scatter_plot(data_min, color = 'r', marker="v", s=s)
            self.title(title = 'cluster nº{}'.format(index[ind]), color = 'r')
            ind += 1