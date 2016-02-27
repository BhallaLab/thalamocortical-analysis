# figure_0_f_i_curves.py --- 
# 
# Filename: figure_0_f_i_curves.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Wed Oct 29 15:26:31 2014 (+0530)
# Version: 
# Last-Updated: Sun Jan 10 20:04:38 2016 (-0500)
#           By: subha
#     Update #: 335
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
"""Plot the F-I curves for single cell models"""

import os
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import h5py as h5
from peakdetect import peakdetect
import util
import config

plt.rc('font', size=12)
FILES = {
    'DeepBasket': 'f_i_tests_DeepBasket.h5',
    'DeepLTS': 'f_i_tests_DeepLTS.h5',
    'SpinyStellate': 'f_i_tests_SpinyStellate.h5',
    'TCR:': 'f_i_tests_TCR.h5',}

#DIRECTORY = '/data/subha/cortical_data'
DIRECTORY = 'f_i_curves'

CMAP = {'SpinyStellate': plt.cm.Reds,
        'DeepBasket': plt.cm.Blues,
        'DeepLTS': plt.cm.Purples}

REBOUND_WINDOW = 100e-3
REBOUND_DELAY = 20e-3
SPIKE_THRESHOLD = -40e-3
import warnings

warnings.simplefilter("error")

def plot_fi_curves():
    fig_fi = plt.figure(figsize=(3, 5))
    ax_fi = None
    for cellno, celltype in enumerate(util.CELLTYPES):
        filename = os.path.join(DIRECTORY, FILES[celltype])
        with h5.File(filename, 'r') as fhandle:
            groups = [key for key in fhandle.keys() if key.startswith(celltype)]
            cnt = len(groups)
            current_list = []
            freq_list = []
            ax_fi = fig_fi.add_subplot(len(util.CELLTYPES), 1, cellno + 1, sharey=ax_fi, sharex=ax_fi)
            for testno, test_name in enumerate(groups):
                test_group = fhandle[test_name]
                current = test_group.attrs['current']
                if current == 0.0:
                    continue
                current_list.append(current)
                dt = test_group['Vm'].attrs['dt']
                vm = np.asarray(test_group['Vm'])
                times = np.arange(0, len(vm), 1.0) * dt
                peaks, troughs = peakdetect(vm, times, lookahead=3)
                peaks = np.asarray(peaks, dtype=np.float64)
                spike_times = peaks[peaks[:,1] > SPIKE_THRESHOLD, 0].copy()
                stim = np.asarray(test_group['stimulus'])
                if current > 0:
                    tstart = np.where(np.diff(stim) > 0)[0][0]
                    tend = np.where(np.diff(stim) < 0)[0][0]
                else:
                    tstart = np.where(np.diff(stim) < 0)[0][0]
                    tend = np.where(np.diff(stim) > 0)[0][0]
                tstart = tstart * dt
                tend = tend * dt
                positive_spike = spike_times[(spike_times > tstart) & (spike_times < tend)].copy()
                freq = len(positive_spike) / (tend - tstart)
                freq_list.append(freq)
            current_list = np.asarray(current_list)
            freq_list = np.asarray(freq_list)
            # rebound_freq_list = np.asarray(rebound_freq_list)
            sort_idx = np.argsort(current_list)
            current_list = current_list[sort_idx].copy()
            freq_list = freq_list[sort_idx].copy()
            ax_fi.plot(current_list[current_list > 0]*1e9, freq_list[current_list > 0],
                       color=config.cellcolor[celltype], marker='^')
            #ax_fi.xaxis.set_visible(False)
            ax_fi.tick_params(axis='y', right=False)
            ax_fi.tick_params(axis='x', top=False)
            ax_fi.xaxis.set_visible(False)
            ax_fi.set_yticks([0, 300, 600])
            ax_fi.set_ylim([0, 600])
            ax_fi.spines['top'].set_visible(False)
            ax_fi.spines['right'].set_visible(False)
            #plt.setp(ax_fi, frame_on=False)
            # rebound_axes.plot(current_list[sort_idx], rebound_freq_list[sort_idx])
    
    ax_fi.xaxis.set_visible(True)
    ax_fi.set_xlabel('Current (nA)')
    ax_fi.set_ylabel('spikes/s')
    fig_fi.subplots_adjust(bottom=0.1, top=0.95, left=0.3, right=0.95)
    fig_fi.savefig('figures/Figure_1_EFG_curves.png', transparent=True)
    plt.show()
    
