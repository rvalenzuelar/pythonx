# Read array 

import numpy as np

file=open('swp.1040216150010.NOAA-D.0.0.5_PPI_v2_V3.vad')

# intialize list
data=[]

# populate list with text data
for line in file:
    cols=line.split()
    row_data=[float(x) for x in cols]
    data.append(row_data)

# convert list to array
data=np.array(data)

file.close()