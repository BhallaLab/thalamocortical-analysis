# anova_psth_and_slope.py --- 
# 
# Filename: anova_psth_and_slope.py
# Description: 
# Author: Subhasis Ray
# Maintainer: 
# Created: Mon Feb 16 15:16:37 2015 (-0500)
# Version: 
# Package-Requires: ()
# Last-Updated: Wed Feb 18 17:42:37 2015 (-0500)
#           By: Subhasis Ray
#     Update #: 256
# URL: 
# Doc URL: 
# Keywords: 
# Compatibility: 
# 
# 

# Commentary: 
# 
# 
# 
# 

# Change Log:
# 
# 
# 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
# 
# 

# Code:
"""Compare the PSTH peak and slopes between normal and lognormal
distribution using two-way ANOVA."""



import h5py as h5
import numpy as np
from scipy import signal, stats
from collections import defaultdict
import matplotlib.pyplot as plt
import csv
import util
from peakdetect import peakdetect
from util import get_filenames, makepath, get_dbcnt_dict, psth
from plotutil import get_psth_with_dbcount
from traubdata import TraubData
from plot_stimulus_effect_new import get_stim_times
import scipy.stats as stats
import config
import os
from statsmodels.formula.api import ols

from statsmodels.graphics.api import interaction_plot, abline_plot

from statsmodels.stats.anova import anova_lm

import pandas 
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import sys
sys.path.append('C:\\Users\\Subhasis\\Documents\\research\\spike_sorting\\python')
import pyximport
pyximport.install()
# import peakdetect as pd
from figure_7_psth_and_slope_norm_lognorm import get_dbcnt_psth_peaks

import pickle ## Always save intermediate data ##


window = 100e-3
binwidth = 5e-3
# first try to find saved data
lognorm_psth_file = 'psth_lognorm.pkl'
try:
    lognorm_psth = pickle.load(open(lognorm_psth_file, 'rb'))
    print 'Loading pickled file', lognorm_psth_file
except IOError:
    lognorm_psth = {}
    dbcnt_bg_psth, dbcnt_probe_psth, bins = get_psth_with_dbcount('lognorm.csv', window, binwidth, datadirs=config.datadirs)
    lognorm_psth['dbcnt_bg_psth'] = dbcnt_bg_psth
    lognorm_psth['dbcnt_probe_psth'] = dbcnt_probe_psth
    lognorm_psth['bins'] = bins
    lognorm_psth['window'] = window
    lognorm_psth['binwidth'] =  binwidth
    pickle.dump(lognorm_psth, open(lognorm_psth_file, 'wb'))

norm_psth_file = 'psth_norm.pkl'
try:
    norm_psth = pickle.load(open(norm_psth_file, 'rb'))
    print 'Loading pickled file', norm_psth_file
except IOError:
    norm_psth = {}
    dbcnt_bg_psth, dbcnt_probe_psth, bins = get_psth_with_dbcount('normal.csv', window, binwidth, datadirs=config.datadirs)
    norm_psth['dbcnt_bg_psth'] = dbcnt_bg_psth
    norm_psth['dbcnt_probe_psth'] = dbcnt_probe_psth
    norm_psth['bins'] = bins
    norm_psth['window'] = window
    norm_psth['binwidth'] =  binwidth
    pickle.dump(norm_psth, open(norm_psth_file, 'wb'))

