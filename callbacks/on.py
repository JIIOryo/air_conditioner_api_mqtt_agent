import json
import sys

import requests

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.mqtt import publish
from lib.config import get_config

config = get_config()
taeget_path = 'http://' + config['air_conditioner_api_server']['host'] + ':' + str(config['air_conditioner_api_server']['port'])\

def on_hot(message: str) -> None:
    on_requestby_temperature(type_ = 'hot', message = message)

def on_cool(message: str) -> None:
    on_requestby_temperature(type_ = 'cool', message = message)

def on_requestby_temperature(type_: str, message: str) -> None:
    if type_ not in ['hot', 'cool']:
        raise ValueError # TODO new Error

    req = json.loads(message)
    temperature = req['temperature']
    airflow_level = req['airflowLevel']

    try:
        response = requests.put(
            url = f'{taeget_path}/on/{type_}',
            json = {
                'temperature': temperature,
                'airflowLevel': airflow_level,
            }
        )
        status_code = response.status_code
        api_state = status_code == 200
    except:
        return # TODO publish error
    
    publish_message = json.dumps({
        'isRunning': True,
        'type': type_,
        'temperature': temperature,
        'dehumidificationLevel': None,
        'airflowLevel': airflow_level,
    })

    print(publish_message)

    publish(
        topic = '/'.join([
            config['project_id'],
            'air_conditioner_api_mqtt_agent',
            'state'
        ]),
        message = publish_message,
        qos = 0,
        retain = True,
        keepalive = 60,
    )
    return

def on_dehumidify(message: str) -> None:
    req = json.loads(message)
    dehumidification_level = req['dehumidificationLevel']
    airflow_level = req['airflowLevel']

    try:
        response = requests.put(
            url = f'{taeget_path}/on/dehumidify',
            json = {
                'dehumidificationLevel': dehumidification_level,
                'airflowLevel': airflow_level,
            }
        )
        status_code = response.status_code
        api_state = status_code == 200
    except:
        return # TODO publish error

    publish_message = json.dumps({
        'isRunning': True,
        'type': 'dehumidify',
        'temperature': None,
        'dehumidificationLevel': dehumidification_level,
        'airflowLevel': airflow_level,
    })

    print(publish_message)

    publish(
        topic = '/'.join([
            config['project_id'],
            'air_conditioner_api_mqtt_agent',
            'state'
        ]),
        message = publish_message,
        qos = 0,
        retain = True,
        keepalive = 60,
    )
    return
