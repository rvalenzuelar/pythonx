import scipy.io as sio
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import numpy as np


def main():

	mat=sio.loadmat('/home/raul/Downloads/czc_cal_sprof_01023_120gates.mat')

	dayt=mat['czc_sprof_dayt']
	dbz=mat['czc_sprof_dbz']
	ht=mat['czc_sprof_ht']
	vvel=mat['czc_sprof_vvel']

	dayt2 = np.asarray([datenum_to_datetime(x) for x in dayt])

	fig,ax=plt.subplots(2,1,sharex=True)
	ax[0].imshow(dbz.T,origin='lower',interpolation='none')
	# ax[1].imshow(vvel.T,origin='lower',interpolation='none',cmap='bwr')
	plt.show()


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

main()