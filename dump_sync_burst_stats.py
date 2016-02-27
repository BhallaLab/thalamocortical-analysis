# dump_sync_burst_stats.py --- 
# 
# Filename: dump_sync_burst_stats.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Tue Apr 21 19:44:56 2015 (-0400)
# Version: 
# Last-Updated: 
#           By: 
#     Update #: 0
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
"""This scripts computes the mean fraction of synchronously bursting
cells, mean interburst intervals for each simulation and dumps it to a
csv file for further analysis.

"""
import sys
import csv
import numpy as np
from scipy import stats
import pandas as pd
from traubdata import TraubData
from util import makepath, get_dbcnt_dict
from peakdetect import peakdetect

celltypes = ['SpinyStellate', 'DeepBasket', 'DeepLTS']

def dump_syncspike_stats(outfile, dbcnt_file_dict,  trange=(2,20), cutoff=0.2, binsize=5e-3, lookahead=3):
    """Combined statistics for synchrounous fractions and inter burst intervals"""
    datalist = []
    for dbcnt, flist in dbcnt_file_dict.items():
        for fname in flist:
            data = TraubData(makepath(fname))
            hist, bins = data.get_spiking_cell_hist('SpinyStellate',
                                            timerange=trange,
                                            binsize=binsize,
                                            frac=True)
            peaks, troughs = peakdetect(hist, bins[:-1], lookahead=lookahead)
            time, frac, = zip(*peaks)
            frac = np.array(frac)
            time = np.array(time)
            idx = np.flatnonzero(frac > cutoff)                
            frac = frac[idx].copy()
            ibi = np.diff(time[idx])
            data_stats = {
                'filename': fname,
                'dbcount': dbcnt,
                'frac_mean': np.mean(frac),
                'frac_median': np.median(frac),
                'frac_iqr': np.diff(np.percentile(frac, [25, 75]))[0],
                'frac_sem': stats.sem(frac),
                'ibi_mean': np.mean(ibi), 
                'ibi_median': np.median(ibi), 
                'ibi_iqr': np.diff(np.percentile(ibi, [25, 75]))[0], 
                'ibi_sem': stats.sem(ibi)
            }
            datalist.append(data_stats)
    dataframe = pd.DataFrame(datalist, columns=['filename',
                                                'dbcount',
                                                'frac_mean',
                                                'frac_median',
                                                'frac_iqr',
                                                'frac_sem',
                                                'ibi_mean', 
                                                'ibi_median', 
                                                'ibi_iqr', 
                                                'ibi_sem'])
    dataframe.to_csv(outfile)
    print 'Saved data in', outfile


if __name__ == '__main__':    
    tstart = 2.0
    tend = 20.0
    cutoff = 0.2
    binsize = 5e-3
    lookahead = 3
    norm_files = get_dbcnt_dict('normal.csv')    
    norm_out = 'norm_syncspike_stats_cutoff_{}_binwidth_{}ms_lookahead_{}.csv'.format(cutoff, binsize*1000, lookahead)
    dump_syncspike_stats(norm_out, norm_files, trange=(tstart, tend), cutoff=cutoff, binsize=binsize, lookahead=lookahead)
    
    lognorm_files = get_dbcnt_dict('lognorm.csv')    
    lognorm_out = 'lognorm_syncspike_stats_cutoff_{}_binwidth_{}ms_lookahead_{}.csv'.format(cutoff, binsize*1000, lookahead)
    dump_syncspike_stats(lognorm_out, lognorm_files, trange=(tstart, tend), cutoff=cutoff, binsize=binsize, lookahead=lookahead)    
    

# 
# dump_sync_burst_stats.py ends here
