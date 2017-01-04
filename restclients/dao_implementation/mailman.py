"""
Contains Mailman DAO implementations.
"""

from django.conf import settings
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url,\
    convert_to_platform_safe, post_mockdata_url, delete_mockdata_url,\
    put_mockdata_url, patch_mockdata_url, read_resp_data
from django.conf import settings


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_MAILMAN_DAO_CLASS =
    'restclients.dao_implementation.mailman.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("mailman", "file", url, headers)

    def putURL(self, url, headers, body):
        put_url = url + ".PUT"
        response = put_mockdata_url("mailman", "file",
                                    put_url, headers, body)
        if response.status == 400:
            return response
        return read_resp_data("mailman", "file", put_url, response)

    def postURL(self, url, headers, body):
        post_url = url + ".POST"
        response = post_mockdata_url("mailman", "file",
                                     post_url, headers, body)
        if response.status == 400:
            return response
        return read_resp_data("mailman", "file", post_url, response)


MAILMAN_MAX_POOL_SIZE = 10
MAILMAN_SOCKET_TIMEOUT = 15


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_MAILMAN_HOST=''
    RESTCLIENTS_MAILMAN_CERT_FILE='.../cert.cert',
    RESTCLIENTS_MAILMAN_KEY_FILE='.../certs_key.key',
    """
    pool = None
    host = None

    def __init__(self):
        self.set_pool()

    def set_pool(self):
        if Live.pool is None or Live.host is None:
            Live.host = settings.RESTCLIENTS_MAILMAN_HOST
            Live.pool = get_con_pool(Live.host,
                                     verify_https=True,
                                     max_pool_size=MAILMAN_MAX_POOL_SIZE,
                                     socket_timeout=MAILMAN_SOCKET_TIMEOUT)

    def getURL(self, url, headers):
        return get_live_url(Live.pool, 'GET',
                            Live.host, url,
                            headers=headers,
                            service_name='mailman')

    def putURL(self, url, headers, body):
        return get_live_url(Live.pool, 'PUT',
                            Live.host, url,
                            headers=headers,
                            body=body,
                            service_name='mailman')

    def postURL(self, url, headers, body):
        return get_live_url(Live.pool, 'POST',
                            Live.host, url,
                            headers=headers,
                            body=body,
                            service_name='mailman')
