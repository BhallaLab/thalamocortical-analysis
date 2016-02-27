# figure_2_e_vm_fft_connected.py --- 
# 
# Filename: figure_2_e_vm_fft_connected.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Wed Jul  2 11:40:11 2014 (+0530)
# Version: 
# Last-Updated: Sat Dec 26 22:35:45 2015 (-0500)
#           By: subha
#     Update #: 4
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
"""Plot the fft of summed Vm for each cell population with synapses
removed."""

import sys
import numpy as np
from matplotlib import pyplot as plt

from traubdata import TraubData
from util import makepath
from config import cellcolor
from fig_3_d_vm_fft_disconnected import population_vm_spectrum, plot_vm_fft_multifile


from matplotlib import rc
rc('font', size=12)
rc('figure', figsize=(3, 3))


    
def old_main():
    datfilename = 'data_20130710_090635_4684.h5' # This is a simulation with 40 deep basket
    figfilename = 'Figure_2E.svg'
    trange = (2.0, 20.0)
    result = population_vm_spectrum(datfilename, trange)
    result.pop('TCR')
    fig = plt.figure()
    nax = len(result)
    ax = None
    major_formatter = plt.FormatStrFormatter('%1.1g')
    for ii, celltype in enumerate(reversed(result.keys())):
        ax = fig.add_subplot(nax, 1, ii+1, sharex=ax)
        freq, ft, = result[celltype]
        ax.plot(freq[(freq > 1) & (freq < 100)],
                 ft[(freq > 1) & (freq < 100)],
                 color=cellcolor[celltype], label=celltype)  #, alpha=0.5)
        # ax.get_yaxis().set_visible(False)
        ymax = ax.get_ylim()[1]
        p10 = np.log10(ymax)
        ymax = np.ceil(ymax / 10**int(p10)) * 10**int(p10)
        ax.set_ylim((0, ymax))
        ax.xaxis.set_visible(False)
        ax.yaxis.set_major_formatter(major_formatter)
        ax.yaxis.tick_left()
        ax.set_yticks(ax.get_ylim())
        plt.setp(ax, frame_on=False)
    ax.set_visible(True)
    ax.get_xaxis().set_visible(True)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('power')
    #ax.set_yticks([-15, 0, 15])
    ax.get_xaxis().tick_bottom()   # remove unneeded ticks
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', which='major', labelsize=11)
    plt.tight_layout()
    fig.savefig(figfilename)
    plt.show()


if __name__ == '__main__':
    plot_vm_fft_multifile('connected_norm_for_unconnected_fft.csv',
                          'figures/Figure_3e_fft_normal_connected.svg')
#    plot_vm_fft_multifile('connected_lognorm_for_unconnected_fft.csv',
#                          'figures/Figure_3_e_fft_lognorm_connected.svg')

# 
# figure_2_e_vm_fft_connected.py ends here
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
