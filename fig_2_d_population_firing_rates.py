# fig_2_d_population_firing_rate.py --- 
# 
# Filename: fig_2_d_population_firing_rate.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Fri Dec 18 16:45:25 2015 (-0500)
# Version: 
# Package-Requires: ()
# Last-Updated: Sun Jan 10 15:51:32 2016 (-0500)
#           By: subha
#     Update #: 26
# URL: 
# Doc URL: 
# Keywords: 
# Compatibility: 
# 
# 

# Commentary: 
# 
# 
# 
# 

# Change Log:
# 
# 
# 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
# 
# 

# Code:

import numpy as np
import pylab as plt

from traubdata import TraubData
from trbhist import get_spiketime_hist
from util import makepath, smooth_gaussian
from config import cellcolor

plt.rc('font', size=12)
#plt.rc('figure', figsize=(3, 2))  # ineffective

from fig_2_b_spike_raster import datafile_figure_2b #= 'data_20140724_125424_236053_compute-0-2.local.h5' # normally distributed synaptic conductance

if __name__ == '__main__':
    figfilename = 'figures/Figure_2D_population_firing_rates.svg'
    binsize=5e-3
    binsize = 5e-3
    trange = (2, 20)
    data = TraubData(makepath(datafile_figure_2b))
    celltypes = ['SpinyStellate', 'DeepBasket', 'DeepLTS']
    fig = plt.figure(figsize=(3, 2))
    ax = fig.add_subplot(111)
    for celltype in celltypes:
        y, bins = get_spiketime_hist(data, celltype,
                                        timerange=trange, binsize=binsize,
                                        percell=True, pertime=True, density=False)
        y = smooth_gaussian(y, binsize=binsize, twindow=50e-3, std=1.0)
        ax.plot((bins[1:] + bins[:-1]) * 0.5, y, color=cellcolor[celltype])
    ax.set_xlabel('Time (s)')
    ax.set_xlim((5, 8))
    ax.set_ylabel('Firing rate (Hz)')
    ax.set_yticks((0, 100, 200))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_xticks([5.0, 6.0, 7.0, 8.0])
    # plt.setp(plt.gca(), frame_on=False)
    #plt.tight_layout()
    fig.savefig(figfilename, transparent=True)
    plt.show()

# 
# fig_2_d_population_firing_rate.py ends here
