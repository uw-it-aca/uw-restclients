from restclients.dao import DAO
from httplib import HTTPResponse
from restclients.mock_http import MockHTTP

class Always404(object):
    def getURL(self, url, headers):
        response =  MockHTTP()
        response.status = 404
        response.body = "Not found"

        return response
