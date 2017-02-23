from flask import request

from app.views.api.v1 import APIView_v1


class PointsView(APIView_v1):
    def post(self):
        """\
        Expected data format:
        {
            "sensors": {
                "top": {
                    "humidity": 75.123455, // % humidity
                    "temperature": 29.243513 // degrees in C
                }
                // More named sensors can go here
            }
        }
        """

        print request.json
        return "OK"
