import os
import sys
import json
import requests

try:
    headers = {'content-type': 'application/json'}
    params = {'secret_key':os.environ.get('SECRET_KEY')}
    resp = requests.post(os.environ.get('SERVICE_ENDPOINT') + '/apisrv/device-lifecycle-service/lifecycle/registration', params=params, data=sys.argv[1], headers=headers)
    resp.raise_for_status()
    data = json.loads(resp.text)
    with open(os.environ.get('HOME') + '/.agent/certs/' + os.environ.get('DEVICE_ID') + '.cert.pem', 'w') as f:
        f.write(data['certificates']['certificatePem'])
    with open(os.environ.get('HOME') + '/.agent/certs/' + os.environ.get('DEVICE_ID') + '.private.key', 'w') as f:
        f.write(data['certificates']['keyPair']['PrivateKey'])
except requests.exceptions.RequestException as e:
    print 'Eror while retreiving certificate information: {}'.format(e)