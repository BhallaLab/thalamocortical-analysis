# figure_2_d_vm_fft_disconnected.py --- 
# 
# Filename: figure_2_d_vm_fft_disconnected.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Wed Jul  2 11:40:11 2014 (+0530)
# Version: 
# Last-Updated: Fri Dec 18 16:37:27 2015 (-0500)
#           By: Subhasis Ray
#     Update #: 30
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
from collections import defaultdict

from traubdata import TraubData
from util import makepath, get_filenames
from config import cellcolor

from matplotlib import rc
rc('font', size=12)
rc('figure', figsize=(3, 3))

CELLTYPES = ['SpinyStellate', 'DeepBasket', 'DeepLTS']

def population_vm_spectrum(filename, trange=(0, 1e9)):
    result = {}
    data = TraubData(makepath(filename))
    npts = int(data.simtime / data.simdt)
    t = np.arange(0, npts, 1.0) * data.simdt
    for celltype in data.cellcounts._fields:
        count = data.cellcounts._asdict()[celltype]
        if count == 0:
            continue
        vm_sum = np.zeros(npts)    
        for cellname in data.fdata['Vm']:
            if cellname.startswith(celltype):
                cellvm = data.fdata['Vm'][cellname]
                assert len(cellvm) == len(vm_sum)                                          
                vm_sum = vm_sum + cellvm
        vm_sum = vm_sum[(t >= trange[0]) & (t < trange[1])] / count
        ps = np.abs(np.fft.fft(vm_sum))**2
        freq = np.fft.fftfreq(ps.size, data.simdt)
        idx = np.argsort(freq)
        result[celltype] = (freq[idx].copy(), ps[idx].copy())
    return result


def plot_vm_fft(datfilename, trange=(2,20)):
    result = population_vm_spectrum(datfilename, trange)
    result.pop('TCR')
    fig = plt.figure()
    nax = len(result)
    ax = None
    # major_formatter = plt.FormatStrFormatter('%1.1g')
    for ii, celltype in enumerate(CELLTYPES):
        ax = fig.add_subplot(nax, 1, ii+1, sharex=ax)
        freq, ft, = result[celltype]
        ax.plot(freq[(freq > 1) & (freq < 100)],
                 ft[(freq > 1) & (freq < 100)],
                 color=cellcolor[celltype], label=celltype)  #, alpha=0.5)
        #ax.yaxis.set_visible(False)
        ymax = ax.get_ylim()[1]
        p10 = np.log10(ymax)
        ymax = np.ceil(ymax / 10**int(p10)) * 10**int(p10) 
        ax.set_ylim((0, ymax))
        ax.yaxis.tick_left()
        # ax.yaxis.set_major_formatter(major_formatter)
        ax.set_yticks(ax.get_ylim())
        ax.xaxis.set_visible(False)
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
    return fig

def overlay_unconnected_fft(flist, figfile, trange=(2,20)):
    fig = plt.figure()
    # major_formatter = plt.FormatStrFormatter('%1.3g')
    celltype_ax_dict = {}
    for fname in get_filenames(flist):
        result = population_vm_spectrum(fname, trange)
        result.pop('TCR')
        nax = len(result)
        for ii, celltype in enumerate(CELLTYPES):
            ax = celltype_ax_dict.get(celltype, None)
            if ax is None:
                ax = fig.add_subplot(nax, 1, ii+1, sharex=ax)
                celltype_ax_dict[celltype] = ax
            freq, ft, = result[celltype]
            idx = (freq > 1) & (freq < 100)
            ax.plot(freq[idx], ft[idx], # color=cellcolor[celltype],
                    label=celltype, alpha=0.5)
    plt.show()

    
