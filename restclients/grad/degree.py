"""
Interfacing with the Grad Scho Degree Request API
"""
import logging
import json
from restclients.models.grad import GradDegree
from restclients.sws.person import get_person_by_regid
from restclients.grad import get_resource, datetime_from_string


PREFIX = "/services/students/v1/api/request?id="
SUFFIX = "&exclude_past_quarter=yes"


def get_degree_by_regid(regid):
    sws_person = get_person_by_regid(regid)
    if sws_person is None:
        return None
    return get_degree_by_syskey(sws_person.student_system_key)


def get_degree_by_syskey(system_key):
    url = "%s%s%s" % (PREFIX, system_key, SUFFIX)
    return _process_json(json.loads(get_resource(url)))


def _process_json(json_data):
    """
    """
    requests = []
    for item in json_data:
        degree = GradDegree()
        degree.req_type = item["RequestType"]
        degree.submit_date = datetime_from_string(item["RequestSubmitDate"])
        degree.degree_title = item["DegreeTitle"]
        degree.status = item["status"]
        degree.exam_place = item["examPlace"]
        degree.exam_date = datetime_from_string(item["examDate"])
        degree.target_award_year = item["TargetAwardYear"]
        degree.target_award_quarter = item["TargetAwardQuarter"]

        requests.append(degree)
    return requests
