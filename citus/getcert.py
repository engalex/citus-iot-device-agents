import os
import sys
import json
import requests

try:
    headers = {'content-type': 'application/json'}
    params = {'secret_key':os.environ.get('SECRET_KEY')}
    resp = requests.get(os.environ.get('SERVICE_ENDPOINT') + '/' + sys.argv[1] + '/certificates', params=params, headers=headers)
    resp.raise_for_status()
    data = json.loads(resp.text)
    with open(os.environ.get('HOME') + '/.agent/certs/' + os.environ.get('DEVICE_ID') + '.cert.pem', 'w') as f:
        f.write(data['certificatePem'])
    with open(os.environ.get('HOME') + '/.agent/certs/' + os.environ.get('DEVICE_ID') + '.private.key', 'w') as f:
        f.write(data['keyPair']['PrivateKey'])
except requests.exceptions.RequestException as e:
    print 'Eror while retreiving certificate information: {}'.format(e)