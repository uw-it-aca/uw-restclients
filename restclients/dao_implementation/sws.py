"""
Contains SWS DAO implementations.
"""

from django.conf import settings
from restclients.mock_http import MockHTTP
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url

# XXX - this is arbitrary.  I didn't have a handy multi-threaded sws test
# case that went over 4 concurrent connections.  Just took the PWS number
SWS_MAX_POOL_SIZE = 10

class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.sws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("sws", "file", url, headers)

    def putURL(self, url, headers, body):
        response = MockHTTP()
        if body is not None:
            response.status = 200
            response.headers = {"X-Data-Source": "SWS file mock data"}
            response.data = body
        else:
            response.status = 400
            response.data = "Bad Request: no PUT body"

        return response

class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.

    RESTCLIENTS_SWS_CERT_FILE='/path/to/an/authorized/cert.cert',
    RESTCLIENTS_SWS_KEY_FILE='/path/to/the/certs_key.key',
    RESTCLIENTS_SWS_HOST='https://ucswseval1.cac.washington.edu:443',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = self._get_pool()

        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_SWS_HOST,
                            url, headers=headers)

    def putURL(self, url, headers, body):
        if Live.pool is None:
            Live.pool = self._get_pool()

        return get_live_url(Live.pool, 'PUT',
                            settings.RESTCLIENTS_SWS_HOST,
                            url, headers=headers, body=body)

    def _get_pool(self):
        return get_con_pool(settings.RESTCLIENTS_SWS_HOST,
                            settings.RESTCLIENTS_SWS_KEY_FILE,
                            settings.RESTCLIENTS_SWS_CERT_FILE,
                            max_pool_size=SWS_MAX_POOL_SIZE)
