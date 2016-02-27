# dump_psth_peaks.py --- 
# 
# Filename: dump_psth_peaks.py
# Description: 
# Author: subha
# Maintainer: 
# Created: Tue May  5 23:14:24 2015 (-0400)
# Version: 
# Last-Updated: Mon Nov 23 23:07:34 2015 (-0500)
#           By: subha
#     Update #: 43
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

def dump_psth_peaks(ffname, outprefix, celltype, window=100e-3, binwidth=5e-3):
    """Dump the population spike histogram values."""
    with open('{}_psth_{}_{}ms_window_{}ms_bins.csv'.format(outprefix, celltype, window*1e3, binwidth*1e3), 'wb') as fd:
        writer = csv.writer(fd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        dbcnt_flist = get_dbcnt_dict(ffname)
        bins = np.arange(-window / 2.0, window / 2.0 + 0.5 * binwidth, binwidth)
        writer.writerow(['dbcount', 'filename'] + list(np.asarray(np.round(bins[1:]*1e3), dtype=int)))
        for dbcnt, flist in dbcnt_flist.items():
            for fname in flist:
                data = TraubData(makepath(fname))
                pop_train_list = []
                bgtimes, probetimes = get_stim_times(data, correct_tcr=True)
                if (len(bgtimes) == 0) and (len(probetimes) == 0):
                    print 'EE: {} has no TCR spiking on stimulus.'.format(fname)
                    continue
                stim_times = np.concatenate((bgtimes, probetimes))
                stim_times.sort()
                # print '###', stim_times
                for cell, train in data.spikes.items():
                    if cell.startswith(celltype):
                        pop_train_list.append(train)
                pop_train = np.concatenate(pop_train_list)
                pop_train.sort()
                
                bgpsth, b = psth(pop_train, stim_times, window=window, bins=bins)
                bgpsth /= (data.cellcounts._asdict()[celltype] * binwidth)
                writer.writerow([dbcnt, fname] + list(bgpsth))
                
            
        
if __name__ == '__main__':
    ffname = 'normal.csv'
    dump_psth_peaks(ffname, 'norm', 'SpinyStellate', window=200e-3)
    dump_psth_peaks(ffname, 'norm', 'DeepBasket', window=200e-3)
    dump_psth_peaks(ffname, 'norm', 'DeepLTS', window=200e-3)
    ffname = 'lognorm.csv'
    dump_psth_peaks(ffname, 'lognorm', 'SpinyStellate', window=200e-3)
    dump_psth_peaks(ffname, 'lognorm', 'DeepBasket', window=200e-3)
    dump_psth_peaks(ffname, 'lognorm', 'DeepLTS', window=200e-3)

# 
# dump_psth_peaks.py ends here
