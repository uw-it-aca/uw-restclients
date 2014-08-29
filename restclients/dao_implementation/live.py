"""
Provides access to the http connection pools and 
connections for live data from a web service

"""
import logging
import ssl
import time
import socket
from urlparse import urlparse
from urllib3 import connection_from_url
from django.conf import settings
from restclients.signals.rest_request import rest_request
from restclients.signals.success import rest_request_passfail


def get_con_pool(host,
                 key_file=None,
                 cert_file=None,
                 socket_timeout=15.0,
                 max_pool_size=3,
                 verify_https=True,
                 is_ssl=True):
    """
    Return a ConnectionPool instance of given host
    :param socket_timeout:
        socket timeout for each connection in seconds
    """
    kwargs = {
        "timeout": socket_timeout,
        "maxsize": max_pool_size,
        "block": True,
        }
    if is_ssl:
        kwargs["ssl_version"] = ssl.PROTOCOL_SSLv3

    if key_file is not None and cert_file is not None:
        kwargs["key_file"] = key_file
        kwargs["cert_file"] = cert_file

    if verify_https and urlparse(host).scheme == "https":
        kwargs["cert_reqs"] = "CERT_REQUIRED"
        kwargs["ca_certs"] = getattr(settings, "RESTCLIENTS_CA_BUNDLE",
                                     "/etc/ssl/certs/ca-bundle.crt")

    return connection_from_url(host, **kwargs)


def get_live_url(con_pool, 
                 method, 
                 host, 
                 url,
                 headers,
                 retries=1,
                 body=None,
                 service_name=None):
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

    start_time = time.time()
    response = con_pool.urlopen(method, url, body=body, headers=headers, retries=retries, timeout=timeout)
    request_time = time.time() - start_time
    rest_request.send(sender='restclients',
                      url=url,
                      request_time=request_time,
                      hostname=socket.gethostname(),
                      service_name=service_name)
    rest_request_passfail.send(sender='restclients',
                               url=url,
                               success=True,
                               hostname=socket.gethostname(),
                               service_name=service_name)

    return response
