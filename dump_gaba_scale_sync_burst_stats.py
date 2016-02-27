# dump_gaba_scale_sync_burst_stats.py --- 
# 
# Filename: dump_gaba_scale_sync_burst_stats.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Wed Oct 22 13:01:27 2014 (+0530)
# Version: 
# Last-Updated: Tue May 26 18:19:54 2015 (-0400)
#           By: Subhasis Ray
#     Update #: 123
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
# Tue May  5 19:36:55 EDT 2015 - converted figure_4 ... script
# to dump the data in csv format for later analysis. Changed look ahead 
# from 3 to 10.

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
"""Plots the effect of scaling GABA conductance."""


import sys
import csv
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict

from peakdetect import peakdetect

from traubdata import TraubData
from util import makepath, get_filenames
from config import cellcolor

from matplotlib import rc
plt.rc('font', size=12)
plt.rc('figure', figsize=(17.35/2.54, 23.35/2.54/3))

CELLTYPES = ['SpinyStellate', 'DeepBasket', 'DeepLTS']

def get_gaba_data_dict(filelist):
    """Returns a mapping from GABA conductance to TraubData objects"""
    ret = defaultdict(list)
    for fname in get_filenames(filelist):        
        print fname, makepath(fname)
        data = TraubData(makepath(fname))
        gaba = dict(data.fdata['/runconfig/GABA'])
        ret[float(gaba['conductance_scale'])].append(data)
        
    return ret
    
def plot_ss_fraction(scale_data_dict, figfilename='Figure_4A.svg'):
    """Plot the fraction of cells spiking in each bin"""
    fig = plt.figure()
    ii = 0
    for scale in sorted(scale_data_dict.keys()):        
        datalist = scale_data_dict[scale]        
        for celltype in CELLTYPES:
            ax = fig.add_subplot(len(scale_data_dict), len(CELLTYPES), ii+1)
            if ii % len(CELLTYPES) == 0:
                ax.set_ylabel('gaba={}x'.format(scale))
            ii += 1
            ax.set_title(celltype)
            for data in datalist:
                hist, bins = data.get_spiking_cell_hist(celltype, frac=True)
                ax.plot(0.5 * (bins[:-1] + bins[1:]), hist, alpha=0.5)

def dump_ss_fraction_peaks(flistfilename, trange=(2,20), cutoff=0.2, binsize=5e-3, lookahead=10):
    """Plot the peaks in fraction of spiny stellate cells over multiple
    simulations."""
    #data_dict = get_gaba_data_dict(flistfilename)
    peak_frac_med = defaultdict(list)
    peak_frac_mean = defaultdict(list)
    iqr_dict = defaultdict(list)
    with open('gaba_scale_ss_frac_cutoff_{}_binwidth_{}ms_lookahead_{}.csv'.format(cutoff, binsize*1000, lookahead), 'wb') as fd:
        writer = csv.writer(fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('filename', 'gabascale',  'frac_mean', 'frac_med', 'frac_iqr'))
        for fname in get_filenames(flistfilename):
            data = TraubData(makepath(fname))
            gaba = dict(data.fdata['/runconfig/GABA'])
            scale = gaba['conductance_scale']
            print fname, gaba
            hist, bins = data.get_spiking_cell_hist('SpinyStellate',
                                                    timerange=trange,
                                                    binsize=binsize,
                                                    frac=True)
            peaks, troughs = peakdetect(hist, bins[:-1], lookahead=lookahead)
            if len(peaks) == 0:
                print 'No peaks for', data.fdata.filename
                writer.writerow((fname, scale, '', '', ''))
                continue
            x, y = zip(*peaks)
            x = np.asarray(x)
            y = np.asarray(y)
            idx = np.flatnonzero(y > cutoff)
            frac_med = ''
            frac_mean = ''
            iqr = ''
            if len(idx) > 0:
                frac_med = np.median(y[idx])
                frac_mean = np.mean(y[idx])
                iqr = np.diff(np.percentile(y[idx], [25,75]))
                if len(iqr) > 0:
                    iqr = iqr[0]
                else:
                    iqr = ''
            peak_frac_med[scale].append(frac_med)
            peak_frac_mean[scale].append(frac_mean)
            iqr_dict[scale].append(iqr)
            writer.writerow((fname, scale, frac_mean, frac_med, iqr))
    return peak_frac_mean, peak_frac_med, iqr_dict
    # ax = plt.subplot(121)
    # ax.boxplot([peak_frac_med[scale] for scale in sorted(peak_frac_med.keys())], notch=True)
    # ax.set_xticklabels(sorted(peak_frac_med.keys()))
    # ax.set_xlabel('GABA scale')
    # ax.set_ylabel('Median fraction')
    # ax.set_yticks([0.0, 0.5, 1.0])
    # plt.setp(ax, frame_on=False)
    # ax.tick_params(axis='y', right=False)
    # ax.tick_params(axis='x', top=False)            
    # ax = plt.subplot(122)
    # ax.boxplot([iqr_med[scale] for scale in sorted(iqr_med.keys())], notch=True)
    # ax.set_xticklabels(sorted(peak_frac_med.keys()))
    # ax.set_xlabel('GABA scale')
    # ax.set_ylabel('Interquartile range')
    
    # plt.setp(ax, frame_on=False)
    # ax.tick_params(axis='y', right=False)
    # ax.tick_params(axis='x', top=False)            
    # plt.savefig(figfilename)

if __name__ == '__main__':
    # data_dict = get_gaba_data_dict('gaba_scaling.csv')
    # plot_ss_fraction(data_dict)
    # dump_ss_fraction_peaks('gaba_scaling.csv', cutoff=0.1)
    dump_ss_fraction_peaks('gaba_scaling.csv', cutoff=0.2)

# 
# dump_gaba_scale_sync_burst_stats.py ends here
