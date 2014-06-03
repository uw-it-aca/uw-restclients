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

    RESTCLIENTS_HFS_DAO_CLASS = 'restclients.dao_implementation.hfs.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("hfs", "file", url, headers)


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_LIBRARIES_HOST=''
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool == None:
            Live.pool = self._get_pool()
        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_HFS_HOST,
                            url, headers=headers,
                            service_name='hfs')

    def _get_pool(self):
        pass
