import time

from flask import request, abort

from app.views.api.v1 import APIView_v1


class PointsParser(object):
    def __init__(self, data):
        self.points = []
        self.interval = None
        self.state = 'root'

        lines = map(lambda l: l.split(), filter(None, map(str.strip, data.split('\n'))))
        self.parse(lines)

    def parse(self, lines):
        for line in lines:
            try:
                reparse = False
                while True:
                    self.state, reparse = getattr(self, 'parse_' + self.state + '_line')(*line)
                    if not reparse:
                        break
            except Exception as e:
                abort(400, "Malformed line '{}' - {}: {}".format(' '.join(line), e.__class__.__name__, str(e)))

    def require_args(self, num, args):
        if len(args) != num:
            raise ValueError("Expected {} args, got {}".format(num, len(args)))

    def parse_int(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValueError("Invalid integer value")

    def parse_float(self, value):
        try:
            return float(value)
        except ValueError:
            raise ValueError("Invalid float value")

    def parse_root_line(self, keyword, *args):
        if keyword == 'INTERVAL':
            self.require_args(1, args)
            self.interval = self.parse_int(args[0])
            return 'root', False
        elif keyword == 'POINT':
            self.require_args(0, args)
            self.points.append([])
            return 'point', False
        else:
            raise ValueError("Invalid root keyword")

    def parse_point_line(self, keyword, *args):
        if keyword == 'SENSOR':
            self.require_args(1, args)
            self.points[-1].append({'sensor': args[0]})
            return 'sensor', False
        else:
            raise ValueError("Invalid point keyword")

    def parse_sensor_line(self, keyword, *args):
        if keyword in ('HUMIDITY', 'TEMPERATURE'):
            self.require_args(1, args)
            self.points[-1][-1][keyword.lower()] = self.parse_float(args[0])
            return 'sensor', False
        elif keyword == 'SENSOR':
            return 'point', True
        elif keyword == 'POINT':
            return 'root', True
        else:
            raise ValueError("Invalid sensor keyword")


class PointsView(APIView_v1):
    def post(self):
        """\
        Expected data format:
        INTERVAL 1000
        POINT
            SENSOR top
                HUMIDITY 75.123455
                TEMPERATURE 29.243513

        "INTERVAL" is the interval between points in ms.  The points sections
        are ordered by time, ascending - the last section is assumed to be at
        the current time.

        A "POINT" section is a collection of datapoints for a variety of sensors
        at a given point in time.  The point section may be repeated any number
        of times, and leading whitespace and blank lines are ignored.

        A "SENSOR" section is the data from one sensor for a given point in
        time.  A point may contain data from many sensors.  The sensor name,
        given after the keyword, may be any string not containing a newline.

        Each "SENSOR" section should contain a "TEMPERATURE" and "HUMIDITY". The
        temperature is a floating point number specified in degrees celsius, and
        the humidity is the percent humidity, also floating point
        """

        now = time.time()
        res = PointsParser(request.data)
        for point in reversed(res.points):
            for sensor in point:
                sensor['timestamp'] = now
            now += (res.interval / 1000.0)
        return "OK"
