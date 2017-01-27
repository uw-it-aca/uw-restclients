"""
This is the interface for interacting with the UPass service.

"""

from restclients.dao import UPass_DAO
from restclients.exceptions import DataFailureException
from restclients.models.upass import UPassStatus


def get_upass_status(netid):
    dao = UPass_DAO()
    url = get_upass_url(netid)
    response = dao.getURL(url, {})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    status = UPassStatus.create(response.data)
    return status


def get_upass_url(netid):
    return "/upass/MyUWUpass.aspx?id=%s" % (netid)
