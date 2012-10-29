"""
Contains GWS DAO implementations.
"""
from django.conf import settings
from urllib3 import connection_from_url
from mock import get_mockdata_url

class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_GWS_DAO_CLASS = 'restclients.dao_implementation.gws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("gws", "file", url, headers)

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
