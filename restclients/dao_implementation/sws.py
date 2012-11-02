"""
Contains SWS DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url

class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.sws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("sws", "file", url, headers)

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
            Live.pool = get_con_pool(settings.RESTCLIENTS_SWS_HOST,
                                     settings.RESTCLIENTS_SWS_KEY_FILE,
                                     settings.RESTCLIENTS_SWS_CERT_FILE)
        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_SWS_HOST,
                            url, headers=headers)

