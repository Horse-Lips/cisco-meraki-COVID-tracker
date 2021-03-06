"""
* Camera functionality
* Subscribes to an MQTT broker for a 
* camera with the given serial number
"""
import meraki
import django
import time
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cisco_dashboard.settings')
django.setup()

from main.models import Snapshot
from main.models import Device
from main.models import Network
from datetime import datetime

import paho.mqtt.client as mqtt


serial = None
key    = None

try:
    serial = sys.argv[1]
except:
    print("No serial provided")
    sys.exit(0)

try:
    key = sys.argv[2]
except:
    print("No API key provided")
    sys.exit(0)

dash = meraki.DashboardAPI(key, output_log = False, print_console = False, suppress_logging = False)


def on_connect(client, userData, flags, rc):
    """
    * Callback function for client connection
    * Means a CONNACK was received
    """
    client.subscribe("/merakimv/" + serial + "/raw_detections")


previous_time = None
def on_message(client, userData, msg):
    """
    * Callback function
    * Means client received publish message from MQTT broker
    """
    if len(eval(msg.payload)['objects']) >= 0:
        timestamp = datetime.fromtimestamp(time.time()).isoformat()
        response = dash.camera.generateDeviceCameraSnapshot(serial, ts = timestamp)

        snapDevice = None

        if (previous_time is None or (previous_time + 60) < time.time()):
            try:
                snapDevice = Device.objects.filter(devSerial = serial)[0]
                snapOrg = snapDevice.net.org

                new_snapshot = Snapshot.objects.create(
                    org = snapOrg,
                    url = response['url'],
                    time = str(timestamp)
                )
                new_snapshot.save()
                
                time.sleep(60)
            except:
                print("Device not found")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()
