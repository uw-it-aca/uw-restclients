"""
Contains UW Libraries Currics DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation import get_timeout
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url,\
    post_mockdata_url, delete_mockdata_url, put_mockdata_url
from restclients.mock_http import MockHTTP
import re


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_LIBCURRICS_DAO_CLASS =
    'restclients.dao_implementation.libraries.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("libcurrics", "file", url, headers)


LIB_MAX_POOL_SIZE = 10
LIB_SOCKET_TIMEOUT = 15


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_LIBCURRICS_HOST = '...'
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_LIBCURRICS_HOST,
                max_pool_size=LIB_MAX_POOL_SIZE,
                socket_timeout=get_timeout('library'))

        return get_live_url(Live.pool,
                            'GET',
                            settings.RESTCLIENTS_LIBCURRICS_HOST,
                            url,
                            headers=headers,
                            service_name='libcurrics')
