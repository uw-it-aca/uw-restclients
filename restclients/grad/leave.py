"""
Interfacing with the GradScho Degree Request API
"""
import logging
import json
from restclients.models.grad import GradLeave, GradTerm
from restclients.pws import PWS
from restclients.grad import get_resource, datetime_from_string


PREFIX = "/services/students/v1/api/leave?id="


logger = logging.getLogger(__name__)


def get_leave_by_regid(regid):
    """
    raise: InvalidRegID, DataFailureException
    """
    person = PWS().get_person_by_regid(regid)
    return get_leave_by_syskey(person.student_system_key)


def get_leave_by_syskey(system_key):
    url = "%s%s" % (PREFIX, system_key)
    return _process_json(json.loads(get_resource(url)))


def _process_json(data):
    """
    return a list of GradLeave objects.
    """
    requests = []
    for item in data:
        leave = GradLeave()
        leave.reason = item.get('leaveReason')
        leave.submit_date = datetime_from_string(item.get('submitDate'))
        if item.get('status') is not None and len(item.get('status')) > 0:
            leave.status = item.get('status').lower()

        for quarter in item.get('quarters'):
            term = GradTerm()
            term.quarter = quarter.get('quarter').lower()
            term.year = quarter.get('year')
            leave.terms.append(term)
        requests.append(leave)
    return requests
