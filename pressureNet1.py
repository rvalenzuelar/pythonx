# import urllib2

# data=urllib2.urlopen('https://pressurenet.io/live/?min_lat=40&max_lat=45&min_lon=-80&max_lon=-75&start_time=1430956800000&end_time=1430956860000&api_key=e7d13070f8c64380b3808bc8e71d1501&format=json')
# content=data.read()
# print content


import pandas as pd

url='https://pressurenet.io/live/?min_lat=40&max_lat=45&min_lon=-80&max_lon=-75&start_time=1430956800000&end_time=1430956860000&api_key=e7d13070f8c64380b3808bc8e71d1501&format=json'
df = pd.read_json(url)

print df
