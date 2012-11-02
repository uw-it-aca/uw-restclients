"""
The function to get the url for accessing live data from a web service
"""
import logging
from urllib3 import connection_from_url

def get_con_pool(host,
                 key_file,
                 cert_file):
    if key_file is None or cert_file is None:
        return connection_from_url(host)
    kwargs = {
        "key_file": key_file,
        "cert_file": cert_file
        }
    return connection_from_url(host, **kwargs)


def get_live_url(con_pool, 
                 method, 
                 host, 
                 url, 
                 headers):
    """
    The argument con_pool is the http connection pool associated with the service 
    The argument method is the HTTP method i.e., 'GET'
    The argument host is the url of the server host.
    """

    logger = logging.getLogger('restclients.dao_implementation.live')
    logger.info('%s %s%s', method, host, url) 
    return con_pool.urlopen(method, url, headers=headers)


