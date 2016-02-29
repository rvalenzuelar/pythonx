'''
 Reads csv file in google cloud storage using Google API

 Low performance for large mat files

 Raul Valenzuela
 raul.valenzuela@colorado.edu
'''

import io
# import scipy.io as sio
from apiclient import discovery
from oauth2client.client import GoogleCredentials
from apiclient.http import MediaIoBaseDownload

credentials = GoogleCredentials.get_application_default()
service = discovery.build('storage', 'v1', credentials=credentials)
req = service.objects().get_media(bucket='surface-bby',
                                  object='BBY01_Sfcmet.csv')
fh = io.BytesIO()
# fh = io.StringIO()
downloader = MediaIoBaseDownload(fh, req, chunksize=1024 * 1024)
done = False
while not done:
    status, done = downloader.next_chunk()
    if status:
        print 'Download %d%%.' % int(status.progress() * 100)
print 'Download complete'

# downloader.next_chunk()
