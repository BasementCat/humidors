from flask.views import MethodView


class APIView(MethodView):
    api_version = None
    path = None

    @classmethod
    def get_path(self):
        if self.path:
            return self.path
        elif self.__name__.endswith('View'):
            return self.__name__[:-4].lower()
        else:
            return self.__name__

    @classmethod
    def get_rule(self):
        if self.api_version is None:
            raise RuntimeError("An API version is required")
        return '/v{}/{}'.format(self.api_version, self.get_path())

    @classmethod
    def add_rule_to_app(self, app, prefix=None):
        rule = self.get_rule()
        app.add_url_rule(
            (prefix or '') + rule,
            view_func=self.as_view(rule.strip('/').replace('/', '_').lower())
        )
