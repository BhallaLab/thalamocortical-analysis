# figure_2_b_rate_distr.py --- 
# 
# Filename: figure_2_b_rate_distr.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Thu Jun 26 14:44:23 2014 (+0530)
# Version: 
# Last-Updated: Fri Dec 18 12:04:05 2015 (-0500)
#           By: Subhasis Ray
#     Update #: 10
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

"""Plots firing rate distribution in cells when simulated without
synaptic connections.

"""

from collections import defaultdict
import numpy as np
import pylab as plt

from traubdata import TraubData
from trbhist import get_spiketime_hist
from util import makepath, smooth_gaussian, get_filenames
from config import cellcolor

plt.rc('font', size=12)
plt.rc('figure', figsize=(3, 2.5))

CELLTYPES = ['SpinyStellate', 'DeepBasket', 'DeepLTS']

def old_main():
    figfilename = 'Figure_2B.svg'
    trange = (2, 20)
    filename = 'data_20140423_101740_1735.h5'
    data = TraubData(makepath(filename))
    rates = defaultdict(list)
    
    counts = data.cellcounts._asdict()
    for celltype in counts.keys():
        if counts[celltype] == 0:
            counts.pop(celltype)
            continue
        for cell, spiketrain in data.spikes.items():
            if cell.startswith(celltype):
                rate = 1.0 * np.count_nonzero((spiketrain > trange[0]) & \
                                              (spiketrain < trange[1])) \
                    / (trange[1] - trange[0])
                rates[celltype].append(rate)
    rates.pop('TCR')
    bins = np.arange(0, 61.0, 5.0)
    print 'bins:', bins
    hists = {}
    prev = np.zeros(len(bins)-1)
    ax = None
    # plt.axis('off')
    for ii, celltype in enumerate(reversed(rates.keys())):        
        ctype_rates = rates[celltype]
        ax = plt.subplot(len(rates), 1, ii+1, sharex=ax, sharey=ax)
        h, b = np.histogram(ctype_rates, bins=bins)
        h = np.asarray(h, dtype='float64') / counts[celltype]
        x = bins[:-1]
        plt.bar(x,
                h,
                color=cellcolor[celltype],
                width=(bins[1]-bins[0]))
                # bottom = prev, color=cellcolor[celltype], label=celltype)
        prev += h        
        ax.tick_params(axis='y', right=False, left=False)
        # plt.setp(ax, frame_on=False)
        ax.tick_params(axis='x', top=False, bottom=True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.spines['bottom'].set_color((0, 0, 0, 0))
        # ax.xaxis.set_visible(False)
    # ax.xaxis.set_visible(True)
    ax.set_xticks(bins[::2])
    ax.set_yticks([0, 1.0])
    ax.tick_params(axis='y', left=True)
    plt.xlabel('Firing rate (Hz)')
    plt.tight_layout()
    plt.savefig(figfilename)
    plt.show()
    

def multifile_firing_rate_distribution(flist='unconnected_network.csv',
                                                   figfilename='Figure_3B.svg', trange=(2,20)):
    """Plots histograms showing distribution of firing rates among cells
    of each type collected from multiple simulations.

    """
    start = trange[0]
    end = trange[1]
    rates = defaultdict(list)    
    for fname in get_filenames(flist):
        data = TraubData(makepath(fname))
        if data.simtime < end:
            end = data.simtime
        for celltype in CELLTYPES:
            for cell, spiketrain in data.spikes.items():
                if cell.startswith(celltype):
                    rate = 1.0 * np.count_nonzero((spiketrain > start) & (spiketrain < end)) / (end - start)
                    rates[celltype].append(rate)
    bins = np.arange(0, 61.0, 5.0)
    hists = {}
    prev = np.zeros(len(bins) - 1)
    ax = None
    for ii, celltype in enumerate(CELLTYPES):
        ctype_rates = rates[celltype]
        ax = plt.subplot(len(rates), 1, ii+1, sharex=ax, sharey=ax)
        h, b = np.histogram(ctype_rates, bins=bins)
        h = np.asarray(h, dtype='float64') / len(ctype_rates)
        x = bins[:-1]
        plt.bar(x,
                h,
                color=cellcolor[celltype],
                width=(bins[1]-bins[0]))
                # bottom = prev, color=cellcolor[celltype], label=celltype)
        prev += h        
        ax.tick_params(axis='y', right=False, left=False)
        # plt.setp(ax, frame_on=False)
        ax.tick_params(axis='x', top=False, bottom=True)        
        ax.spines['bottom'].set_color((0, 0, 0, 0))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.xaxis.set_visible(False)
    ax.xaxis.set_visible(True)
    ax.set_xticks(bins[::2])
    ax.set_yticks([0, 1.0])
    ax.tick_params(axis='y', left=True)
    plt.xlabel('Firing rate (Hz)')
    plt.tight_layout()
    plt.savefig(figfilename)
    plt.show()

    
if __name__ == '__main__':
    multifile_firing_rate_distribution(figfilename='figures/Figure_3B_unconnected_firing_rates.svg')
    multifile_firing_rate_distribution(flist='connected_norm_for_unconnected_fft.csv',
                                       figfilename='figures/Figure_3B_norm.svg')
    multifile_firing_rate_distribution(flist='connected_lognorm_for_unconnected_fft.csv',
                                       figfilename='figures/Figure_3B_lognorm.svg')
    

# 
# figure_2_b_rate_distr.py ends here
