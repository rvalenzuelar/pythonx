
import pandas as pd
import scipy.io as sio
from datetime import datetime, timedelta


def datenum_to_datetime(datenum):
    """
    Convert Matlab datenum into Python datetime.
    :param datenum: Date in datenum format
    :return:        Datetime object corresponding to datenum.

    source: https://gist.github.com/vicow
    """
    days = datenum % 1
    hours = days % 1 * 24
    minutes = hours % 1 * 60
    seconds = minutes % 1 * 60
    return datetime.fromordinal(int(datenum)) \
        + timedelta(days=int(days)) \
        + timedelta(hours=int(hours)) \
        + timedelta(minutes=int(minutes)) \
        + timedelta(seconds=round(seconds)) \
        - timedelta(days=366)


f = '/home/rvalenzuela/SURFACE/climatology/BBY01_Sfcmet.mat'
mat = sio.loadmat(f)['Sfcmet_bby']

# cols=sfc.dtype.names
date, tempc, rh, pmb, wspd, wdir, precip = \
    [], [], [], [], [], [], []
for n in range(mat.size):
    date.append(datenum_to_datetime(mat['dayt'][0][n][0][0]))
    tempc.append(mat['tamb'][0][n][0][0])
    rh.append(mat['rh'][0][n][0][0])
    pmb.append(mat['pmb'][0][n][0][0])
    wspd.append(mat['wspd'][0][n][0][0])
    wdir.append(mat['wdir'][0][n][0][0])
    precip.append(mat['precip'][0][n][0][0])
d = {'tempc': tempc, 'rh': rh, 'pmb': pmb,
     'wspd': wspd, 'wdir': wdir, 'precip': precip}
dframe = pd.DataFrame(data=d, index=date)
fo = '/home/rvalenzuela/Github/pythonx/BBY01_Sfcmet.csv'
dframe.to_csv(fo)
