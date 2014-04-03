"""
Contains UW Libraries DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url, post_mockdata_url
from restclients.dao_implementation.mock import delete_mockdata_url, put_mockdata_url
from restclients.mock_http import MockHTTP
import re


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_LIBRARIES_DAO_CLASS = 'restclients.dao_implementation.libraries.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("libraries", "file", url, headers)


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_LIBRARIES_HOST='https://mylibinfo.lib.washington.edu/mylibinfo/v1/'
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool == None:
            Live.pool = self._get_pool()
        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_LIBRARIES_HOST,
                            url, headers=headers,
                            service_name='libraries')

    def _get_pool(self):
        libraries_key_file = None
        libraries_cert_file = None
        max_pool_size = 10 #default values
        socket_timeout = 15 #default values

        if settings.RESTCLIENTS_LIBRARIES_KEY_FILE and settings.RESTCLIENTS_LIBRARIES_CERT_FILE:
            libraries_key_file = settings.RESTCLIENTS_LIBRARIES_KEY_FILE
            libraries_cert_file = settings.RESTCLIENTS_LIBRARIES_CERT_FILE

        if hasattr(settings, "RESTCLIENTS_LIBRARIES_MAX_POOL_SIZE"):
            max_pool_size = settings.RESTCLIENTS_LIBRARIES_MAX_POOL_SIZE
        if hasattr(settings, "RESTCLIENTS_LIBRARIES_SOCKET_TIMEOUT"):
            socket_timeout = settings.RESTCLIENTS_LIBRARIES_SOCKET_TIMEOUT

        return get_con_pool(settings.RESTCLIENTS_LIBRARIES_HOST,
                                     libraries_key_file,
                                     libraries_cert_file,
                                     max_pool_size=max_pool_size,
                                     socket_timeout=socket_timeout)
