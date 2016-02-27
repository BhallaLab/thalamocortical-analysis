# dump_psth_peaks.py --- 
# 
# Filename: dump_psth_peaks.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Tue May  5 23:14:24 2015 (-0400)
# Version: 
# Last-Updated: Sat May  9 20:15:35 2015 (-0400)
#           By: Subhasis Ray
#     Update #: 68
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
"""Dump the psth peaks in the first bin ( and later ) from simulations
with varied basket cell counts."""

import csv
from collections import defaultdict
import numpy as np
from datafiles import *
from traubdata import TraubData
from util import get_filenames, makepath, get_dbcnt_dict, get_stim_times, window_spikes, psth

def dump_pre_post_stim_spike_count(ffname, outprefix, celltype, window=10e-3):
    """Dump the standard deviation in population spike before and after stimulus.
    """
    with open('{}_prepost_spikes_{}_{}ms_window.csv'.format(outprefix, celltype, window*1e3), 'wb') as fd:
        writer = csv.writer(fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        norm_files = get_dbcnt_dict(ffname)
        writer.writerow(['dbcount', 'filename', 'premean', 'premedian', 'prestd', 'postmean', 'postmedian', 'poststd'])
        for dbcnt, flist in norm_files.items():
            for fname in flist:
                data = TraubData(makepath(fname))
                pop_train_list = []
                bgtimes, probetimes = get_stim_times(data, correct_tcr=False)
                times = np.concatenate((bgtimes, probetimes))
                times.sort()
                for cell, train in data.spikes.items():
                    if cell.startswith(celltype):
                        pop_train_list.append(train)
                pop_train = np.concatenate(pop_train_list)
                pop_train.sort()
                pre = []
                post = []
                for t in times:
                    pre.append(np.flatnonzero((pop_train < t) & (pop_train > t - window/2)).shape[0]*1.0 / data.cellcounts._asdict()[celltype])
                    post.append(np.flatnonzero((pop_train > t) & (pop_train < t + window/2)).shape[0]*1.0 / data.cellcounts._asdict()[celltype])
                writer.writerow([dbcnt, fname] + [np.mean(pre), np.median(pre), np.std(pre, ddof=1), np.mean(post), np.median(post), np.std(post, ddof=1)])
                
            
        
if __name__ == '__main__':
    ffname = 'normal.csv'
    dump_pre_post_stim_spike_count(ffname, 'norm', 'SpinyStellate')
    dump_pre_post_stim_spike_count(ffname, 'norm', 'DeepBasket')
    dump_pre_post_stim_spike_count(ffname, 'norm', 'DeepLTS')
    ffname = 'lognorm.csv'
    dump_pre_post_stim_spike_count(ffname, 'lognorm', 'SpinyStellate')
    dump_pre_post_stim_spike_count(ffname, 'lognorm', 'DeepBasket')
    dump_pre_post_stim_spike_count(ffname, 'lognorm', 'DeepLTS')

# 
# dump_psth_peaks.py ends here
