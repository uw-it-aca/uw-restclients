"""
Contains UW Libraries DAO implementations.
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

    RESTCLIENTS_LIBRARIES_DAO_CLASS =
    'restclients.dao_implementation.libraries.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("libraries", "file", url, headers)


LIB_MAX_POOL_SIZE = 10


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_LIBRARIES_HOST = '...'
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_LIBRARIES_HOST,
                settings.RESTCLIENTS_LIBRARIES_KEY_FILE,
                settings.RESTCLIENTS_LIBRARIES_CERT_FILE,
                max_pool_size=LIB_MAX_POOL_SIZE,
                socket_timeout=get_timeout('library'))

        # For rest router...
        url_prefix = getattr(settings, "RESTCLIENTS_LIBRARIES_PREFIX", "")
        url = "%s%s" % (url_prefix, url)
        return get_live_url(Live.pool,
                            'GET',
                            settings.RESTCLIENTS_LIBRARIES_HOST,
                            url,
                            headers=headers,
                            service_name='libraries')
