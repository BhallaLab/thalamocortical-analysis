# figure_6_a_psth_with_dbcount.py --- 
# 
# Filename: figure_6_a_psth_with_dbcount.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Wed Oct 22 14:55:13 2014 (+0530)
# Version: 
# Last-Updated: Sun Jan 17 17:37:38 2016 (-0500)
#           By: subha
#     Update #: 295
# URL: 
# Keywords: 
# Compatibility: 
# 
# 


# Commentary: 
# 
# 
# 
# 

# Change log:
# 
# Sat, May 09, 2015  4:01:05 PM - Updated to use csv dump of PSTH in
# the 100 ms window.
# 
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 
# 

# Code:
"""Plots the PSTH peaks with changing DeepBasket count."""
import numpy as np
from collections import defaultdict
import matplotlib as mpl
import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import util
# from peakdetect import peakdetect
from util import get_filenames, makepath, get_dbcnt_dict, psth
from traubdata import TraubData
from util import get_stim_times
from scipy.stats import mode
from bisect import bisect_left

plt.rc('font', size=10)
plt.rc('figure', figsize=(17.35/2.54/3, 2*23.35/2.54/3))
# plt.rc('figure', figsize=(20, 15))

CELLTYPES = ['SpinyStellate', 'DeepBasket', 'DeepLTS']
from plotutil import get_psth_with_dbcount

def plot_psth_with_dbcount_from_csv(psthfile, figfilename='Figure_4C_1.svg', palette='Blues', yticks=None, xticks=None):
    data = pd.read_csv(psthfile)
    bin_ends = [float(col) for col in data.columns[2:]]
    header = [col for col in data.columns[:2]] + [str(val) for val in bin_ends]
    data.columns = header
    dbcnt_bg_ax = {}
    ax = None
    fig = plt.figure(figfilename)
    dbcounts = sorted(set(data['dbcount']))
    cm = plt.cm.get_cmap(palette)
    for ii, dbcnt in enumerate(dbcounts):
        ax = fig.add_subplot(len(dbcounts), 1, ii+1, axisbg='none')        # sharex=ax, sharey=ax, 
        nplots = len(data[data.dbcount == dbcnt])
        print('dbcount:', dbcnt, 'nplots:', nplots)
        kk = 0
        for jj, row in data[data.dbcount == dbcnt].iterrows():
            hist = row[2:]
            color = cm(0.3+kk*0.7/nplots, 1)
            kk += 1
            ax.plot(bin_ends, hist, alpha=0.6, c=color, lw=1)
        if yticks is not None:
            print(ii, yticks)
            ax.set_yticks(yticks)
        if xticks is not None:
            ax.set_xticks(xticks)
        ax.tick_params(axis='y', right=False)
        ax.tick_params(axis='x', top=False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title('{}'.format(dbcnt))
    fig.tight_layout()
    return data
    # fig.savefig(figfilename)
                    
    
if __name__ == '__main__':
    plot_psth_with_dbcount_from_csv('norm_psth_SpinyStellate_200.0ms_window_5.0ms_bins.csv', figfilename='Figure_7A_normal_psth_SpinyStellate_200ms.svg', palette='Reds', yticks=[0, 50, 100], xticks=[-100, -50, 0, 50, 100])
    plot_psth_with_dbcount_from_csv('norm_psth_DeepBasket_200.0ms_window_5.0ms_bins.csv', figfilename='Figure_7B_normal_psth_DeepBasket_200ms.svg', palette='Blues', yticks=[0, 100,  200], xticks=[-100, -50, 0, 50, 100])
    plot_psth_with_dbcount_from_csv('norm_psth_DeepLTS_200.0ms_window_5.0ms_bins.csv', figfilename='Figure_7C_normal_psth_DeepLTS_200ms.svg', palette='Purples', yticks=[0, 50, 100], xticks=[-100, -50, 0, 50, 100])
    plot_psth_with_dbcount_from_csv('lognorm_psth_SpinyStellate_200.0ms_window_5.0ms_bins.csv', figfilename='lognormal_psth_SpinyStellate_200ms.svg', palette='Reds', yticks=[0, 50, 100], xticks=[-100, -50, 0, 50, 100])
    plt.show()

# 
# figure_6_a_psth_with_dbcount.py ends here
