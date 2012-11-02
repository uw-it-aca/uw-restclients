"""
Contains PWS DAO implementations.
"""

from django.conf import settings
from restclients.mock_http import MockHTTP
import re
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url

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
            Live.pool = get_con_pool(settings.RESTCLIENTS_PWS_HOST,
                                     settings.RESTCLIENTS_PWS_KEY_FILE,
                                     settings.RESTCLIENTS_PWS_CERT_FILE)
        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_PWS_HOST,
                            url, headers=headers)
