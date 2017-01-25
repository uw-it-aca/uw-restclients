"""
Contains UPass DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation import get_timeout
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url


MAX_POOL_SIZE = 10
HOST = settings.RESTCLIENTS_UPASS_HOST


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_UPASS_DAO_CLASS = 'restclients.dao_implementation.upass.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("upass", "file", url, headers)


class Live(object):
    """
    This DAO provides real data.
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_UPASS_DAO_CLASS,
                settings.RESTCLIENTS_UPASS_KEY_FILE,
                settings.RESTCLIENTS_UPASS_CERT_FILE,
                max_pool_size=MAX_POOL_SIZE,
                socket_timeout=get_timeout('upass'))
        return get_live_url(Live.pool,
                            'GET',
                            HOST,
                            url,
                            headers=headers,
                            service_name='upass')
