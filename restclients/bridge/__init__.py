"""
This module directly interacts with Bridge web services on
It will log the https requests and responses.
Be sure to set the logging configuration if you use the LiveDao!
"""

import logging
from restclients.dao import Bridge_DAO
from restclients.exceptions import DataFailureException
from restclients.util.timer import Timer
from restclients.util.log import log_info, log_err


logger = logging.getLogger(__name__)
DHEADER = {"Content-Type": "application/json",
           'Accept': 'application/json'}
GHEADER = {'Accept': 'application/json'}
PHEADER = {"Content-Type": "application/json",
           'Accept': 'application/json',
           'Connection': 'keep-alive'}


def delete_resource(url):
    timer = Timer()
    response = Bridge_DAO().deleteURL(url, DHEADER)
    log_data = "DELETE %s ==status==> %s" % (url, response.status)

    if response.status != 204:
        # 204 is a successful deletion
        log_err(logger, log_data, timer)
        raise DataFailureException(url, response.status, response.data)

    _log_resp_time(logger, log_data, timer, response)
    return response


def get_resource(url):
    timer = Timer()
    response = Bridge_DAO().getURL(url, GHEADER)
    log_data = "GET %s ==status==> %s" % (url, response.status)

    if response.status != 200:
        log_err(logger, log_data, timer)
        raise DataFailureException(url, response.status, response.data)

    _log_resp_time(logger, log_data, timer, response)
    return response.data


def patch_resource(url, body):
    """
    Patch resource with the given json body
    :returns: http response data
    """
    timer = Timer()
    response = Bridge_DAO().patchURL(url, PHEADER, body)
    log_data = "PATCH %s %s ==status==> %s" % (url, body, response.status)

    if not (response.status == 200 or response.status == 201):
        log_err(logger, log_data, timer)
        raise DataFailureException(url, response.status, response.data)

    _log_resp_time(logger, log_data, timer, response)
    return response.data


def post_resource(url, body):
    """
    Post resource with the given json body
    :returns: http response data
    """
    timer = Timer()
    response = Bridge_DAO().postURL(url, PHEADER, body)
    log_data = "POST %s %s ==status==> %s" % (url, body, response.status)

    if response.status != 200 and response.status != 201:
        # 201 Created
        log_err(logger, log_data, timer)
        raise DataFailureException(url, response.status, response.data)

    _log_resp_time(logger, log_data, timer, response)
    return response.data


def _log_resp_time(logger, log_data, timer, response):
    log_info(logger, log_data, timer)
    logger.info("%s ==data==> %s" % (log_data, response.data))
