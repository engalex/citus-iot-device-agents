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
    data=sys.argv[1]
    headers = {'content-type': 'application/json'}
    params = {'secret_key':os.environ.get('SECRET_KEY')}
    result = requests.post(os.environ.get('SERVICE_ENDPOINT') + '/apisrv/device-lifecycle-service/device/' + os.environ.get('DEVICE_ID') + '/_metadata', params=params, data=json.dumps(data), headers=headers)
    print result.__dict__
    print data    
    result.raise_for_status()    
except requests.exceptions.RequestException as e:
    print 'Eror while updating device information: {}'.format(e)