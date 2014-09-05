"""
Contains R25 DAO implementations.
"""

from django.conf import settings
from restclients.mock_http import MockHTTP
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
import datetime
import hashlib
import pytz


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_R25_DAO_CLASS = 'restclients.dao_implementation.r25.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("r25", "file", url, headers)


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_R25_HOST
    """
    pool = None

    def getURL(self, url, headers):
        host = settings.RESTCLIENTS_R25_HOST

        if Live.pool is None:
            Live.pool = get_con_pool(host)

        return get_live_url(Live.pool, "GET", host, url, headers=headers)
