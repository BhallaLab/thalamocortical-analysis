# fig_5_b_spikeraster_30DB.py --- 
# 
# Filename: fig_5_b_spikeraster_30DB.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Mon Jan 11 01:44:51 2016 (-0500)
# Version: 
# Last-Updated: Mon Jan 11 02:02:21 2016 (-0500)
#           By: subha
#     Update #: 7
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

from collections import defaultdict
import numpy as np
import pylab as plt
from util import makepath
from traubdata import TraubData
from trbhist import get_spiketime_hist
from util import makepath, smooth_gaussian
from config import cellcolor
from plotutil import plot_spike_raster

plt.rc('font', size=12)
plt.rc('figure', figsize=(3, 4))

data_filename = 'data_20140724_125424_3938_compute-0-1.local.h5'

if __name__ == '__main__':
    figfilename = 'figures/Figure_5A_spikeraster_30DB.png'
    trange = (5, 8)
    fig, ax = plot_spike_raster(makepath(data_filename), trange)
    plt.savefig(figfilename, transparent=True)
    plt.show()



# 
# fig_5_b_spikeraster_30DB.py ends here
