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

    log_info(logger, log_data, timer)
    logger.debug("%s ==data==> %s" % (log_data, response.data))
    return response


def get_resource(url):
    timer = Timer()
    response = Bridge_DAO().getURL(url, GHEADER)
    log_data = "GET %s ==status==> %s" % (url, response.status)

    if response.status != 200:
        log_err(logger, log_data, timer)
        raise DataFailureException(url, response.status, response.data)

    log_info(logger, log_data, timer)
    logger.debug("%s ==data==> %s" % (log_data, response.data))
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

    log_info(logger, log_data, timer)
    logger.debug("%s ==data==> %s" % (log_data, response.data))
    return response.data


def put_resource(url, body):
    """
    Put resource with the given json body
    :returns: http response data
    """
    timer = Timer()
    response = Bridge_DAO().putURL(url, PHEADER, body)
    log_data = "PUT %s %s ==status==> %s" % (url, body, response.status)

    if not (response.status == 200 or response.status == 201):
        log_err(logger, log_data, timer)
        raise DataFailureException(url, response.status, response.data)

    log_info(logger, log_data, timer)
    logger.debug("%s ==data==> %s" % (log_data, response.data))
    return response.data
