# dump_prepost_spikes_stats.py --- 
# 
# Filename: dump_prepost_spikes_stats.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Tue May  5 23:14:24 2015 (-0400)
# Version: 
# Last-Updated: Tue Jan 19 03:01:13 2016 (-0500)
#           By: subha
#     Update #: 231
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
from scipy import stats
import pandas as pd

def dump_pre_post_stim_spike_count(ffname, outprefix, celltype, window=10e-3):
    """Dump mean, median and standard deviation in population spike before and after stimulus.
    """
    with open('{}_prepost_spikes_{}_{}ms_window.csv'.format(outprefix, celltype, window*1e3), 'wb') as fd:
        writer = csv.writer(fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        norm_files = get_dbcnt_dict(ffname)
        writer.writerow(['dbcount', 'filename', 'premean', 'premedian', 'prestd', 'postmean', 'postmedian', 'poststd', 'nstim'])
        for dbcnt, flist in norm_files.items():
            for fname in flist:
                data = TraubData(makepath(fname))
                pop_train_list = []
                bgtimes, probetimes = get_stim_times(data, correct_tcr=True)
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
                    npre = np.flatnonzero((pop_train < t) & (pop_train > (t - window/2))).shape[0]
                    pre.append(npre * 1.0 / (data.cellcounts._asdict()[celltype] * window / 2.0))
                    npost = np.flatnonzero((pop_train > t) & (pop_train < t + window/2)).shape[0]
                    post.append(npost * 1.0 / (data.cellcounts._asdict()[celltype] * window / 2.0))
                    if np.median(pre) == 0:
                        print '####', fname, pre
                writer.writerow([dbcnt, fname, np.mean(pre), np.median(pre), np.std(pre, ddof=1), np.mean(post), np.median(post), np.std(post, ddof=1), len(times)])
                

def dump_pre_post_stim_firing_rate(ffname, outprefix, window=10e-3):
    """Dump mean, median and standard deviation in population spike before and after stimulus.
    """
    dbcnt_flist_dict = get_dbcnt_dict(ffname)
    celltype_data_dict = defaultdict(list)
    for dbcnt, flist in dbcnt_flist_dict.items():
        for fname in flist:
            data = TraubData(makepath(fname))
            bgtimes, probetimes = get_stim_times(data, correct_tcr=True)
            times = np.concatenate((bgtimes, probetimes))
            times.sort()
            spiketrains = defaultdict(list)
            for cell, train in data.spikes.items():
                celltype = cell.partition('_')[0]
                spiketrains[celltype].append(train)
            for celltype, trains in spiketrains.items():
                popspikes = np.concatenate(trains)
                popspikes.sort()
                pre = []
                post = []
                for t in times:
                    npre = np.flatnonzero((popspikes <= t) & (popspikes > (t - window/2))).shape[0]
                    pre.append(npre / (data.cellcounts._asdict()[celltype] * window / 2.0))
                    npost = np.flatnonzero((popspikes > t) & (popspikes < (t + window/2))).shape[0]
                    post.append(npost / (data.cellcounts._asdict()[celltype] * window / 2.0))
                dstats = {
                    'filename': fname,
                    'dbcount': dbcnt,
                    'premean': np.mean(pre),
                    'premedian': np.median(pre),
                    'prestd': np.std(pre),
                    'presem': stats.sem(pre),
                    'postmean': np.mean(post),
                    'postmedian': np.median(post),
                    'poststd': np.std(post),
                    'postsem': stats.sem(post),
                    'nstim': len(times)}
                celltype_data_dict[celltype].append(dstats)
    for celltype, datalist in celltype_data_dict.items():
        df = pd.DataFrame(datalist, columns=['filename',
                    'dbcount',
                    'premean',
                    'premedian',
                    'prestd',
                    'presem',
                    'postmean',
                    'postmedian',
                    'poststd',
                    'postsem',
                    'nstim'])
        outfile = '{}_prepost_rates_{}_{}ms_window.csv'.format(outprefix, celltype, window*1e3)
        df.to_csv(outfile)
                                                    
                    
        
if __name__ == '__main__':
    dump_pre_post_stim_firing_rate('normal.csv', 'norm', window=20e-3)
    # dump_pre_post_stim_spike_count(ffname, 'norm', 'DeepBasket', window=20e-3)
    # dump_pre_post_stim_spike_count(ffname, 'norm', 'DeepLTS', window=20e-3)
    # dump_pre_post_stim_spike_count(ffname, 'norm', 'SpinyStellate', window=10e-3)
    # dump_pre_post_stim_spike_count(ffname, 'norm', 'DeepBasket', window=10e-3)
    # dump_pre_post_stim_spike_count(ffname, 'norm', 'DeepLTS', window=10e-3)
    dump_pre_post_stim_firing_rate('lognorm.csv', 'lognorm', window=20e-3)
    # dump_pre_post_stim_spike_count(ffname, 'lognorm', 'SpinyStellate', window=20e-3)
    # dump_pre_post_stim_spike_count(ffname, 'lognorm', 'DeepBasket', window=20e-3)
    # dump_pre_post_stim_spike_count(ffname, 'lognorm', 'DeepLTS', window=20e-3)
    # dump_pre_post_stim_spike_count(ffname, 'lognorm', 'SpinyStellate', window=10e-3)
    # dump_pre_post_stim_spike_count(ffname, 'lognorm', 'DeepBasket', window=10e-3)
    # dump_pre_post_stim_spike_count(ffname, 'lognorm', 'DeepLTS', window=10e-3)

# 
# dump_prepost_spikes_stats.py ends here
