"""
This is the interface for interacting with the UW Libraries Web Service.
"""

import logging
from datetime import datetime
from restclients.dao import Grad_DAO
from restclients.exceptions import DataFailureException


logger = logging.getLogger(__name__)


def get_resource(url):
    dao = Grad_DAO()
    response = dao.getURL(url, {})
    logger.info("%s ==status==> %s" % (url, response.status))

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    logger.debug("%s ==data==> %s" % (url, response.data))
    return response.data


def datetime_from_string(date_string):
    if date_string is None:
        return None
    date_format = "%Y-%m-%dT%H:%M:%S"
    if len(date_string) > 20:
        date_string = date_string[0:19]
    return datetime.strptime(date_string, date_format)
