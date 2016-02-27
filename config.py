import socket


cellcolor = {
    'SupBasket': '#377eb8',
    'SupLTS': '#984ea3',
    'SupAxoaxonic': '#4daf4a',
    'DeepBasket': '#377eb8',
    'DeepLTS': '#984ea3',
    'DeepAxoaxonic': '#4daf4a',
    'SupPyrRS': '#ffff33',
    'SupPyrFRB': '#ff7f00',
    'SpinyStellate': '#e41a1c',
    'NontuftedRS': '#e41a1c',
    'TuftedIB': '#ff7f00',
    'TuftedRS': '#ff7f00',
    'nRT': '#377eb8',
    'TCR': '#ff7f00'
    }

mdict = {
    'SupBasket' : '^',
    'SupLTS' : '^',
    'SupAxoaxonic' : '^',
    'DeepBasket' : '|',
    'DeepLTS' : '|',
    'DeepAxoaxonic' : '|',
    'SupPyrRS' : '^',
    'SupPyrFRB' : '^',
    'SpinyStellate' : '|',
    'NontuftedRS' : '^',
    'TuftedIB' : '^',
    'TuftedRS' : '^',
    'nRT' : '^',
    'TCR' : '|',
}

import subprocess

CELLTYPES = ['SpinyStellate', 'DeepBasket', 'DeepLTS']

# The first series of locations for linux machines in Upi's lab, the second is my hard disk mounted on windows
hostname = socket.gethostname()
if  'chamcham' == hostname:
    datadirs = ['/data/subha/rsync_ghevar_cortical_data_clone', '/pantua/subha/nargis_cortical_data', '/data/subha/cortical_data']
elif 'niyantran' == hostname:
    datadirs = ['/mnt/wd2/data_bhalla_lab/subha/rsync_ghevar_cortical_data_clone', '/mnt/wd2/data_bhalla_lab/subha/nargis_cortical_data']
else:
    datadirs =['G:\\data_bhalla_lab\\subha\\nargis_cortical_data', 'G:\\data_bhalla_lab\\subha\\rsync_ghevar_cortical_data_clone', 'G:\\data_bhalla_lab\\subha\\rsync_ghevar_cortical_clone\\py\\data']
