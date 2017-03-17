"""
This is the interface for interacting with the UPass service.

"""

from restclients.dao import UPass_DAO
from restclients.exceptions import DataFailureException
from restclients.models.upass import UPassStatus, CURRENT, NOT_CURRENT


def get_upass_status(netid):
    dao = UPass_DAO()
    url = get_upass_url(netid)
    response = dao.getURL(url, {})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    if len(response.data) == 0 or\
            not(CURRENT in response.data or NOT_CURRENT in response.data):
        raise Exception("%s Unexpected Response Data: %s" %
                        (url, response.data))

    status = UPassStatus.create(response.data)
    return status


def get_upass_url(netid):
    return ("/MyUWUpass/MyUWUpass.aspx?id=%s" % netid)
