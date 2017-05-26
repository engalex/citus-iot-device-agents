import os
import sys
import json
import time
import requests

try:
    resp = requests.get(os.environ.get('SERVICE_ENDPOINT') + '/geoip')
    data = json.loads(resp.text)
    GEO_LOCATION=data['address']
    GEO_LATITUDE=data['latitude']
    GEO_LONGITUDE=data['longitude']
    DEVICE_NAME='FPT-' + os.uname()[1]
    data={'name':os.environ.get('DEVICE_ID'),'owner':sys.argv[1],'_metadata':{'name':DEVICE_NAME,'type': 'Default','location': GEO_LOCATION,'latitude': GEO_LATITUDE,'longitude': GEO_LONGITUDE,'lastModified':int(round(time.time() * 1000))}}
    print data
    headers = {'content-type': 'application/json'}
    params = {'secret_key':os.environ.get('SECRET_KEY')}
    result = requests.post(os.environ.get('SERVICE_ENDPOINT') + '/apisrv/device-lifecycle-service/device/' + os.environ.get('DEVICE_ID') + '/_metadata', params=params, data=json.dumps(data), headers=headers)    
    result.raise_for_status()
    print result.__dict__
except requests.exceptions.RequestException as e:
    print 'Eror while updating device information: {}'.format(e)