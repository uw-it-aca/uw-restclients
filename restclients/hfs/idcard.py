"""
This is the interface for interacting with the UW Libraries Web Service.
"""

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
        student_husky_card_account = StudentHuskyCardAccout()
        student_husky_card_account.balance = json_data['student_husky_card']['balance']
        student_husky_card_account.last_updated = json_data['student_husky_card']['last_updated']
        student_husky_card_account.add_funds_url = json_data['student_husky_card']['add_funds_url']
        return_obj.student_husky_card = student_husky_card_account

    if json_data.get('resident_dining') is not None:
        resident_dining_account = ResidentDiningAccount()
        resident_dining_account.balance = json_data['resident_dining']['balance']
        resident_dining_account.last_updated = json_data['resident_dining']['last_updated']
        resident_dining_account.add_funds_url = json_data['resident_dining']['add_funds_url']
        return_obj.resident_dining = resident_dining_account

    if json_data.get('employee_husky_card') is not None:
        employee_husky_card_account = EmployeeHuskyCardAccount()
        employee_husky_card_account.balance = json_data['employee_husky_card']['balance']
        employee_husky_card_account.last_updated = json_data['employee_husky_card']['last_updated']
        employee_husky_card_account.add_funds_url = json_data['employee_husky_card']['add_funds_url']
        return_obj.employee_husky_card = employee_husky_card_account

    return return_obj

