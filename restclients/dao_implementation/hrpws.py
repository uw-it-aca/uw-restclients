"""
Contains UW HRP DAO implementations.
"""

from os.path import abspath, dirname
from django.conf import settings
from restclients.dao_implementation import get_timeout
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url, \
    post_mockdata_url
from restclients.mock_http import MockHTTP


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_HRPWS_DAO_CLASS =
    'restclients.dao_implementation.hrpws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("hrpws", "file", url, headers)


HRPWS_MAX_POOL_SIZE = 10


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_HRPWS_HOST=''
    RESTCLIENTS_HRPWS_CERT_FILE='.../cert.cert',
    RESTCLIENTS_HRPWS_KEY_FILE='.../certs_key.key',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_HRPWS_HOST,
                settings.RESTCLIENTS_HRPWS_KEY_FILE,
                settings.RESTCLIENTS_HRPWS_CERT_FILE,
                max_pool_size=HRPWS_MAX_POOL_SIZE,
                socket_timeout=get_timeout('hrpws'))
        return get_live_url(Live.pool,
                            'GET',
                            settings.RESTCLIENTS_HRPWS_HOST,
                            url,
                            headers=headers,
                            service_name='hrpws')
