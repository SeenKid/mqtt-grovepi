#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from grovepi import *

from paho.mqtt import client as mqtt_client


broker = '' # add mqtt broker
port = 0 # add port
topic = "" # add topic
retain=False
led = 3
qos=0
max_qos = 1

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        var = input("Enter a value for the power of the led between 1 and 255 :") # since it's analog
        int(var)
        int(led)
        analogWrite(led, int(var))
        result = client.publish(topic, msg, qos, retain)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic, with qos `{msg.qos}` and retain `{msg.retain}`")
        analogWrite(led, int(msg.payload.decode()))

    client.subscribe(topic, max_qos)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
