from restclients.mock_http import MockHTTP

class Always500(object):
    def getURL(self, url, headers):
        response =  MockHTTP()
        response.status = 500
        response.body = ""

        return response