def plot_vm_current():
    """Plot Vm against current for *celltype*.

    This draws an overlayed plot of Vm for each step current
    amplitude. The colours changing from blue to red with increasing
    current.

    """
    fig_vi = plt.figure(figsize=(3,4))
    fig_inj = plt.figure(figsize=(3, 1))
    ax_vi = None
    ax_inj = fig_inj.add_subplot(111)
    for cellno, celltype in enumerate(util.CELLTYPES):
        filename = os.path.join(DIRECTORY, FILES[celltype])
        with h5.File(filename, 'r') as fhandle:
            groups = sorted([grp for grp in fhandle.keys() if grp.startswith(celltype)], key=lambda g: fhandle[g].attrs['current'])
            for g in groups:
                print(g, fhandle[g].attrs['current'])
            cnt = len(groups)
            current_list = [0.1e-9, 1e-9]
            ls = [':', '--', '-.', '-']
            ax_vi = fig_vi.add_subplot(len(util.CELLTYPES), 1, cellno+1, sharex=ax_inj, sharey=ax_vi)
            #plt.setp(ax_vi, frame_on=False)
            #ax_vi.xaxis.set_visible(False)
            ax_vi.tick_params(axis='y', right=False)
            ax_vi.tick_params(axis='x', top=False)
            # inject_axes = fig.add_subplot(2,1,2, sharex=vm_axes)
            for ii, test_name in enumerate(groups):
                found = False
                for jj, current in enumerate(current_list):
                    if np.isclose(current, fhandle[test_name].attrs['current'], atol=1e-15):
                        found = True
                        break
                if not found:
                #if ii % 5:
                    continue
                test_group = fhandle[test_name]
                current = test_group.attrs['current']
                if current < -1e-9:
                    continue
                print celltype, current
                vm = np.asarray(test_group['Vm'])
                stim = np.asarray(test_group['stimulus'])
                color = CMAP[celltype]((jj+1.0)/len(current_list))
                dt = test_group['Vm'].attrs['dt']
                times = np.arange(0, len(vm), 1.0) * dt
                idx = np.flatnonzero((times > 0.49) & (times < 0.55))
                ax_vi.plot(times[idx]*1e3, vm[idx]*1e3, color=color, ls='-')#ls[jj])
                ax_vi.spines['top'].set_visible(False)
                ax_vi.spines['right'].set_visible(False)
                ax_vi.set_yticks([-80, -40, 0, 40])
                ax_vi.set_ylim((-80, 40))
                ax_vi.xaxis.set_visible(False)
                if cellno == 0:
                    ax_inj.plot(times[idx]*1e3, stim[idx]*1e9, color=color,
                                label='{}'.format(test_group.attrs['current']))
    ax_vi.set_ylabel('Vm (mV)')
    fig_vi.subplots_adjust(left=0.3, right=0.95, bottom=0.1, top=0.95)
    fig_vi.savefig('figures/Figure_1ABC_Vm.svg', transparent=True)
    #fig_vi.tight_layout()
    #plt.setp(ax_inj, frame_on=False)
    ax_inj.spines['top'].set_visible(False)
    ax_inj.spines['right'].set_visible(False)
    ax_inj.set_xticks([490, 500, 550])
    ax_inj.set_xticklabels([490, 500, 550], rotation=45)
    ax_inj.set_xlabel('Time (ms)')
    ax_inj.set_yticks(np.array(current_list)*1e9)
    ax_inj.set_ylabel('Current (nA)')
    ax_inj.tick_params(axis='y', right=False)
    ax_inj.tick_params(axis='x', top=False)
    fig_inj.subplots_adjust(left=0.3, right=0.95, bottom=0.5, top=0.7)
    fig_inj.savefig('figures/Figure_1D_Inject.svg', transparent=True)
    
    plt.show()
    


if __name__ == '__main__':
    plot_fi_curves()
    plot_vm_current()
                                     


# 
# figure_0_f_i_curves.py ends here
