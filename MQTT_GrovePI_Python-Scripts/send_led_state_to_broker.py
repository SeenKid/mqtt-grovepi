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
qos=0
max_qos=1

led = 3
var1 = -1
poten = 0
 
pinMode(led,"OUTPUT")
pinMode(poten, "INPUT")
time.sleep(0.1)

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
        var = analogRead(poten)
        while(var != var1):
            result = client.publish(topic, var, qos, retain)
            var = var1
            analogWrite(led, var//4)
        time.sleep(1)
        msg = f"messages: {msg_count}"
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
