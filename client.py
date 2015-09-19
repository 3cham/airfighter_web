__author__ = 'dang'

import paho.mqtt.client as mqtt
import requests
import json

#server_address = "http://87.106.23.44:8000/api/push/"
server_address = "http://localhost:8000/api/push/"
last_id = None
last_payload = None
# The callback for when the client receives a CONNACK response from the server.

with open("id.txt","wb") as idfile:
    idfile.write("")

with open("payload.txt","wb") as idfile:
    idfile.write("")

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("io/skybus/sensors5/#")


# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    with open("id.txt", 'rb') as idfile:
        last_id = idfile.read()
        if last_id == "":
            last_id = None

    with open("payload.txt", 'rb') as plfile:
        last_payload = plfile.read()
        if last_payload == "":
            last_payload = None

    if "rf" in msg.payload:
        last_payload = str(msg.payload)
    else:
        last_id = str(msg.payload)

    if last_id is not None and last_payload is not None:
        print last_payload
        last_payload = eval(last_payload)
        data = {
            "sensor_id": last_id,
            "rf":last_payload["rf"],
            "C":last_payload["C"]
        }
        requests.post(url=server_address, data=json.dumps(data))

    if last_id is not None:
        with open("id.txt",'wb') as idfile:
            idfile.write(str(last_id))

    if last_payload is not None:
        with open("payload.txt", 'wb') as plfile:
            plfile.write(str(last_payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("gcp5.skybus.io", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()