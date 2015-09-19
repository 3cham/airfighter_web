__author__ = 'dang'
from datetime import datetime
import json

import redis
import configinfo


class PubSubModel:
    '''
    A backend for real-time events reporting, every time the receivers send an alert
      it will be save into redis database, redis will publish the events to
       event stream consumed by the browser
    '''

    client = None

    def __init__(self):
        self.connect_db()

    def connect_db(self):
        '''
        initialize the connection to the redis database
        '''
        if self.client is None:
            self.client = redis.StrictRedis(host=configinfo.host, port=configinfo.port)

    def get_room(self, sensor_id):
        return self.client.get(sensor_id)

    def set_room(self, sensor_id, room):
        self.client.set(sensor_id, room)

    def publish_event(self, event):
        now = datetime.now().replace(microsecond=0).time()
        data = {
            "sensor_id":event['sensor_id'],
            "co2_level":event['co2_level'],
            "timestamp":now.__format__("%Y-%m-%d %H:%M:%S"),
            "room": self.get_room(event['sensor_id']),
            "state":event['state']
        }
        self.client.publish(configinfo.event_stream_name, json.dumps(data))

    def get_publisher(self):
        return self.client.pubsub()
