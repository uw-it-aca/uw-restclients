"""
Contains DAO implementations that always return specific errors.
Used for unit testing.
"""

from restclients.mock_http import MockHTTP
from restclients_core.dao import DAO


class Always404(object):
    """
    Always404 will return a 404 for any URL given.
    """
    def __init__(self, *args, **kwargs):
        pass

    def getURL(self, url, headers):
        """
        This method takes a partial url, e.g. "/v1/person/123AAAAA" and
        a dictionary of headers.

        Returns an object that can be used like an HTTPResponse object.
        """
        return self.load(None, None, None, None)

    def is_mock(self):
        return True

    def load(self, method, url, headers, body):
        response = MockHTTP()
        response.status = 404
        response.data = "Not found"
        return response


class Always500(object):
    """
    Always500 will return a 500 for any URL given.
    """
    def __init__(self, *args, **kwargs):
        pass

    def getURL(self, url, headers):
        """
        This method takes a partial url, e.g. "/v1/person/123AAAAA" and
        a dictionary of headers.

        Returns an object that can be used like an HTTPResponse object.
        """
        return self.load(None, None, None, None)

    def is_mock(self):
        return True

    def load(self, method, url, headers, body):
        response = MockHTTP()
        response.status = 500
        response.data = ""

        return response
