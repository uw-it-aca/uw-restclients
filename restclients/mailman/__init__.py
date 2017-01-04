"""
This is the interface for interacting with the mailman web service.
"""

import json
import logging
from restclients.dao import Mailman_DAO
from restclients.exceptions import DataFailureException
from restclients.util.timer import Timer
from restclients.util.log import log_info


logger = logging.getLogger(__name__)


def get_resource(url):
    timer = Timer()
    response = Mailman_DAO().getURL(url, {'Accept': 'application/json'})
    log_info(logger,
             "%s ==status==> %s" % (url, response.status),
             timer)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    logger.debug("%s ==data==> %s" % (url, response.data))

    return response.data


def post_resource(url, body):
    timer = Timer()
    response = Mailman_DAO().postURL(url, {
        'Content-Type': 'application/json',
        'Acept': 'application/json',
    }, body)
    log_info(logger,
             "%s ==status==> %s" % (url, response.status),
             timer)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    logger.debug("%s ==data==> %s" % (url, response.data))

    return response.data
