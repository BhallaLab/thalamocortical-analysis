# fig_4_d_psth_plots_with_GABA_scale.py --- 
# 
# Filename: fig_4_d_psth_plots_with_GABA_scale.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Sun Jan 10 21:58:14 2016 (-0500)
# Version: 
# Last-Updated: Sun Jan 17 16:44:39 2016 (-0500)
#           By: subha
#     Update #: 160
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
# 
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
import os
import numpy as np
from collections import defaultdict
import matplotlib as mpl
import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import util
# from peakdetect import peakdetect
from util import get_filenames, makepath, get_dbcnt_dict, psth, get_stim_times
from traubdata import TraubData
from scipy.stats import mode
from bisect import bisect_left
import csv

from config import CELLTYPES

plt.rc('font', size=12)
plt.rc('figure', figsize=(3, 3))

def get_psth_with_GABA_scale(window, binwidth):
    psthdict = defaultdict(dict)
    bins = np.arange(-window/2, window/2+0.5 * binwidth, binwidth)
    with open('gaba_scaling.csv', 'r') as fd:
        reader = csv.DictReader(fd, delimiter='\t')
        for row in reader:
            fname = row['filename']
            if (not fname) or fname.strip().startswith('#'):
                continue
            try:
                data = TraubData(makepath(fname))
                bgtimes, probetimes = get_stim_times(data)
                stim_times = np.concatenate((bgtimes, probetimes))
                stim_times.sort()
                gaba = dict(data.fdata['/runconfig/GABA'])
                gaba_scale = float(gaba['conductance_scale'])                
                pop_spike_times = []
                for cell, spikes in data.spikes.items():
                    if not cell.startswith('SpinyStellate'):
                        continue
                    pop_spike_times.append(spikes)
                pop_spike_times = np.concatenate(pop_spike_times)
                pop_spike_times.sort()
                psth_, b = psth(pop_spike_times, stim_times, window=window, bins=bins)
                psthdict[gaba_scale][fname] = psth_
            except IOError as e:
                print(fname, e)
    return psthdict, bins

if __name__ == '__main__':
    fname = 'gabascale_psth_200.0ms_window_5.0ms_bins.csv'    
    if os.path.exists(fname):
        with open(fname, 'r') as fd:
            reader = csv.DictReader(fd)
            bins = [float(v)*1e-3 for v in reader.fieldnames[2:]] 
            bins.append(bins[-1] + bins[-1] - bins[-2])
            psthdict = defaultdict(dict)
            for row in reader:
                gabascale = float(row['gaba_scale'])
                dfile = row['filename']
                psthdict[gabascale][dfile] = [float(row[v]) for v in reader.fieldnames[2:]]
    else:
        psthdict, bins = get_psth_with_GABA_scale(200e-3, 5e-3)        
        with open(fname, 'w') as fd:
            writer = csv.writer(fd)
            header = [ 'gaba_scale', 'filename'] + [b * 1e3 for b in bins[:-1]]
            writer.writerow(header)
            for ii, gabascale in enumerate(sorted(psthdict.keys())):
                for fname, psth in psthdict[gabascale].items():
                    row = [gabascale, fname] + [v for v in psth]
                    writer.writerow(row)
    fig = plt.figure()
    ax = None
    bins = np.array(bins)
    for ii, gabascale in enumerate(sorted(psthdict.keys())):
        ax = fig.add_subplot(len(psthdict), 1, ii+1, sharex=ax, sharey=ax)
        for fname, psth in psthdict[gabascale].items():
            row = [gabascale, fname] + [v for v in psth]
            ax.plot(1e3*(bins[1:]+bins[:-1])/2.0, psthdict[gabascale][fname], 'k-', alpha=0.3)
            ax.set_yticks((0, 200))
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.xaxis.set_visible(False)
            ax.xaxis.tick_bottom()
            ax.yaxis.tick_left()
    ax.xaxis.set_visible(True)
    ax.set_xlabel('Time since stimulus (ms)')
    ax.set_ylabel('Population firing rate')
    fig.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.2, hspace=0.5)
    fig.savefig('figures/Figure_4D_psth_plots_with_GABA_scale.svg', transparent=True)
    plt.show()

# 
# fig_4_d_psth_plots_with_GABA_scale.py ends here
