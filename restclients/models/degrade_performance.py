import json


class DegradePerformance(object):
    def __init__(self, serialized=None):
        self.problems = {}

        if serialized:
            self.problems = json.loads(serialized)

    def remove_service(self, service):
        del self.problems[service]

    def set_status(self, service, value):
        self._set(service, "status", value)

    def set_content(self, service, value):
        self._set(service, "content", value)

    def set_load_time(self, service, value):
        self._set(service, "load_time", value)

    def get_status(self, service):
        return self._get(service, "status")

    def get_content(self, service):
        return self._get(service, "content")

    def get_load_time(self, service):
        return self._get(service, "load_time")

    def services(self):
        return self.problems.keys()

    def _set(self, service, key, value):
        self._add_service(service)
        self.problems[service][key] = value

    def _get(self, service, key):
        if service in self.problems:
            if key in self.problems[service]:
                return self.problems[service][key]
        return None

    def _add_service(self, service):
        if service not in self.problems:
            self.problems[service] = {}

    def serialize(self):
        return json.dumps(self.problems)
