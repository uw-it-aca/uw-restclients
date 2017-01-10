"""
Contains KWS DAO implementations.
"""

from django.conf import settings
from restclients.mock_http import MockHTTP
from restclients.dao_implementation import get_timeout
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url


KWS_MAX_POOL_SIZE = 10


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_KWS_DAO_CLASS = 'restclients.dao_implementation.kws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url('kws', 'file', url, headers)


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.

    RESTCLIENTS_KWS_CERT_FILE='/path/to/an/authorized/cert.cert',
    RESTCLIENTS_KWS_KEY_FILE='/path/to/the/certs_key.key',
    RESTCLIENTS_KWS_HOST='https://ucswseval1.cac.washington.edu:443',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(settings.RESTCLIENTS_KWS_HOST,
                                     settings.RESTCLIENTS_KWS_KEY_FILE,
                                     settings.RESTCLIENTS_KWS_CERT_FILE,
                                     max_pool_size=KWS_MAX_POOL_SIZE,
                                     socket_timeout=get_timeout("kws"))
        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_KWS_HOST,
                            url, headers=headers,
                            service_name='kws')
