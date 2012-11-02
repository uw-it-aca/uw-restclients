"""
Contains GWS DAO implementations.
"""
from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url

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
        if Live.pool is None:
            Live.pool = get_con_pool(settings.RESTCLIENTS_GWS_HOST,
                                     settings.RESTCLIENTS_GWS_KEY_FILE,
                                     settings.RESTCLIENTS_GWS_CERT_FILE)
        return get_live_url(Live.pool, 'GET', 
                            settings.RESTCLIENTS_GWS_HOST,
                            url, headers=headers)
