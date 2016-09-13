"""
Contains Bridge DAO implementations.
"""

from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url,\
    convert_to_platform_safe, post_mockdata_url, delete_mockdata_url,\
    put_mockdata_url, patch_mockdata_url
from django.conf import settings
from os.path import abspath, dirname


def make_resp_body(url, response):
    path = abspath(dirname(__file__) + "/../resources/bridge/file" +
                   url)
    try:
        handle = open(path)
        response.data = handle.read()
        response.status = 200
    except IOError:
        response.status = 404
    return response


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
        patch_url = convert_to_platform_safe(url) + ".PATCH"
        response = patch_mockdata_url("bridge", "file",
                                      patch_url, headers, body)
        if response.status == 400:
            return response
        return make_resp_body(patch_url, response)

    def putURL(self, url, headers, body):
        put_url = convert_to_platform_safe(url) + ".PUT"
        response = put_mockdata_url("bridge", "file",
                                    put_url, headers, body)
        if response.status == 400:
            return response
        return make_resp_body(put_url, response)

    def postURL(self, url, headers, body):
        post_url = convert_to_platform_safe(url) + ".POST"
        response = post_mockdata_url("bridge", "file", post_url, headers, body)
        if response.status == 400:
            return response
        return make_resp_body(post_url, response)

    def deleteURL(self, url, headers):
        del_url = convert_to_platform_safe(url) + ".DELETE"
        response = delete_mockdata_url("bridge", "file", url, headers)
        if response.status == 400:
            return response
        return make_resp_body(del_url, response)


BRIDGE_MAX_POOL_SIZE = 5
BRIDGE_SOCKET_TIMEOUT = 10


class Live(object):
    """
    This DAO provides real data.  It requires the following configuration:

    RESTCLIENTS_BRIDGE_HOST="https://uw.bridgeapp.com/"
    RESTCLIENTS_BRIDGE_BASIC_AUTH_KEY="..."
    RESTCLIENTS_BRIDGE_BASIC_AUTH_SECRET="..."
    """
    pool = None
    host = None

    def get_basic_auth(self):
        return "%s:%s" % (settings.RESTCLIENTS_BRIDGE_BASIC_AUTH_KEY,
                          settings.RESTCLIENTS_BRIDGE_BASIC_AUTH_SECRET)

    def add_basicauth_header(self, headers):
        basic_auth_value = base64.urlsafe_b64encode(self.get_basic_auth())
        headers["Authorization"] = "Basic %s" % basic_auth_value
        return headers

    @staticmethod
    def set_pool(self):
        if Live.pool is None:
            self.host = settings.RESTCLIENTS_BRIDGE_HOST
            max_pool_size = getattr(settings,
                                    "RESTCLIENTS_BRIDGE_MAX_POOL_SIZE",
                                    BRIDGE_MAX_POOL_SIZE)
            socket_timeout = getattr(settings,
                                     "RESTCLIENTS_BRIDGE_SOCKET_TIMEOUT",
                                     BRIDGE_SOCKET_TIMEOUT),
            Live.pool = get_con_pool(self.host,
                                     verify_https=True,
                                     max_pool_size=max_pool_size,
                                     socket_timeout=socket_timeout)

    def getURL(self, url, headers):
        self.set_pool()
        return get_live_url(Live.pool, 'GET',
                            self.host, url,
                            headers=self.add_basicauth_header(headers),
                            service_name='bridge')

    def patchURL(self, url, headers, body):
        self.set_pool()
        return get_live_url(Live.pool, 'PATCH',
                            self.host, url,
                            headers=self.add_basicauth_header(headers),
                            body=body,
                            service_name='bridge')

    def putURL(self, url, headers, body):
        self.set_pool()
        return get_live_url(Live.pool, 'PUT',
                            self.host, url,
                            headers=self.add_basicauth_header(headers),
                            body=body,
                            service_name='bridge')

    def postURL(self, url, headers, body):
        self.set_pool()
        return get_live_url(Live.pool, 'POST',
                            self.host, url,
                            headers=self.add_basicauth_header(headers),
                            body=body,
                            service_name='bridge')

    def deleteURL(self, url, headers):
        self.set_pool()
        return get_live_url(Live.pool, 'DELETE',
                            self.host, url,
                            headers=self.add_basicauth_header(headers),
                            service_name='bridge')
