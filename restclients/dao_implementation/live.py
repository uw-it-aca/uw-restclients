"""
The function to get the url for accessing live data from a web service
"""
import logging
from urllib3 import connection_from_url

def get_live_url(self, 
                 con_pool, 
                 method, 
                 host, 
                 key_file, 
                 cert_file, 
                 url, 
                 headers):
    """
    The argument con_pool is the http connection pool associated with the service 
    The argument method is the HTTP method i.e., 'GET'
    The argument host is the url of the server host.
    """
    if con_pool == None:
        if key_file is not None and cert_file is not None:
            kwargs = {
                "key_file": key_file,
                "cert_file": cert_file,
            }

            con_pool = connection_from_url(host, **kwargs)
    else:
        Live.pool = connection_from_url(host)

    logger = logging.getLogger('restclients.dao_implementation.live')
    logger.info('%s %s%s', method, host, url) 
    return con_pool.urlopen(method, url, headers=headers)

