"""
This is the low level interface for interacting
with the UW Libraries Subject Guide Web Service.
"""

import json
import logging
from restclients.dao import DigitLib_DAO
from restclients.exceptions import DataFailureException
from restclients.util.timer import Timer
from restclients.util.log import log_info


logger = logging.getLogger(__name__)


def get_resource(url):
    timer = Timer()
    dao = DigitLib_DAO()
    response = dao.getURL(url, {})

    log_info(logger,
             "%s ==status==> %s" % (url, response.status),
             timer)

    if response.status == 302:
        return response.headers

    if response.status == 200 and response.data is not None:
        logger.debug("%s ==data==> %s" % (url, response.data))
        return json.loads(response.data)
