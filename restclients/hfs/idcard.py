"""
This is the interface for interacting with the UW Libraries Web Service.
"""

from datetime import datetime
import logging
import json
from restclients.models.hfs import StudentHuskyCardAccout, EmployeeHuskyCardAccount
from restclients.models.hfs import ResidentDiningAccount, HfsAccouts
from restclients.hfs import get_resource


url_prefix = "/v1/hfs/" 
logger = logging.getLogger(__name__)


def get_hfs_accounts(netid):
    """
    Return a restclients.models.hfs.HfsAccoutsThe object on the given uwnetid
    """
    url = "%s%s" % (url_prefix, netid)
    response = get_resource(url)
    return _object_from_json(response)


def _object_from_json(response_body):
    return_obj = HfsAccouts()
    json_data = json.loads(response_body)

    if json_data.get('student_husky_card') is not None:
        return_obj.student_husky_card = _load_acc_obj(
            json_data['student_husky_card'],
            StudentHuskyCardAccout())

    if json_data.get('resident_dining') is not None:
        return_obj.resident_dining = _load_acc_obj(
            json_data['resident_dining'],
            ResidentDiningAccount())

    if json_data.get('employee_husky_card') is not None:
        return_obj.employee_husky_card = _load_acc_obj(
            json_data['employee_husky_card'],
            EmployeeHuskyCardAccount())

    return return_obj


def _load_acc_obj(account_data, account_obj):
    account_obj.balance = account_data['balance']
    account_obj.last_updated = get_last_updated(account_data['last_updated'])
    account_obj.add_funds_url = account_data['add_funds_url']
    return account_obj


def get_last_updated(data):
    return datetime.strptime(data[0:19], "%Y-%m-%dT%H:%M:%S")
