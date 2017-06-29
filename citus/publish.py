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
import random
from decimal import *

# Usage
usageInfo = """Usage:

Use MQTT over TCP on port 8883
$ citus-device send -p <topic> -v <value> -t <temperature> -i <humidity> -l <label> -u <unit> -s <samples>

Use MQTT over WebSocket:
$ citus-device send -p <topic> -v <value> -t <temperature> -i <humidity> -l <label> -u <unit> -s <samples> -w  

Type "citus-device send -h" for available options.
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
-p, --topic
	The topic to send
-s, --samples
	The number of samples
-w, --websocket
	Use MQTT over WebSocket
-h, --help
	Help information


"""
getcontext().prec = 2
# Read in command-line parameters
topic="telemetry/sensors"
label="Leakage"
unit="PPM"
value=random.uniform(1, 100)
temperature=random.uniform(10, 40)
humidity=random.uniform(60, 90)
number_of_samples=10

useWebsocket = False
host = "a1t67w73z7o66l.iot.ap-northeast-1.amazonaws.com"
if not os.environ.get('DEVICE_ID'):
	print("Missing 'DEVICE_ID' in environment variables")
	exit(1)
rootCAPath = os.environ.get('HOME') + "/.agent/certs/root-CA.crt"
certificatePath = os.environ.get('HOME') + "/.agent/certs/" + os.environ.get('DEVICE_ID') + ".cert.pem"
privateKeyPath = os.environ.get('HOME') + "/.agent/certs/" + os.environ.get('DEVICE_ID') + ".private.key"
clientId = os.environ.get('DEVICE_ID')
deviceOwner = os.environ.get('DEVICE_OWNER')

try:
	opts, args = getopt.getopt(sys.argv[1:], "hwlus:v:t:i:p", ["help", "topic=", "label=", "unit=", "value=","temperature=","humidity=", "samples=", "websocket"])	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print(helpInfo)
			exit(0)
		if opt in ("-p", "--topic"):
			topic = arg
		if opt in ("-l", "--label"):
			label = arg
		if opt in ("-u", "--unit"):
			unit = arg
		if opt in ("-v", "--value"):
			value = float(arg)
		if opt in ("-t", "--temperature"):
			temperature = float(arg)
		if opt in ("-i", "--humidity"):
			humidity = float(arg)
		if opt in ("-s", "--samples"):
			number_of_samples = int(arg)
		if opt in ("-w", "--websocket"):
			useWebsocket = True
except getopt.GetoptError:
	print(usageInfo)	
	exit(1)

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

count = 0
while (count < number_of_samples):
	# Building the payload
	JSONPayload = {'value':float(round(value,2)), 'unit':unit, 'label':label, '@timestamp':int(round(time.time() * 1000)), 'temperature':float(round(temperature,2)), 'humidity':float(round(humidity,2)), 'ID':clientId, 'ownerID':deviceOwner}
	print json.dumps(JSONPayload, ensure_ascii=True)
	# Publish to the same topic in a loop forever
	myAWSIoTMQTTClient.publish(topic, json.dumps(JSONPayload, ensure_ascii=True), 1)
	value=random.uniform(1, 100)
	temperature=random.uniform(10, 40)
	humidity=random.uniform(60, 90)
	unit = (unit=="PPM"? "kWh": unit)
	count = count + 1
	time.sleep(1)

print("Shuting down the sending process...")
time.sleep(10)
