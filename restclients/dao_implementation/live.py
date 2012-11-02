"""
Provides access to the http connection pools and 
connections for live data from a web service

"""
import logging
from urllib3 import connection_from_url

def get_con_pool(host,
                 key_file,
                 cert_file,
                 socket_timeout=3.0,
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
                 retries=1):
    """
    Return a connection from the pool and perform an HTTP request.
    :param con_pool:
        is the http connection pool associated with the service 
    :param method:
        HTTP request method (such as GET, POST, PUT, etc.)
    :param host:
        the url of the server host.
    
    """

    logger = logging.getLogger('restclients.dao_implementation.live')
    logger.info('%s %s%s', method, host, url) 
    return con_pool.urlopen(method, url, headers=headers, retries=retries)


