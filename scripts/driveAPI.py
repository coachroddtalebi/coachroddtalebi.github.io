# input:
# $python driveAPI.py "Sheet Name"

### using google Drive API for Sheets export to csv
# http://wescpy.blogspot.com/2016/07/exporting-google-sheet--as-csv.html

### Authorization
# http://wescpy.blogspot.com/2014/11/authorized-google-api-access-from-python.html
from __future__ import print_function
import argparse
import os
import sys

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

home_dir = "/Users/Rodd/Desktop/websites/roddtalebi.github.io/scripts/"

SCOPES = (
    "https://www.googleapis.com/auth/drive.readonly"
    ) # Read-only access to file content or metadata

CLIENT_SECRET = (
    home_dir + "driveAPI/client_id.json"
    ) #file where creds are stored

#security code
store = file.Storage(home_dir + 'driveAPI/storage.json')
creds = store.get()
if not creds or creds.invalid:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    creds = tools.run_flow(flow, store)


DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http())) # define API
SRC_MIMETYPE = 'application/vnd.google-apps.spreadsheet'
DST_MIMETYPE = 'text/csv'

if len(sys.argv) > 1:
    FILENAME = sys.argv[1]
else:
    FILENAME = 'Attendance'

# Query components are conjoined with the "and" keyword, so your query string will look like this: q='name="%s" and mimeType="%s"' % (FILENAME, SRC_MIMETYPE).
files = DRIVE.files().list(
    q='name="%s" and mimeType="%s"' % (FILENAME, SRC_MIMETYPE),
    orderBy='modifiedTime desc,name').execute().get('files', [])
# orderBy...^sorts files so that if there are duplicate files, it picks the most recently modified
if files:
    # creates file name...'SHEETNAME.csv'
    fn = '%s.csv' % os.path.splitext(home_dir + '../data/' + files[0]['name'].replace(' ', '_'))[0]

    print('Exporting "%s" as "%s"... ' % (files[0]['name'], fn), end='')
    data = DRIVE.files().export(fileId=files[0]['id'], mimeType=DST_MIMETYPE).execute()
    if data:
        with open(fn, 'wb') as f:
            f.write(data)
        print('DONE')
    else:
        print('ERROR (could not download file)')
else:
    print('!!! ERROR: File not found')