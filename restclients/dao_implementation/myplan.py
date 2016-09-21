"""
Contains MyPlan DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.mock_http import MockHTTP
import re


MAX_POOL_SIZE = 10
HOST = ''  # - TBD


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_MYPLAN_DAO_CLASS = 'restclients.dao_implementation.myplan.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("myplan", "file", url, headers)


class Live(object):
    """
    This DAO provides real data.
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_MYPLAN_HOST,
                settings.RESTCLIENTS_MYPLAN_KEY_FILE,
                settings.RESTCLIENTS_MYPLAN_CERT_FILE,
                max_pool_size=MAX_POOL_SIZE)
        return get_live_url(Live.pool,
                            'GET',
                            HOST,
                            url,
                            headers=headers,
                            service_name='myplan')
