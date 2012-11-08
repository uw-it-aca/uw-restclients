from restclients.mock_http import MockHTTP
from os.path import abspath, dirname

"""
A centralized the mock data access 
"""

def get_mockdata_url(service_name, implementation_name, 
                     url, headers,
                     dir_base = dirname(__file__)):
    """
    :param service_name:
        possible "sws", "pws", "book", "hfs", etc.
    :param implementation_name:
        possible values: "file", etc.
    """
        
    RESOURCE_ROOT = abspath(dir_base + "/../resources/" + 
                            service_name + "/" + implementation_name)
    if url == "///":
        # Just a placeholder to put everything else in an else.
        # If there are things that need dynamic work, they'd go here
        pass
    else:
        try:
            handle = open(RESOURCE_ROOT + url)
        except IOError:
            try:
                handle = open(RESOURCE_ROOT + url + "/index.html")
            except IOError:
                response = MockHTTP()
                response.status = 404
                return response
            
        response = MockHTTP()
        response.status = 200
        response.data = handle.read()
        response.headers = { "X-Data-Source": service_name + " file mock data", }
        return response