# CELLTYPE = 'SpinyStellate' # PSTH for this cell type
for celltype in config.CELLTYPES:
    # Save the data in pandas files. This does not specifically go after the
    # peaks, but only the PSTH value in first bin
    dbcnt_norm = sorted(norm_psth['dbcnt_bg_psth'][celltype].keys())
    peaks_norm, slopes_norm, = get_dbcnt_psth_peaks(norm_psth['dbcnt_bg_psth'], norm_psth['bins'], celltype)
    dbcnt_lognorm = sorted(lognorm_psth['dbcnt_bg_psth'][celltype].keys())
    peaks_lognorm, slopes_lognorm, = get_dbcnt_psth_peaks(lognorm_psth['dbcnt_bg_psth'], lognorm_psth['bins'], celltype)
    data = []
    # distribution 0: norm, 1: lognorm
    for dbcnt, peaks in zip(dbcnt_norm, peaks_norm):
        print 'dbcnt:', dbcnt
        for peak in peaks:
            data.append((0, dbcnt, peak))
    for dbcnt, peaks in zip(dbcnt_lognorm, peaks_lognorm):
        for peak in peaks:
            data.append((1, dbcnt, peak))
    df = pandas.DataFrame.from_records(data, columns=['distribution', 'dbcount', 'psth_first_bin'])
    psth_combined_file = 'psth_first_bin_{}.h5'.format(celltype)
    if not os.path.exists(psth_combined_file):
        df.to_hdf(psth_combined_file, key='PSTH_first_bin', format='t')
        print 'Saved combined dataframe into file {}.'.format(psth_combined_file)
    else:
        print 'File {} already exists - rename to write data frame.'.format(psth_combined_file)

    """
    ############################################
    # Verify the dbcnt and distribution of data
    fig = plt.figure('psth-first-bin entry')
    ax = fig.add_subplot(111)
    colors = ['r', 'b']
    symbols = ['+', 'x']
    factor_groups = df.groupby(['distribution'])
    # Display the grouped values in scatter plot
    for values, group in factor_groups:
        # print 'ssss Start ssss'
        # print '--- Values ---'
        # print values
        # print '==== Group ===='
        # print group
        # print 'xxxx End xxxx'
        # print group['dbcount']
        i = values
        label = 'normal' if i == 0 else 'lognorm'
        ax.scatter(group['dbcount'], group['psth_first_bin'], marker=symbols[i], color=colors[i], label=label)
        ax.set_xlabel('dbcount')
        ax.set_ylabel('psth-first-bin')
    ax.legend()    
    # plt.show()
    # DataFrame.hist(by=[]) shows distribution of data in each group using histogram
    df.hist(by=['distribution', 'dbcount'])
    plt.show()
    """

    # One-way ANOVA for normal and log normal distribution
    normal_data = df[df.distribution == 0]
    print 'NORMAL DISTR {} ################'.format(celltype)
    print normal_data
    print '################'
    formula = 'psth_first_bin ~ dbcount'
    lm = ols(formula, normal_data).fit()
    print 'FORMULA:', formula
    print 'Summary of linear model-----------------'
    print lm.summary()
    print 'ANOVA::::::::::::::::::::::::::::::::::::::'
    print anova_lm(lm)

    lognormal_data = df[df.distribution == 1]
    print 'LOGNORMAL DISTR {} ################'.format(celltype)
    print lognormal_data
    print '################'
    lm = ols(formula,lognormal_data).fit()
    print 'FORMULA:', formula
    print 'Summary of linear model-----------------'
    print lm.summary()
    print 'ANOVA::::::::::::::::::::::::::::::::::::::'
    print anova_lm(lm)

    # Describe after grouping by distribution and dbcount

    formula = 'psth_first_bin ~ C(distribution) * dbcount'
    factor_groups = df.groupby(['distribution', 'dbcount'])
    # print '=============Start group description ==================='
    # factor_groups.describe() # Works in interactive mode only 
    # print '=============End group description ==================='

    lm = ols(formula, df).fit()
    print 'Two-factor ANOVA {} #######################'.format(celltype)
    print 'FORMULA:', formula
    print 'Summary of linear model-----------------'
    print lm.summary()
    print 'ANOVA::::::::::::::::::::::::::::::::::::::'
    print anova_lm(lm)
    print '+++++++++++++++++++++++++++++++++++++++++\n\n\n'
    # formula = 'psth_first_bin ~ dbcount * distribution'
    # print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
    # lm = ols(formula, df).fit()
    # print lm.summary()
    # print(anova_lm(lm))


    
    


# 
# anova_psth_and_slope.py ends here
