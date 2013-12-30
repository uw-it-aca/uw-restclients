from restclients.mock_http import MockHTTP
from os.path import abspath, dirname
from django.conf import settings
from django.utils.importlib import import_module
import sys
import os
import json
import logging

"""
A centralized the mock data access
"""
# Based on django.template.loaders.app_directories
fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
app_resource_dirs = []
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError, e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))

    resource_dir = os.path.join(os.path.dirname(mod.__file__), 'resources')
    if os.path.isdir(resource_dir):
        # Cheating, to make sure our resources are overridable
        data = {
            'path': resource_dir.decode(fs_encoding),
            'app': app,
        }
        if app == 'restclients':
            app_resource_dirs.append(data)
        else:
            app_resource_dirs.insert(0, data)

def get_mockdata_url(service_name, implementation_name,
                     url, headers):

    """
    :param service_name:
        possible "sws", "pws", "book", "hfs", etc.
    :param implementation_name:
        possible values: "file", etc.
    """

    dir_base = dirname(__file__)



    RESOURCE_ROOT = abspath(dir_base + "/../resources/" +
                            service_name + "/" + implementation_name)

    file_path = None
    success = False

    for resource_dir in app_resource_dirs:
        response = _load_resource_from_path(resource_dir, service_name,
                                            implementation_name, url, headers)

        if response:
            return response

    # If no response has been found in any installed app, return a 404
    response = MockHTTP()
    response.status = 404
    return response

def _load_resource_from_path(resource_dir, service_name, implementation_name,
                                url, headers):

    RESOURCE_ROOT = os.path.join(resource_dir['path'],
                                    service_name,
                                    implementation_name)
    app = resource_dir['app']

    if url == "///":
        # Just a placeholder to put everything else in an else.
        # If there are things that need dynamic work, they'd go here
        pass
    else:
        try:
            file_path = RESOURCE_ROOT + url
            handle = open(file_path)
        except IOError:
            try:
                file_path = RESOURCE_ROOT + url + "/index.html"
                handle = open(file_path)
            except IOError:
                return

        logger = logging.getLogger(__name__)
        logger.info("URL: %s; App: %s; File: %s" % (url, app, file_path))

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
