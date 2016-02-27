# fig_2_c_zoomed_Vm.py --- 
# 
# Filename: fig_2_c_zoomed_Vm.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Sat Jan  9 14:45:55 2016 (-0500)
# Version: 
# Last-Updated: Sun Jan 10 15:44:18 2016 (-0500)
#           By: subha
#     Update #: 62
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

"""Show spike times zoomed in time."""

import sys
import numpy as np
from matplotlib import pyplot as plt
from util import makepath
from config import cellcolor, mdict, CELLTYPES

from traubdata import TraubData, cellcount_tuple
from matplotlib import rc
from fig_2_b_spike_raster import datafile_figure_2b
rc('font', size=12)
rc('figure', figsize=(4, 3))
start = 5.5
end = 6.0
if __name__ == '__main__':
    data = TraubData(makepath(datafile_figure_2b))
    ax = None
    for ii, celltype in enumerate(CELLTYPES):
        for node in data.fdata['Vm']:
            if node.startswith(celltype):
                ax = plt.subplot(len(CELLTYPES), 1, ii+1, sharex=ax, sharey=ax)
                # plt.title(celltype)
                Vm = data.fdata['Vm'][node][:]
                ts = np.linspace(0, data.simtime, Vm.shape[0])
                idx = np.flatnonzero((ts > start) & (ts < end))
                ts = ts[idx].copy()
                Vm = Vm[idx].copy()
                plt.plot(ts, Vm*1e3, color=cellcolor[celltype])
                plt.gca().spines['top'].set_visible(False)
                plt.gca().spines['right'].set_visible(False)
                plt.gca().get_xaxis().tick_bottom()
                plt.gca().get_yaxis().tick_left()
                plt.gca().xaxis.set_visible(False)
                break
    plt.xlabel('Time (s)')
    plt.ylabel('Vm (mV)')
    plt.gca().set_yticks([-80, -40, 0, 40])
    plt.gca().xaxis.set_visible(True)
    plt.gcf().subplots_adjust(left=0.2, right=0.95, bottom=0.2, top=0.95)
    # plt.tight_layout()
    plt.savefig('figures/Figure_2_C_Vm.svg', transparent=True)
    plt.show()


# 
# fig_2_c_zoomed_Vm.py ends here
