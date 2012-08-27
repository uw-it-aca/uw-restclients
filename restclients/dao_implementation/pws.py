"""
Contains PWS DAO implementations.
"""
from restclients.mock_http import MockHTTP
from os.path import abspath, dirname


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_PWS_DAO_CLASS = 'restclients.dao_implementation.pws.File'
    """
    def getURL(self, url, headers):
        RESOURCE_ROOT = abspath(dirname(__file__) + "/../resources/pws/file")
        if url == "///":
            # Just a placeholder to put everything else in an else.
            # If there are things that need dynamic work, they'd go here
            pass
        else:
            try:
                handle = open(RESOURCE_ROOT + url)
            except IOError:
                try:
                    handle = open(RESOURCE_ROOT + url + "/index.html")
                except IOError:
                    response = MockHTTP()
                    response.status = 404
                    return response

            response = MockHTTP()
            response.status = 200
            response.data = handle.read()
            return response

class ETag(object):
    """
    The ETag DAO is a testing DAO, that is just here for
    testing the ETag cache class.  You don't want to use it
    for anything else.
    """
    def getURL(self, url, headers):
        if "If-None-Match" in headers and url == "/same":
            response = MockHTTP()
            response.status = 304
            return response

        else:
            response = MockHTTP()
            response.status = 200
            response.data = "Body Content"
            response.headers = { "ETag": "A123BBB" }

            return response



