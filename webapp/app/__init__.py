from flask import Flask


def get_app():
    app = Flask(__name__)

    api_prefix = '/api'

    from app.views.api.v1.points import PointsView as api_v1_PointsView

    api_v1_PointsView.add_rule_to_app(app, prefix=api_prefix)

    return app
