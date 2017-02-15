"""
Contains UW Libraries DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation import get_timeout
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.mock_http import MockHTTP


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_HFS_DAO_CLASS = 'restclients.dao_implementation.hfs.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("hfs", "file", url, headers)


HFS_MAX_POOL_SIZE = 10


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_HFS_HOST=''
    RESTCLIENTS_HFS_CERT_FILE='.../cert.cert',
    RESTCLIENTS_HFS_KEY_FILE='.../certs_key.key',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_HFS_HOST,
                settings.RESTCLIENTS_HFS_KEY_FILE,
                settings.RESTCLIENTS_HFS_CERT_FILE,
                max_pool_size=HFS_MAX_POOL_SIZE,
                socket_timeout=get_timeout('hfs'))
        return get_live_url(Live.pool,
                            'GET',
                            settings.RESTCLIENTS_HFS_HOST,
                            url,
                            headers=headers,
                            service_name='hfs')
