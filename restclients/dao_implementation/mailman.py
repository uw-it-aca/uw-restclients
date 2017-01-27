"""
Contains Mailman DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation import get_timeout
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_MAILMAN_DAO_CLASS =\
        'restclients.dao_implementation.mailman.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("mailman", "file", url, headers)


MAILMAN_MAX_POOL_SIZE = 10


class Live(object):
    """
    This DAO provides real data. It requires further configuration, e.g.
    RESTCLIENTS_MAILMAN_HOST=''
    RESTCLIENTS_MAILMAN_KEY=''
    """
    pool = None
    host = None

    def __init__(self):
        self.set_pool()

    def set_pool(self):
        if Live.host is None:
            Live.host = settings.RESTCLIENTS_MAILMAN_HOST
        if Live.pool is None:
            Live.pool = get_con_pool(
                Live.host,
                max_pool_size=MAILMAN_MAX_POOL_SIZE,
                socket_timeout=get_timeout('mailman'))

    def getURL(self, url, headers):
        return get_live_url(Live.pool,
                            'GET',
                            Live.host,
                            url,
                            headers=headers,
                            service_name='mailman')
