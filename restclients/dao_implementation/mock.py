from restclients.mock_http import MockHTTP
from os.path import abspath, dirname
import json

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
        response.headers = {"X-Data-Source": service_name + " file mock data", }

        try:
            headers = open(handle.name + '.http-headers')
            response.headers = dict(response.headers.items() + json.loads(headers.read()).items())
        except IOError:
            pass

        return response


def post_mockdata_url(service_name, implementation_name,
                     url, headers, body,
                     dir_base = dirname(__file__)):
    """
    :param service_name:
        possible "sws", "pws", "book", "hfs", etc.
    :param implementation_name:
        possible values: "file", etc.
    """
    #Currently this post method does not return a response body
    response = MockHTTP()
    if body is not None:
        if "dispatch" in url:
            response.status = 200
        else:
            response.status = 201
        response.headers = {"X-Data-Source": service_name + " file mock data", "Content-Type": headers['Content-Type']}
    else:
        response.status = 400
        response.data = "Bad Request: no POST body"
    return response


def put_mockdata_url(service_name, implementation_name,
                     url, headers, body,
                     dir_base = dirname(__file__)):
    """
    :param service_name:
        possible "sws", "pws", "book", "hfs", etc.
    :param implementation_name:
        possible values: "file", etc.
    """
    #Currently this put method does not return a response body
    response = MockHTTP()
    if body is not None:
        response.status = 204
        response.headers = {"X-Data-Source": service_name + " file mock data", "Content-Type": headers['Content-Type']}
    else:
        response.status = 400
        response.data = "Bad Request: no POST body"
    return response


def delete_mockdata_url(service_name, implementation_name,
                     url, headers,
                     dir_base = dirname(__file__)):
    """
    :param service_name:
        possible "sws", "pws", "book", "hfs", etc.
    :param implementation_name:
        possible values: "file", etc.
    """
    #Http response code 204 No Content:
    #The server has fulfilled the request but does not need to return an entity-body
    response = MockHTTP()
    response.status = 204

    return response
