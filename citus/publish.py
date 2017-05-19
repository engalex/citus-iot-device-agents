'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
import sys
import logging
import time
import getopt
import json

# Usage
usageInfo = """Usage:

Use MQTT over TCP on port 8883
$ python publish.py -l <label> -u <unit> -v <value> -t <temperature> -i <humidity>

Use MQTT over WebSocket:
$ python publish.py -l <label> -u <unit> -v <value> -t <temperature> -i <humidity> -w

Type "python publish.py -h" for available options.
"""
# Help info
helpInfo = """-l, --label
	The meaning of value as label
-u, --unit
	The unit of value to measure
-v, --value
	The value of <label> by <unit>
-t, --temperature
	The ambient temperature
-i, --humidity
	The ambient humidity
-w, --websocket
	Use MQTT over WebSocket
-h, --help
	Help information


"""

# Read in command-line parameters
label="Leakage"
unit="PPM"
value=0
temperature=0
humidity=0

useWebsocket = False
host = "iot.ap-northeast-1.amazonaws.com"
if not os.environ.get('DEVICE_ID'):
	print("Missing 'DEVICE_ID' in environment variables")
	exit(1)
rootCAPath = os.environ.get('HOME') + "/.agent/certs/root-CA.crt"
certificatePath = os.environ.get('HOME') + "/.agent/certs/" + os.environ.get('DEVICE_ID') + ".cert.pem"
privateKeyPath = os.environ.get('HOME') + "/.agent/certs/" + os.environ.get('DEVICE_ID') + ".privkey.pem"
clientId = os.environ.get('DEVICE_ID')

try:
	opts, args = getopt.getopt(sys.argv[1:], "hwluv:t:i:", ["help", "label=", "unit=", "value=","temperature=","humidity=", "websocket"])
	if len(opts) == 0:
		raise getopt.GetoptError("No input parameters!")
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print(helpInfo)
			exit(0)
		if opt in ("-l", "--label"):
			label = arg
		if opt in ("-u", "--unit"):
			unit = arg
		if opt in ("-v", "--value"):
			value = arg
		if opt in ("-t", "--temperature"):
			temperature = arg
		if opt in ("-i", "--humidity"):
			humidity = arg
		if opt in ("-w", "--websocket"):
			useWebsocket = True
except getopt.GetoptError:
	print(usageInfo)
	exit(1)

# Building the payload
JSONPayload = {'value':value, 'unit':unit, 'label':label, '@timestamp':int(round(time.time() * 1000)), 'temperature':temperature, 'humidity':humidity, 'ID':os.environ.get('DEVICE_ID')}
print json.dumps(JSONPayload, ensure_ascii=True)

# Missing configuration notification
missingConfiguration = False
if value==0:
	print("Missing '-v' or '--value'")
	missingConfiguration = True
if temperature==0:
	print("Missing '-t' or '--temperature'")
	missingConfiguration = True
if humidity==0:
	print("Missing '-i' or '--humidity'")
	missingConfiguration = True
if missingConfiguration:
	exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
time.sleep(2)

# Publish to the same topic in a loop forever
myAWSIoTMQTTClient.publish("telemetry/sensors", json.dumps(JSONPayload, ensure_ascii=True), 1)
time.sleep(1)
