"""
This is the interface for interacting with the HRP Web Service.
"""

from datetime import datetime
import logging
import simplejson as json
from restclients.exceptions import InvalidRegID, InvalidNetID,\
    InvalidEmployeeID
from restclients.pws import PWS
from restclients.models.hrp import Appointment, Appointee
from restclients.hrpws import get_resource


URL_PREFIX = "/hrp/v1/appointee/"
logger = logging.getLogger(__name__)


def get_appointee_by_eid(employee_id):
    if not PWS().valid_employee_id(employee_id):
        raise InvalidEmployeeID(employee_id)
    return _get_appointee(employee_id)


def get_appointee_by_netid(netid):
    if not PWS().valid_uwnetid(netid):
        raise InvalidNetID(netid)
    return _get_appointee(netid)


def get_appointee_by_regid(regid):
    if not PWS().valid_uwregid(regid):
        raise InvalidRegID(regid)
    return _get_appointee(regid)


def _get_appointee(id):
    """
    Return a restclients.models.hrp.AppointeePerson object
    """
    url = "%s%s.json" % (URL_PREFIX, id)
    response = get_resource(url)
    return process_json(response)


def process_json(response_body):
    json_data = json.loads(response_body)
    person_data = json_data.get("Person")
    if not person_data:
        return None

    appointee = create_appointee(person_data)

    if json_data.get("Appointments"):
        apps = []
        for app in json_data.get("Appointments"):
            apps.append(create_appointment(app))
        appointee.appointments = apps
    return appointee


def create_appointee(person):
    ap = Appointee()
    ap.netid = person.get("UWNetID")
    ap.regid = person.get("UWRegID")
    ap.employee_id = person.get("EmployeeID")
    ap.status = person.get("EmploymentStatus")
    ap.status_desc = person.get("EmploymentStatusDescription")
    ap.home_dept_budget_number = person.get("HomeDepartmentBudgetNumber")
    ap.home_dept_budget_name = person.get("HomeDepartmentBudgetName")
    ap.home_dept_org_code = person.get("HomeDepartmentOrganizationCode")
    ap.home_dept_org_name = person.get("HomeDepartmentOrganizationName")
    ap.onoff_campus_code = person.get("OnOffCampusCode")
    ap.onoff_campus_code_desc = person.get("OnOffCampusCodeDescription")
    return ap


def create_appointment(appointment):
    app = Appointment()
    app.app_number = int(appointment.get("AppointmentNumber"))
    app.app_state = appointment.get("AppointmentState")
    app.dept_budget_name = appointment.get("DepartmentBudgetName")
    app.dept_budget_number = appointment.get("DepartmentBudgetNumber")
    app.job_class_code = appointment.get("JobClassCode")
    app.job_class_title = appointment.get("JobClassTitle")
    app.org_code = appointment.get("OrganizationCode")
    app.org_name = appointment.get("OrganizationName")
    app.paid_app_code = appointment.get("PaidAppointmentCode")
    app.status = appointment.get("Status")
    app.status_desc = appointment.get("StatusDescription")
    return app
