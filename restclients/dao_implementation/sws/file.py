from restclients.mock_http import MockHTTP
from os.path import abspath, dirname

class File(object):
    def getURL(self, url, headers):
        RESOURCE_ROOT = abspath(dirname(__file__)+"/../../resources/file")
        if url == "///":
            # Just a placeholder to put everything else in an else.
            # If there are things that need dynamic work, they'd go here
            pass
        else:
            try:
                f = open(RESOURCE_ROOT+url)
            except IOError:
                try:
                    f = open(RESOURCE_ROOT+url+"/index.html")
                except IOError:
                    response = MockHTTP()
                    response.status = 404
                    return response

            response = MockHTTP()
            response.status = 200
            response.body = f.read()
            return response
