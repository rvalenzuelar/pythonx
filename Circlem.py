# -*- coding: utf-8 -*-
"""
    Make circle pojected on a map

    Raul Valenzuela
    January, 2106
"""

from geographiclib.geodesic import Geodesic



def pick_circle_point(lon, lat, az, radius):
  
    gd = Geodesic.WGS84.Direct(lat, lon, az,  radius)  
    lon2=gd['lon2']
    lat2=gd['lat2']

    return lon2,lat2

def circle(m, olat, olon, radius):
    """
    m = basemap instance
    olon = origin lon
    olat = origin lat
    radius = radius
    """
    X = []
    Y = []
    for azimuth in range(0, 360):
        lon2, lat2 = pick_circle_point(olon, olat, azimuth, radius)
        X.append(lon2)
        Y.append(lat2)
    X.append(X[0])
    Y.append(Y[0])

    proj_x, proj_y = m(X, Y)
    return zip(proj_x, proj_y)
    
def sector(m, olat, olon, radius, sector):
    X = [olon]
    Y = [olat]
    for azimuth in sector:
        lon2, lat2 = pick_circle_point(olon, olat, azimuth, radius)
        X.append(lon2)
        Y.append(lat2)
    X.append(X[0])
    Y.append(Y[0])
    
#    print zip(X,Y)

    proj_x, proj_y = m(X,Y)
    return zip(proj_x, proj_y)    
    
    