import json
import sys

import requests

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.mqtt import publish
from lib.config import get_config

def off():
    config = get_config()
    taeget_path = 'http://' + config['air_conditioner_api_server']['host'] + ':' + str(config['air_conditioner_api_server']['port'])
    # off request
    response = requests.delete(f'{taeget_path}/off')
    publish(
        topic = '/'.join([
            config['project_id'],
            'air_conditioner_api_mqtt_agent',
            'state'
        ]),
        # TODO get correct state
        message = json.dumps({
            'isRunning': False,
            'type': 'cool',
            'temperature': 26,
            'dehumidificationLevel': None,
            'airflowLevel': '1' 
        }),
        qos = 0,
        retain = True,
        keepalive = 60,
    )
