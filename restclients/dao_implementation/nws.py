"""
Contains NWS DAO implementations.
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

    RESTCLIENTS_NWS_DAO_CLASS = 'restclients.dao_implementation.nws.File'
    """
    def getURL(self, url, headers):
        #Removes expires_after tag in channel search requests
        if "v1/channel?" in url:
            url = re.sub('&expires_after=[^&]*', '', url)
        return get_mockdata_url("nws", "file", url, headers)

    def postURL(self, url, headers, body):
        return post_mockdata_url("nws", "file", url, headers, body)

    def putURL(self, url, headers, body):
        return put_mockdata_url("nws", "file", url, headers, body)

    def deleteURL(self, url, headers):
        return delete_mockdata_url("nws", "file", url, headers)


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_NWS_HOST='https://notify-dev.s.uw.edu/notification/'
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool == None:
            Live.pool = self._get_pool()
        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_NWS_HOST,
                            url, headers=headers,
                            service_name='nws')

    def deleteURL(self, url, headers):
        if Live.pool == None:
            Live.pool = self._get_pool()
        return get_live_url(Live.pool, 'DELETE',
                            settings.RESTCLIENTS_NWS_HOST,
                            url, headers=headers,
                            service_name='nws')

    def postURL(self, url, headers, body):
        if Live.pool == None:
            Live.pool = self._get_pool()
        return get_live_url(Live.pool, 'POST',
                            settings.RESTCLIENTS_NWS_HOST,
                            url, headers=headers, body=body,
                            service_name='nws')

    def putURL(self, url, headers, body):
        if Live.pool == None:
            Live.pool = self._get_pool()
        return get_live_url(Live.pool, 'PUT',
                            settings.RESTCLIENTS_NWS_HOST,
                            url, headers=headers, body=body,
                            service_name='nws')


    def _get_pool(self):
        nws_key_file = None
        nws_cert_file = None
        max_pool_size = 10 #default values
        socket_timeout = 15 #default values

        if settings.RESTCLIENTS_NWS_KEY_FILE and settings.RESTCLIENTS_NWS_CERT_FILE:
            nws_key_file = settings.RESTCLIENTS_NWS_KEY_FILE
            nws_cert_file = settings.RESTCLIENTS_NWS_CERT_FILE

        if hasattr(settings, "RESTCLIENTS_NWS_MAX_POOL_SIZE"):
            max_pool_size = settings.RESTCLIENTS_NWS_MAX_POOL_SIZE
        if hasattr(settings, "RESTCLIENTS_NWS_SOCKET_TIMEOUT"):
            socket_timeout = settings.RESTCLIENTS_NWS_SOCKET_TIMEOUT

        return get_con_pool(settings.RESTCLIENTS_NWS_HOST,
                                     nws_key_file,
                                     nws_cert_file,
                                     max_pool_size=max_pool_size,
                                     socket_timeout=socket_timeout)
