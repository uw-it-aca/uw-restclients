"""
Contains GWS DAO implementations.
"""
from restclients.mock_http import MockHTTP
from os.path import abspath, dirname
from django.conf import settings
from urllib3 import connection_from_url


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.gws.File'
    """
    def getURL(self, url, headers):
        RESOURCE_ROOT = abspath(dirname(__file__) + "/../resources/gws/file")
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
            response.headers = { "X-Data-Source": "SWS File Mock Data", }
            return response

class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.

    RESTCLIENTS_GWS_CERT_FILE='/path/to/an/authorized/cert.cert',
    RESTCLIENTS_GWS_KEY_FILE='/path/to/the/certs_key.key',
    RESTCLIENTS_GWS_HOST='https://iam-tools.u.washington.edu:443',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool == None:
            key_file = settings.RESTCLIENTS_GWS_KEY_FILE
            cert_file = settings.RESTCLIENTS_GWS_CERT_FILE
            gws_host = settings.RESTCLIENTS_GWS_HOST

            kwargs = {
                "key_file": key_file,
                "cert_file": cert_file,
            }

            Live.pool = connection_from_url(gws_host, **kwargs)

        r = Live.pool.urlopen('GET', url, headers=headers)
        return r