def plot_frequency_distribution(flist, figfile, trange=(2,20),
                                freqbins=[0, 4, 10, 20, 40, 80,]):
    """Plot the distribution of various frequency peaks over multiple
    simulations of the unconnected network.

    Divide the range of frequencies into freqbins and then plot
    histogram of FT values in those.

    """
    celltype_freq_dict = defaultdict(dict)
    
    for fname in get_filenames(flist):
        result = population_vm_spectrum(fname, trange)
        result.pop('TCR')
        nax = len(result)
        for celltype, (freq, ft) in result.items():
            for ii, start in enumerate(freqbins):
                ft_list = celltype_freq_dict[celltype].get(start, [])
                print '$$', ii, freqbins[ii]
                if ii < len(freqbins) - 1:
                    idx = (freq >= start) & (freq < freqbins[ii+1])
                else:
                    idx = freq >= start
                nonzero = ft[idx][ft[idx] > 0]
                ft_list += list(nonzero)
                celltype_freq_dict[celltype][start] = ft_list
    fig = plt.figure()
    ax = None
    axno = 0
    for ii, celltype in enumerate(CELLTYPES):
        for jj, start in enumerate(freqbins):            
            axno += 1
            print '##', celltype, start, axno
            ax = fig.add_subplot(len(celltype_freq_dict), len(freqbins), axno)
            ax.hist(celltype_freq_dict[celltype][start], log=True)
            ax.set_xlabel('{}-{}'.format(start, 'inf' if jj == len(freqbins)-1 else freqbins[jj+1]))
            if jj == 0:
                ax.set_ylabel(celltype)
    # plt.tight_layout()
    plt.savefig(figfile)
    plt.show()
            

def plot_vm_fft_multifile(flist, figfile, trange=(2,20)):
    """Combine the Vm from cells of each celltype in all simulations and
    plot FT for each celltype. Since FT is linear, we can just sum the
    FT of individual simulations to get that of the sum of the Vms

    """
    celltype_ft_dict = {}
    freq_comp = None
    for fname in get_filenames(flist):
        result = population_vm_spectrum(fname,  trange)
        result.pop('TCR')
        for celltype, (freq, ft) in result.items():
            if freq_comp is not None:
                np.testing.assert_array_equal(freq_comp, freq)
            else:
                freq_comp = freq
            if celltype in celltype_ft_dict:
                celltype_ft_dict[celltype] += ft
            else:
                celltype_ft_dict[celltype] = ft
    fig = plt.figure()
    ax = None
    # major_formatter = plt.FormatStrFormatter('%1.1g')
    for ii, celltype in enumerate(CELLTYPES):
        ax = fig.add_subplot(len(celltype_ft_dict), 1, ii+1, sharex=ax)
        ft = celltype_ft_dict[celltype]
        idx = (freq_comp > 0) & (freq_comp < 100)
        
        ax.plot(freq_comp[idx], ft[idx], color=cellcolor[celltype],
                label=celltype)
        # print ii, celltype
        # ax.legend()
        # ymax = ax.get_ylim()[1]
        # p10 = np.log10(ymax)
        # ymax = np.ceil(ymax / 10**int(p10)) * 10**int(p10) 
        # ax.set_ylim((0, ymax))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)        
        ax.yaxis.tick_left()
        ax.xaxis.tick_bottom()
        # ax.yaxis.set_major_formatter(major_formatter)
        # ax.set_yticks(ax.get_ylim())
        # ax.xaxis.set_visible(False)
        # plt.setp(ax, frame_on=False)
    # ax.set_visible(True)
    # ax.get_xaxis().set_visible(True)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('power')
    #ax.set_yticks([-15, 0, 15])
    ax.tick_params(axis='x', which='major', labelsize=11)
    plt.tight_layout()
    plt.savefig(figfile)
    plt.show()
    
        
if __name__ == '__main__':
    # overlay_unconnected_fft('unconnected_network.csv', 'fft_unconnected.png', trange=(2,20))
    # plot_frequency_distribution('unconnected_network.csv', 'fft_unconnected.png')
    plot_vm_fft_multifile('unconnected_network.csv', 'figures/Figure_3D_fft_unconnected_multifile.svg')

# 
# figure_2_d_vm_fft_disconnected.py ends here
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
