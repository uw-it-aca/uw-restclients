"""
Contains PWS DAO implementations.
"""

from django.conf import settings
from urllib3 import connection_from_url
import re
from mock import get_mockdata_url

class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_PWS_DAO_CLASS = 'restclients.dao_implementation.pws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("pws", "file", url, headers)

class AlwaysJAverage(object):
    """
    This DAO ensures that all users have javerage's regid
    """
    def getURL(self, url, headers):
        real = File()

        if re.search('/identity/v1/person/([\w]+).json', url):
            return real.getURL('/identity/v1/person/javerage.json', headers)

        return real.getURL(url, headers)


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
            response.headers = {"ETag": "A123BBB"}

            return response


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.

    RESTCLIENTS_PWS_CERT_FILE='/path/to/an/authorized/cert.cert',
    RESTCLIENTS_PWS_KEY_FILE='/path/to/the/certs_key.key',
    RESTCLIENTS_PWS_HOST='https://ucswseval1.cac.washington.edu:443',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool == None:
            key_file = settings.RESTCLIENTS_PWS_KEY_FILE
            cert_file = settings.RESTCLIENTS_PWS_CERT_FILE
            pws_host = settings.RESTCLIENTS_PWS_HOST

            kwargs = {
                "key_file": key_file,
                "cert_file": cert_file,
            }

            Live.pool = connection_from_url(pws_host, **kwargs)

        r = Live.pool.urlopen('GET', url, headers=headers)
        return r
