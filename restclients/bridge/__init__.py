"""
This module directly interacts with Bridge web services on
It will log the https requests and responses.
Be sure to set the logging configuration if you use the LiveDao!
"""

import logging
from restclients.dao import Bridge_DAO
from restclients.exceptions import DataFailureException


logger = logging.getLogger(__name__)
DHEADER = {"Content-Type": "application/json",
           'Accept': 'application/json'}
GHEADER = {'Accept': 'application/json'}
PHEADER = {"Content-Type": "application/json",
           'Accept': 'application/json',
           'Connection': 'keep-alive'}


def delete_resource(url):
    response = Bridge_DAO().deleteURL(url, DHEADER)
    log_data = "DELETE %s ==status==> %s" % (url, response.status)

    if response.status != 204:
        # 204 is a successful deletion
        _raise_exception(log_data, url, response)

    _log_resp(log_data, response.data)
    return response


def get_resource(url):
    response = Bridge_DAO().getURL(url, GHEADER)
    log_data = "GET %s ==status==> %s" % (url, response.status)

    if response.status != 200:
        _raise_exception(log_data, url, response)

    _log_resp(log_data, response.data)
    return response.data


def patch_resource(url, body):
    """
    Patch resource with the given json body
    :returns: http response data
    """
    response = Bridge_DAO().patchURL(url, PHEADER, body)
    log_data = "PATCH %s %s ==status==> %s" % (url, body, response.status)

    if response.status != 200:
        _raise_exception(log_data, url, response)

    _log_resp(log_data, response.data)
    return response.data


def post_resource(url, body):
    """
    Post resource with the given json body
    :returns: http response data
    """
    response = Bridge_DAO().postURL(url, PHEADER, body)
    log_data = "POST %s %s ==status==> %s" % (url, body, response.status)

    if response.status != 200 and response.status != 201:
        # 201 Created
        _raise_exception(log_data, url, response)

    _log_resp(log_data, response.data)
    return response.data


def put_resource(url, body):
    """
    Put request with the given json body
    :returns: http response data
    Bridge PUT seems to have the same effect as PATCH currently.
    """
    response = Bridge_DAO().putURL(url, PHEADER, body)
    log_data = "PUT %s %s ==status==> %s" % (url, body, response.status)

    if response.status != 200:
        _raise_exception(log_data, url, response)

    _log_resp(log_data, response.data)
    return response.data


def _log_resp(log_data, response_data):
    logger.info(log_data)
    logger.debug("%s ==data==> %s" % (log_data, response_data))


def _raise_exception(log_data, url, response):
    if response.status == 404:
        logger.warning(log_data)
    else:
        logger.error(log_data)
    raise DataFailureException(url, response.status, response.data)
