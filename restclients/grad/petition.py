"""
Interfacing with the Grad Scho Petition Request API
"""
import logging
import json
from restclients.models.grad import GradPetition
from restclients.sws.person import get_person_by_regid
from restclients.grad import get_resource, datetime_from_string


PREFIX = "/services/students/v1/api/petition?id="


def get_petition_by_regid(regid):
    sws_person = get_person_by_regid(regid)
    if sws_person is None:
        return None
    return get_petition_by_syskey(sws_person.student_system_key)


def get_petition_by_syskey(system_key):
    url = "%s%s" % (PREFIX, system_key)
    return _process_json(json.loads(get_resource(url)))


def _process_json(data):
    """
    """
    requests = []
    for item in data:
        petition = GradPetition()
        petition.description = item.get('description')
        petition.submit_date = datetime_from_string(item.get('submitDate'))
        petition.dept_recommend = item.get('deptRecommend')
        petition.gradschool_decision = item.get('gradSchoolDecision')
        requests.append(petition)
    return requests
