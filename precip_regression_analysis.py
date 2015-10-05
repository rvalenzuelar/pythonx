import Meteoframes as mf
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from datetime import datetime

# basedir='/home/rvalenzuela/SURFACE'
basedir='/Users/raulv/Documents/SURFACE'
name_field=['press','temp','rh','wspd','wdir','precip','mixr']

index_field=[3,6,9,10,12,17,26]
altitude=15
bb23=mf.parse_surface(basedir+'/case03/bby01023.met',index_field,name_field,altitude)
bb24=mf.parse_surface(basedir+'/case03/bby01024.met',index_field,name_field,altitude)
frames=[bb23,bb24]
bby=pd.concat(frames)

index_field=[3,4,5,6,8,13,22]
altitude=462
cz23=mf.parse_surface(basedir+'/case03/czc01023.met',index_field,name_field,altitude)
cz24=mf.parse_surface(basedir+'/case03/czc01024.met',index_field,name_field,altitude)
frames=[cz23,cz24]
czd=pd.concat(frames)


foo=bby.preciph
bby_precip=foo[~np.isnan(foo)]

foo=czd.preciph
czd_precip=foo[~np.isnan(foo)]


st=bby_precip.index.searchsorted(datetime(2001,1,23,12))
en=bby_precip.index.searchsorted(datetime(2001,1,23,22))
la=bby_precip.index.searchsorted(datetime(2001,1,24,07))

bby1=bby_precip.ix[st:en]
czd1=czd_precip.ix[st:en]
bby2=bby_precip.ix[en:la]
czd2=czd_precip.ix[en:la]

model1=sm.OLS(czd1,bby1)
model2=sm.OLS(czd2,bby2)

result1=model1.fit()
result2=model2.fit()

Rsq1=result1.rsquared
Rsq2=result2.rsquared

m1=result1.params[0]
m2=result2.params[0]

xr=np.linspace(-2,15,20)

fig,ax=plt.subplots()
ax.plot(range(-1,14),range(-1,14),color=(0.7,0.7,0.7),lw=3)
ax.plot(xr,m1*xr,color='blue',lw=1.5)
ax.plot(xr,m2*xr,color='red',lw=1.5)
ax.scatter(bby1,czd1,marker='o',s=55,color='blue',facecolor='none',zorder=10)
ax.scatter(bby2,czd2,marker='+',s=55,color='red',zorder=20)

''' add text annotations '''
m1txt="{:3.2}".format(m1)
m2txt="{:3.2}".format(m2)
r1txt="{:3.2}".format(Rsq1)
r2txt="{:3.2}".format(Rsq2)
text1='23-12UTC to 23-21UTC\nY='+m1txt+'X\nR-sqr='+r1txt
text2='23-22UTC to 24-06UTC\nY='+m2txt+'X\nR-sqr='+r2txt
ax.text(0.7,0.50,text1,color='blue',weight='bold',transform=ax.transAxes)
ax.text(0.7,0.35,text2,color='red',weight='bold',transform=ax.transAxes)
ax.set_xlim([-1,12])
ax.set_ylim([-1,12])
ax.set_xlabel('Rain rate BBY [mm h-1]')
ax.set_ylabel('Rain rate CZD [mm h-1]')
plt.grid(True)
plt.show()





