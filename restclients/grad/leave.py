"""
Interfacing with the GradScho Degree Request API
"""
import logging
import json
from restclients.models.grad import GradLeave, GradTerm
from restclients.sws.person import get_person_by_regid
from restclients.grad import get_resource, datetime_from_string


PREFIX = "/services/students/v1/api/leave?id="


def get_leave_by_regid(regid):
    sws_person = get_person_by_regid(regid)
    if sws_person is None:
        return None
    return get_leave_by_syskey(sws_person.student_system_key)


def get_leave_by_syskey(system_key):
    url = "%s%s" % (PREFIX, system_key)
    return _process_json(json.loads(get_resource(url)))


def _process_json(data):
    """
    """
    requests = []
    for item in data:
        leave = GradLeave()
        leave.reason = item.get('leaveReason')
        leave.submit_date = datetime_from_string(item.get('submitDate'))
        leave.status = item.get('status')

        for quarter in item.get('quarters'):
            term = GradTerm()
            term.quarter = quarter.get('quarter')
            term.year = quarter.get('year')
            leave.terms.append(term)
        requests.append(leave)
    return requests
