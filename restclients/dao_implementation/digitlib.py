"""
Contains web service of curriculum codes DAO implementations.
"""

import re
import logging
from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url, post_mockdata_url
from restclients.dao_implementation.mock import delete_mockdata_url, put_mockdata_url
from restclients.mock_http import MockHTTP


logger = logging.getLogger(__name__)


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_DIGITLIB_DAO_CLASS = 'restclients.dao_implementation.digitlib.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("digitlib", "file", url, headers)


DIGITLIB_MAX_POOL_SIZE = 10
DIGITLIB_SOCKET_TIMEOUT = 15


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_DIGITLIB_HOST
    RESTCLIENTS_DIGITLIB_CERT_FILE
    RESTCLIENTS_DIGITLIB_KEY_FILE
    RESTCLIENTS_DIGITLIB_REDIRECT
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_DIGITLIB_HOST,
                settings.RESTCLIENTS_DIGITLIB_KEY_FILE,
                settings.RESTCLIENTS_DIGITLIB_CERT_FILE,
                max_pool_size=DIGITLIB_MAX_POOL_SIZE,
                socket_timeout=DIGITLIB_SOCKET_TIMEOUT)
        redirect = getattr(settings, 
                           "RESTCLIENTS_DIGITLIB_REDIRECT",
                           True)
        return get_live_url(Live.pool,
                            'GET',
                            settings.RESTCLIENTS_DIGITLIB_HOST,
                            url,
                            headers=headers,
                            redirect=redirect,
                            service_name='digitlib')
