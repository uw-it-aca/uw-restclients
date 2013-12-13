"""
Provides access to the http connection pools and 
connections for live data from a web service

"""
import logging
from urllib3 import connection_from_url
from django.conf import settings


def get_con_pool(host,
                 key_file=None,
                 cert_file=None,
                 socket_timeout=15.0,
                 max_pool_size=3):
    """
    Return a ConnectionPool instance of given host
    :param socket_timeout:
        socket timeout for each connection in seconds
    """
    if key_file is None or cert_file is None:
        return connection_from_url(host,
                                   timeout=socket_timeout,
                                   maxsize=max_pool_size)
    kwargs = {
        "key_file": key_file,
        "cert_file": cert_file,
        "timeout": socket_timeout,
        "maxsize": max_pool_size,
        }
    return connection_from_url(host, **kwargs)


def get_live_url(con_pool, 
                 method, 
                 host, 
                 url,
                 headers,
                 retries=1,
                 body=None):
    """
    Return a connection from the pool and perform an HTTP request.
    :param con_pool:
        is the http connection pool associated with the service 
    :param method:
        HTTP request method (such as GET, POST, PUT, etc.)
    :param host:
        the url of the server host.
    :param headers:
        headers to include with the request
    :param body:
        the POST, PUT body of the request
    """
    timeout = getattr(settings, "RESTCLIENTS_TIMEOUT", con_pool.timeout)
    return con_pool.urlopen(method, url, body=body, headers=headers, retries=retries, timeout=timeout)
