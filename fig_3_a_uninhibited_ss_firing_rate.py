# figure_2_a_uninhibited.py --- 
# 
# Filename: figure_2_a_uninhibited.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Wed Jun 25 14:40:59 2014 (+0530)
# Version: 
# Last-Updated: Fri Dec 18 16:46:12 2015 (-0500)
#           By: Subhasis Ray
#     Update #: 11
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
"""Plot the spike raster for uninhibited network."""
# files_with_ss_tcr = [
    # "data_20121226_095623_17407.h5", # may have a bug in NMDAChan
    # "data_20121228_091024_22059.h5", # may have a bug in NMDAChan
    # "data_20121230_142445_29596.h5", # may have a bug in NMDAChan
    # "data_20130102_100651_9833.h5",  # may have a bug in NMDAChan
    # "data_20130105_092151_12565.h5", # may have a bug in NMDAChan
    # "data_20130107_175609_8221.h5",    # NMDAChan corrected - use this one.
    # "data_20130110_155030_24082.h5",
    # "data_20130112_093358_3354.h5"

    # "data_20130110_155030_24082.h5'
    # 'data_20140324_123836_31910.h5'
# ]
import numpy as np
import pylab as plt

from traubdata import TraubData
from trbhist import get_spiketime_hist
from util import makepath, smooth_gaussian
from config import cellcolor

plt.rc('font', size=12)
plt.rc('figure', figsize=(3, 2))

uninhibited_filename = 'data_20130107_175609_8221.h5'

if __name__ == '__main__':
    figfilename = 'figures/Figure_3A_uninhibited_firing_rate.svg'
    binsize = 5e-3
    trange = (2, 20)
    filename = 'data_20130107_175609_8221.h5'
    data = TraubData(makepath(uninhibited_filename))
    celltype = 'SpinyStellate'
    y, bins = get_spiketime_hist(data, celltype,
                                    timerange=trange, binsize=binsize,
                                    percell=True, pertime=True, density=False)
    y = smooth_gaussian(y, binsize=binsize, twindow=50e-3, std=1.0)
    plt.plot((bins[1:] + bins[:-1]) * 0.5, y, color=cellcolor[celltype])
    plt.xlabel('Time (s)')
    plt.xlim((5, 7))
    plt.ylabel('Firing rate (Hz)')
    plt.yticks((100, 200, 300))
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().get_xaxis().tick_bottom()
    plt.gca().get_yaxis().tick_left()
    plt.xticks([5.0, 6.0, 7.0])
    # plt.setp(plt.gca(), frame_on=False)

    plt.tight_layout()
    plt.savefig(figfilename)
    plt.show()
    
    


# 
# figure_2_a_uninhibited.py ends here
