"""
Contains NWS DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.mock_http import MockHTTP


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_NWS_DAO_CLASS = 'restclients.dao_implementation.nws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("nws", "file", url, headers)


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_NWS_HOST='https://notify-dev.s.uw.edu/notification/'
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool == None:
            Live.pool = get_con_pool(settings.RESTCLIENTS_NWS_HOST,
                                     None,
                                     None,
                                     max_pool_size=settings.RESTCLIENTS_NWS_MAX_POOL_SIZE)
        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_NWS_HOST,
                            url, headers=headers)
