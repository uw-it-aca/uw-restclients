"""
Contains DAO Cache implementations
"""
from restclients.mock_http import MockHTTP

class NoCache(object):
    def getCache(self, service, url, headers):
        return None

    def processResponse(self, service, url, response):
        pass
