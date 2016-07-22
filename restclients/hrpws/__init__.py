"""
This is the interface for interacting with
the hrp web service.
"""

import logging
import json
from restclients.dao import Hrpws_DAO
from restclients.exceptions import DataFailureException
from restclients.util.timer import Timer
from restclients.util.log import log_info, log_err


logger = logging.getLogger(__name__)


def get_resource(url):
    timer = Timer()
    response = Hrpws_DAO().getURL(url, {'Accept': 'application/json'})
    log_data = "%s ==status==> %s" % (url, response.status)

    if response.status != 200:
        log_err(logger, log_data, timer)
        raise DataFailureException(url, response.status, response.data)

    log_info(logger, log_data, timer)
    logger.debug("%s ==data==> %s" % (url, response.data))
    return response.data
