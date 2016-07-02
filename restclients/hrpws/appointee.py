"""
This is the interface for interacting with the HRP Web Service.
"""

from datetime import datetime
import logging
import simplejson as json
from restclients.models.hrp import AppointeePerson
from restclients.hrpws import get_resource


URL_PREFIX = "/hrp/v1/appointee/"
logger = logging.getLogger(__name__)


def get_appointee_by_eid(eid):
    return _get_appointee(eid)


def get_appointee_by_netid(netid):
    return _get_appointee(netid)


def get_appointee_by_regid(regid):
    return _get_appointee(regid)


def _get_appointee(id):
    """
    Return a restclients.models.hrp.AppointeePerson object
    """
    url = "%s%s.json" % (URL_PREFIX, id)
    response = get_resource(url)
    return person_from_json(response)


def person_from_json(response_body):
    json_data = json.loads(response_body)
    person = json_data.get("Person")
    if not person:
        return None
    ap = AppointeePerson()
    ap.regid = person.get("UWRegID")
    ap.eid = person.get("EmployeeID")
    ap.status = person.get("EmploymentStatus")
    ap.status_desc = person.get("EmploymentStatusDescription")
    ap.home_dept_budget_number = person.get("HomeDepartmentBudgetNumber")
    ap.home_dept_budget_name = person.get("HomeDepartmentBudgetName")
    ap.home_dept_org_code = person.get("HomeDepartmentOrganizationCode")
    ap.home_dept_org_name = person.get("HomeDepartmentOrganizationName")
    ap.campus_code = person.get("OnOffCampusCode")
    ap.campus_code_desc = person.get("OnOffCampusCodeDescription")

    return ap
