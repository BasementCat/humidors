class Backend(object):
    def write_points(self, points):
        """\
        Expected format of points:
        [
            [
                {
                    "timestamp": 1487989919.126896, 
                    "sensor": "top", 
                    "temperature_c": 29.243513, 
                    "temperature_f": 29.243513, 
                    "humidity": 75.123455
                }, 
                {
                    "timestamp": 1487989919.126896, 
                    "sensor": "thing", 
                    "temperature_c": 29.243513, 
                    "temperature_f": 29.243513, 
                    "humidity": 75.123455
                }
            ], 
            [
                {
                    "timestamp": 1487989918.126896, 
                    "sensor": "top", 
                    "temperature_c": 29.243513, 
                    "temperature_f": 29.243513, 
                    "humidity": 75.123455
                }, 
                {
                    "timestamp": 1487989918.126896, 
                    "sensor": "thing", 
                    "temperature_c": 29.243513, 
                    "temperature_f": 29.243513, 
                    "humidity": 75.123455
                }
            ]
        ]
        """
        raise NotImplementedError()


class BackendError(Exception):
    pass


class InvalidConfigurationError(BackendError):
    pass


class CommunicationError(BackendError):
    pass
