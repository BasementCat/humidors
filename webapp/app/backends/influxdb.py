from __future__ import absolute_import
from datetime import datetime

from flask import current_app
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

from requests import ConnectionError, HTTPError

from app import backends


class InfluxDBBackend(backends.Backend):
    def __init__(self):
        try:
            self.client = InfluxDBClient(
                current_app.config.get('INFLUXDB_HOST', 'localhost'),
                current_app.config.get('INFLUXDB_PORT', 8086),
                current_app.config.get('INFLUXDB_USER'),
                current_app.config.get('INFLUXDB_PASS'),
                current_app.config['INFLUXDB_DATABASE']
            )
        except KeyError as e:
            raise backends.InvalidConfigurationError("Missing configuration key: " + str(e))

    def write_points(self, points):
        influxdb_points = []
        for point in points:
            for sensor in point:
                influxdb_points.append({
                    'measurement': 'temp_humid',
                    'tags': {
                        'sensor': sensor['sensor'],
                    },
                    'time': datetime.utcfromtimestamp(sensor['timestamp']).isoformat(),
                    'fields': {
                        'temperature_c': sensor['temperature_c'],
                        'temperature_f': sensor['temperature_f'],
                        'humidity': sensor['humidity'],
                    },
                })

        try:
            self.client.write_points(influxdb_points)
        except ConnectionError as e:
            raise backends.CommunicationError("Can't connect: " + str(e))
        except HTTPError as e:
            raise backends.CommunicationError("Operation failed: " + str(e))
        except InfluxDBClientError as e:
            raise backends.CommunicationError("Write failed: " + str(e))
