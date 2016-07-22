"""
Contains UW NetID DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url, \
    post_mockdata_url
from restclients.mock_http import MockHTTP
from os.path import abspath, dirname


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_UWNETID_DAO_CLASS =
    'restclients.dao_implementation.uwnetid.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("uwnetid", "file", url, headers)

    def postURL(self, url, headers, body):
        response = post_mockdata_url("uwnetid", "file", url, headers, body)
        if response.status == 400:
            return response

        path = abspath("%s/../resources/uwnetid/file%s.POST" % (
            dirname(__file__), url))

        try:
            handle = open(path)
            response.data = handle.read()
            response.status = 200
        except IOError:
            response.status = 404

        return response


UWNETID_MAX_POOL_SIZE = 10
UWNETID_SOCKET_TIMEOUT = 15


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_UWNETID_HOST=''
    RESTCLIENTS_UWNETID_CERT_FILE='.../cert.cert',
    RESTCLIENTS_UWNETID_KEY_FILE='.../certs_key.key',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_UWNETID_HOST,
                settings.RESTCLIENTS_UWNETID_KEY_FILE,
                settings.RESTCLIENTS_UWNETID_CERT_FILE,
                max_pool_size=UWNETID_MAX_POOL_SIZE,
                socket_timeout=UWNETID_SOCKET_TIMEOUT)
        return get_live_url(Live.pool,
                            'GET',
                            settings.RESTCLIENTS_UWNETID_HOST,
                            url,
                            headers=headers,
                            service_name='uwnetid')

    def postURL(self, url, headers, body):
        if Live.pool is None:
            Live.pool = get_con_pool(
                settings.RESTCLIENTS_UWNETID_HOST,
                settings.RESTCLIENTS_UWNETID_KEY_FILE,
                settings.RESTCLIENTS_UWNETID_CERT_FILE,
                max_pool_size=UWNETID_MAX_POOL_SIZE,
                socket_timeout=UWNETID_SOCKET_TIMEOUT)
        return get_live_url(Live.pool,
                            'POST',
                            settings.RESTCLIENTS_UWNETID_HOST,
                            url,
                            headers=headers,
                            body=body,
                            service_name='uwnetid')
