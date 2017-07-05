import os
import sys
import json
import time
import requests

try:
    resp = requests.get(os.environ.get('SERVICE_ENDPOINT') + '/geoip')
    data = json.loads(resp.text)
    GEO_LOCATION=data['address']
    GEO_LATITUDE=str(data['latitude'])
    GEO_LONGITUDE=str(data['longitude'])
    DEVICE_NAME='FPT-' + os.uname()[1]
    TIMESTAMP=str(int(round(time.time() * 1000)))
    data={'name':os.environ.get('DEVICE_ID'),'owner':os.environ.get('DEVICE_OWNER'),'_metadata':{'name':DEVICE_NAME,'type': 'Default','location': GEO_LOCATION,'latitude': GEO_LATITUDE,'longitude': GEO_LONGITUDE,'lastModified': TIMESTAMP}}    
    headers = {'content-type': 'application/json', }
    params = '?owner=' + os.environ.get('DEVICE_OWNER') + '&secret_key=' + os.environ.get('SECRET_KEY')
    result = requests.put(os.environ.get('SERVICE_ENDPOINT') + '/apisrv/device-management-service/device/' + os.environ.get('DEVICE_ID') + '/_metadata' + params, data=json.dumps(data), headers=headers)    
    result.raise_for_status()    
except requests.exceptions.RequestException as e:
    print 'Eror while updating device information: {}'.format(e)