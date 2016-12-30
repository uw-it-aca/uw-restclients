"""
Contains Bridge DAO implementations.
"""
import os
import base64
from os.path import abspath, dirname
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url,\
    convert_to_platform_safe, post_mockdata_url, delete_mockdata_url,\
    put_mockdata_url, patch_mockdata_url, read_resp_data
from django.conf import settings


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_BRIDGE_DAO_CLASS = 'restclients.dao_implementation.bridge.File'
    """
    def getURL(self, url, headers):
        response = get_mockdata_url("bridge", "file", url, headers)
        if response.status == 200:
            return response

        new_url = url + ".GET"
        return get_mockdata_url("bridge", "file", url, headers)

    def patchURL(self, url, headers, body):
        patch_url = url + ".PATCH"
        response = patch_mockdata_url("bridge", "file",
                                      patch_url, headers, body)
        if response.status == 400:
            return response
        return read_resp_data("bridge", "file", patch_url, response)

    def putURL(self, url, headers, body):
        put_url = url + ".PUT"
        response = put_mockdata_url("bridge", "file",
                                    put_url, headers, body)
        if response.status == 400:
            return response
        return read_resp_data("bridge", "file", put_url, response)

    def postURL(self, url, headers, body):
        post_url = url + ".POST"
        response = post_mockdata_url("bridge", "file", post_url, headers, body)
        if response.status == 400:
            return response
        return read_resp_data("bridge", "file", post_url, response)

    def deleteURL(self, url, headers):
        del_url = url + ".DELETE"
        response = delete_mockdata_url("bridge", "file", del_url, headers)
        return read_resp_data("bridge", "file", del_url, response)


BRIDGE_MAX_POOL_SIZE = 10
BRIDGE_SOCKET_TIMEOUT = 30


class Live(object):
    """
    This DAO provides real data.  It requires the following configuration:

    RESTCLIENTS_BRIDGE_HOST="https://uw.bridgeapp.com/"
    RESTCLIENTS_BRIDGE_BASIC_AUTH_KEY="..."
    RESTCLIENTS_BRIDGE_BASIC_AUTH_SECRET="..."
    """
    pool = None
    host = None

    def __init__(self):
        self.set_pool()

    def set_pool(self):
        if Live.pool is None or Live.host is None:
            Live.host = settings.RESTCLIENTS_BRIDGE_HOST
            Live.pool = get_con_pool(Live.host,
                                     verify_https=True,
                                     max_pool_size=BRIDGE_MAX_POOL_SIZE,
                                     socket_timeout=BRIDGE_SOCKET_TIMEOUT)

    def get_basic_auth(self):
        return "%s:%s" % (settings.RESTCLIENTS_BRIDGE_BASIC_AUTH_KEY,
                          settings.RESTCLIENTS_BRIDGE_BASIC_AUTH_SECRET)

    def add_basicauth_header(self, headers):
        basic_auth_value = base64.urlsafe_b64encode(self.get_basic_auth())
        headers["Authorization"] = "Basic %s" % basic_auth_value
        return headers

    def getURL(self, url, headers):
        return get_live_url(Live.pool, 'GET',
                            Live.host, url,
                            headers=self.add_basicauth_header(headers),
                            service_name='bridge')

    def patchURL(self, url, headers, body):
        return get_live_url(Live.pool, 'PATCH',
                            Live.host, url,
                            headers=self.add_basicauth_header(headers),
                            body=body,
                            service_name='bridge')

    def putURL(self, url, headers, body):
        return get_live_url(Live.pool, 'PUT',
                            Live.host, url,
                            headers=self.add_basicauth_header(headers),
                            body=body,
                            service_name='bridge')

    def postURL(self, url, headers, body):
        return get_live_url(Live.pool, 'POST',
                            Live.host, url,
                            headers=self.add_basicauth_header(headers),
                            body=body,
                            service_name='bridge')

    def deleteURL(self, url, headers):
        return get_live_url(Live.pool, 'DELETE',
                            Live.host, url,
                            headers=self.add_basicauth_header(headers),
                            service_name='bridge')
