"""
Contains DAO implementations that always return specific errors.
Used for unit testing.
"""

from restclients.mock_http import MockHTTP


class Always404(object):
    """
    Always404 will return a 404 for any URL given.
    """
    def getURL(self, url, headers):
        response = MockHTTP()
        response.status = 404
        response.body = "Not found"

        return response


class Always500(object):
    """
    Always500 will return a 500 for any URL given.
    """
    def getURL(self, url, headers):
        response = MockHTTP()
        response.status = 500
        response.body = ""

        return response
