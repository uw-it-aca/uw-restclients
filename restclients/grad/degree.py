"""
Interfacing with the Grad Scho Degree Request API
"""
import logging
import json
from restclients.models.grad import GradDegree
from restclients.pws import PWS
from restclients.grad import get_resource, datetime_from_string


PREFIX = "/services/students/v1/api/request?id="
SUFFIX = "&exclude_past_quarter=true"


logger = logging.getLogger(__name__)


def get_degree_by_regid(regid):
    """
    raise: InvalidRegID, DataFailureException
    """
    person = PWS().get_person_by_regid(regid)
    return get_degree_by_syskey(person.student_system_key)


def get_degree_by_syskey(system_key):
    if system_key is None:
        logger.info("get_degree_by_syskey abort, key is None!")
        return None
    url = "%s%s%s" % (PREFIX, system_key, SUFFIX)
    return _process_json(json.loads(get_resource(url)))


def _process_json(json_data):
    """
    return a list of GradDegree objects.
    """
    requests = []
    for item in json_data:
        degree = GradDegree()
        degree.degree_title = item["degreeTitle"]
        degree.exam_place = item["examPlace"]
        degree.exam_date = datetime_from_string(item["examDate"])
        degree.req_type = item["requestType"]
        degree.major_full_name = item["majorFullName"]
        degree.submit_date = datetime_from_string(item["requestSubmitDate"])
        if 'decisionDate' in item and item.get('decisionDate') is not None:
            degree.decision_date = datetime_from_string(
                item.get('decisionDate'))
        degree.status = item["status"]
        degree.target_award_year = item["targetAwardYear"]
        if item.get("targetAwardQuarter") is not None:
            degree.target_award_quarter = item["targetAwardQuarter"].lower()

        requests.append(degree)
    return requests
