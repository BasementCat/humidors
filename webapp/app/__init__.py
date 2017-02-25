import json
import os.path

from flask import Flask


def load_config():
    candidate_filenames = ('./humidors-config.json', '~/humidors-config.json', '/etc/humidors-config.json')
    for filename in candidate_filenames:
        filename = os.path.expanduser(filename)
        if os.path.exists(filename):
            with open(filename, 'r') as fp:
                return json.load(fp)

    raise RuntimeError("Can't load a config file in " + ' '.join(candidate_filenames))


def get_app():
    app = Flask(__name__)
    app.config.update(load_config())

    api_prefix = '/api'

    from app.views.api.v1.points import PointsView as api_v1_PointsView

    api_v1_PointsView.add_rule_to_app(app, prefix=api_prefix)

    return app
