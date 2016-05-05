"""
This is the interface for interacting with
the uwnetid subscription web service.
"""

import logging
import json
from restclients.dao import Uwnetid_DAO
from restclients.exceptions import DataFailureException
from restclients.util.timer import Timer
from restclients.util.log import log_info


INVALID_USER_MSG = "No such NetID"
logger = logging.getLogger(__name__)


def get_resource(url):
    timer = Timer()
    response = Uwnetid_DAO().getURL(url, {'Accept': 'application/json'})
    log_info(logger,
             "%s ==status==> %s" % (url, response.status),
             timer)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    #'Bug' with lib API causing requests with no/invalid user to return a 200
    if INVALID_USER_MSG in response.data:
        json_data = json.loads(response.data)
        raise DataFailureException(url, 404, json_data["errorMessage"])

    logger.debug("%s ==data==> %s" % (url, response.data))

    return response.data


def put_resource(url, body):
    timer = Timer()
    response = Uwnetid_DAO().putURL(url, {
        'Content-Type': 'application/json',
        'Acept': 'application/json',
    }, body)
    log_info(logger,
             "%s ==status==> %s" % (url, response.status),
             timer)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    #'Bug' with lib API causing requests with no/invalid user to return a 200
    if INVALID_USER_MSG in response.data:
        json_data = json.loads(response.data)
        raise DataFailureException(url, 404, json_data["errorMessage"])

    logger.debug("%s ==data==> %s" % (url, response.data))

    return response.data
