"""
Interfacing with the IASytem API, Evaluation resource.
"""
from urllib import urlencode
from restclients.iasystem import get_resource
#from restclients.models.iasystem import Evaluation


def search_evaluations(**kwargs):
    """
    year (required)
    term_name (required): Winter|Spring|Summer|Autumn
    curriculum_abbreviation
    course_number
    section_id
    student_id (student number)
    """
    url = "/api/v1/evaluation?%s" % urlencode(kwargs)

    data = get_resource(url)

    evaluations = []
    for eval_data in data.get("items", []):
        evaluation = _json_to_evaluation(eval_data)
        evaluations.append(evaluation)

    return evaluations


def get_evaluation_by_id(evaluation_id):
    url = "/api/v1/evaluation/%s" % evaluation_id
    return _json_to_evaluation(get_resource(url))


def _json_to_evaluation(data):
    # TODO: make a model
    return data
