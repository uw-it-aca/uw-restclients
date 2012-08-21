"""
Contains SWS DAO implementations.
"""
from restclients.mock_http import MockHTTP
from os.path import abspath, dirname


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.sws.File'
    """
    def getURL(self, url, headers):
        RESOURCE_ROOT = abspath(dirname(__file__) + "/../resources/sws/file")
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
            response.body = handle.read()
            return response


class HTTP(object):
    """
    This is just here to show where an alternate, more productiony DAO
    implementation might live.
    """
    pass
