"""
This is the interface for interacting with the UW Libraries Web Service.
"""

import logging
from restclients.dao import Libraries_DAO
from restclients.exceptions import DataFailureException
from restclients.util.timer import Timer
from restclients.util.log import log_info


INVALID_USER_MSG = "User not found"
logger = logging.getLogger(__name__)


def get_resource(url):
    dao = Libraries_DAO()
    timer = Timer()
    response = dao.getURL(url, {})
    log_info(logger,
             "%s ==status==> %s" % (url, response.status),
             timer)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    #'Bug' with lib API causing requests with no/invalid user to return a 200
    if INVALID_USER_MSG in response.data:
        raise DataFailureException(url, 404, response.data)

    logger.debug("%s ==data==> %s" % (url, response.data))

    return response.data
