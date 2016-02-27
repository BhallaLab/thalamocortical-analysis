# fig_4_a_low_gaba_spike_raster.py --- 
# 
# Filename: fig_4_a_low_gaba_spike_raster.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Sat Jan  2 17:29:18 2016 (-0500)
# Version: 
# Last-Updated: Sun Jan 10 15:53:58 2016 (-0500)
#           By: subha
#     Update #: 19
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

import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from util import makepath
from config import cellcolor, mdict
from plotutil import plot_spike_raster
from traubdata import TraubData, cellcount_tuple
from matplotlib import rc

rc('font', size=12)
rc('figure', figsize=(3, 4))

if __name__ == '__main__':
    datafile = 'data_20141026_001929_36071_compute-0-59.local.h5' # 0.6x

    figfilename='figures/Figure_4A_spike_raster_low_GABA.png'
    fig, ax = plot_spike_raster(makepath(datafile), (5, 8))
    # fig.tight_layout()
    fig.savefig(figfilename, transparent=True)
    print 'Saved figure in %s' % (figfilename)
    plt.show()



# 
# fig_4_a_low_gaba_spike_raster.py ends here
