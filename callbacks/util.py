import json
import subprocess
import sys

import requests

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.mqtt import publish
from lib.config import get_config

def ack():
    config = get_config()
    taeget_path = 'http://' + config['air_conditioner_api_server']['host'] + ':' + str(config['air_conditioner_api_server']['port'])
    # off request
    try:
        response = requests.get(f'{taeget_path}/ping')
        status_code = response.status_code
        api_state = status_code == 200
    except:
        api_state = False

    publish(
        topic = '/'.join([
            config['project_id'],
            'air_conditioner_api_mqtt_agent',
            'ack'
        ]),
        message = json.dumps({
        "mqttAgent": True,
        "airConditionerApi": api_state
    }),
        qos = 0,
        retain = False,
        keepalive = 60,
    )

def reboot():
    cmd = 'sudo reboot'
    subprocess.Popen(cmd.split())

