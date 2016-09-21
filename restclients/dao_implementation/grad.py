"""
Contains Grad School DAO implementations.
"""

import re
import logging
from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.mock_http import MockHTTP


logger = logging.getLogger(__name__)


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_GRAD_DAO_CLASS =
    'restclients.dao_implementation.grad.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("grad", "file", url, headers)


GRAD_MAX_POOL_SIZE = 10
GRAD_SOCKET_TIMEOUT = 15


class Live(object):
    """
    This DAO provides real data.
    It requires further configuration, e.g.
    RESTCLIENTS_GRAD_HOST
    RESTCLIENTS_GRAD_CERT_FILE
    RESTCLIENTS_GRAD_KEY_FILE
    RESTCLIENTS_GRAD_REDIRECT
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_GRAD_HOST,
                settings.RESTCLIENTS_GRAD_KEY_FILE,
                settings.RESTCLIENTS_GRAD_CERT_FILE,
                max_pool_size=GRAD_MAX_POOL_SIZE,
                socket_timeout=GRAD_SOCKET_TIMEOUT)
        return get_live_url(Live.pool,
                            'GET',
                            settings.RESTCLIENTS_GRAD_HOST,
                            url,
                            headers=headers,
                            service_name='grad')
