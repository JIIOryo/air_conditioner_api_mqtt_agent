import datetime
import json
import os
import subprocess
import time
import traceback

import paho.mqtt.client as mqtt

from lib.config import *

from callbacks.util import ack, reboot
from callbacks.on import on_cool, on_hot, on_dehumidify
from callbacks.off import off

config = get_config()
PROJECT_ID = config['project_id']
HOST = config['broker']
PORT = config['port']
USERNAME = config['username']
PASSWORD = config['password']
PROTOCOL = mqtt.MQTTv311
KEEPALIVE = config['keepalive']
QOS = config['qos']

TOPIC_PREFIX = f'{PROJECT_ID}/air_conditioner_api_mqtt_agent/'

PUBLISH_TOPIC_MAP = {
    "STATE": "state",
    "ACK": "ack",
}

SUBSCRIBE_TOPIC_MAP = {
    "PING":"ping",
    "REBOOT":"reboot",
    "ON_COOL": "on/cool",
    "ON_HOT": "on/hot",
    "ON_DEHUMIDIFY": "on/dehumidify",
    "OFF": "off"
}
SUBSCRIBE_TOPICS = [(TOPIC_PREFIX + topic, QOS) for topic in SUBSCRIBE_TOPIC_MAP.values()]
print(SUBSCRIBE_TOPICS)

def topic_router(topic: str, message: str): 
    if topic == TOPIC_PREFIX + SUBSCRIBE_TOPIC_MAP['PING']: ack()
    elif topic == TOPIC_PREFIX + SUBSCRIBE_TOPIC_MAP['REBOOT']: reboot()
    elif topic == TOPIC_PREFIX + SUBSCRIBE_TOPIC_MAP['ON_COOL']: on_cool(message)
    elif topic == TOPIC_PREFIX + SUBSCRIBE_TOPIC_MAP['ON_HOT']: on_hot(message)
    elif topic == TOPIC_PREFIX + SUBSCRIBE_TOPIC_MAP['ON_DEHUMIDIFY']: on_dehumidify(message)
    elif topic == TOPIC_PREFIX + SUBSCRIBE_TOPIC_MAP['OFF']: off()   
    return

def on_connect(client, userdata, flags, rc):
    print('Result Code: {}\n'.format(rc))
    client.subscribe(SUBSCRIBE_TOPICS)

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode())
    try: topic_router(topic = msg.topic, message = msg.payload.decode())
    except Exception as e:
        print(e)
        pass # TODO log

def main():
    client = mqtt.Client(protocol = PROTOCOL)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOST, port = PORT, keepalive = KEEPALIVE)
    client.loop_forever()
    
if __name__ == '__main__': main()
