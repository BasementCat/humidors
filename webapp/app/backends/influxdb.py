from __future__ import absolute_import

from flask import current_app
from influxdb import InfluxDBClient

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
                    'time': sensor['timestamp'],
                    'fields': {
                        'temperature_c': sensor['temperature_c'],
                        'temperature_f': sensor['temperature_f'],
                        'humidity': sensor['humidity'],
                    },
                })

        self.client.write_points(influxdb_points)
