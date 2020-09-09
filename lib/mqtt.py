import sys

from paho.mqtt.publish import single

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.config import get_config

config = get_config()

def publish(
        topic: str,
        message: str,
        qos: int = 1,
        retain: bool = False,
        keepalive: int = 60,
    ) -> None:
    auth = {
        'username': config['username'], 
        'password': config['password'],
    }
    single(
        topic = topic,
        payload = message,
        qos = qos,
        retain = retain,
        hostname = config['broker'],
        port = config['port'],
        keepalive = keepalive,
        auth = auth
    )
 