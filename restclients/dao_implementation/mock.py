from restclients.mock_http import MockHTTP
from os.path import abspath, dirname

"""
A centralized the mock data access 
"""

def get_mockdata_url(service_name, implementation_name, url, headers):
    """
    The service_name is somthing like "sws", "pws", "book", "hfs"
    The implementation_name is somthing like "file", etc.
    """
        
    RESOURCE_ROOT = abspath(dirname(__file__) + "/../resources/" + 
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

