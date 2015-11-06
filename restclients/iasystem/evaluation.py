"""
Interfacing with the IASytem API, Evaluation resource.
"""
import pytz
import logging
from urllib import urlencode
from restclients.iasystem import get_resource_by_campus
from restclients.models.iasystem import Evaluation
from datetime import datetime


IAS_PREFIX = "/api/v1/evaluation"


def search_evaluations(campus, **kwargs):
    """
    year (required)
    term_name (required): Winter|Spring|Summer|Autumn
    curriculum_abbreviation
    course_number
    section_id
    student_id (student number)
    """
    url = "%s?%s" % (IAS_PREFIX, urlencode(kwargs))

    data = get_resource_by_campus(url, campus)
    evaluations = _json_to_evaluation(data)

    return evaluations


def get_evaluation_by_id(evaluation_id, campus):
    url = "%s/%s" % (IAS_PREFIX, evaluation_id)
    return _json_to_evaluation(get_resource_by_campus(url, campus))


def _json_to_evaluation(data):
    """
    Only keep the data for online evaluations.
    Two scenarios for multiple instructors:
    1) all of the co-instructors may be evaluated online as a group,
       sharing the eval URL.
    2) each co-instructor may be evaluated individually,
       with separate eval URLs.
    """
    collection_items = data.get('collection').get('items')
    if collection_items is None:
        return None
    evaluations = []
    for item in collection_items:
        item_meta = item.get('meta')
        type = _get_item_type(item_meta)
        if type == "evaluation":
            delivery_data = item.get('data')
            if get_is_online(delivery_data):
                evaluation = Evaluation()
                evaluation.eval_status = \
                    get_value_by_name(delivery_data, 'status')
                evaluation.eval_open_date = get_open_date(delivery_data)
                evaluation.eval_close_date = get_close_date(delivery_data)
                evaluation.eval_url = get_eval_url(item.get('links'))
                section, instructors, completion =\
                    _get_child_items(_get_child_ids(item_meta),
                                     collection_items)
                evaluation.section_sln = get_section_sln(section)
                evaluation.instructor_ids = instructors
                evaluation.is_completed = get_is_complete(completion)
                evaluations.append(evaluation)
    return evaluations


def get_section_sln(section):
    sln = get_value_by_name(section.get('data'), 'instCourseId')
    return int(sln)


def get_is_complete(completion):
    if completion is None:
        return None
    return get_value_by_name(completion.get('data'), 'isCompleted')


def get_instructor_id(instructor):
    id = get_value_by_name(instructor.get('data'), 'instInstructorId')
    return int(id)


def _get_child_items(child_ids, collection_items):
    section = None
    instructors = []  # array of intergers
    completion = None
    for item in collection_items:
        id = get_value_by_name(item.get('meta'), 'id')
        if id in child_ids:
            type = get_value_by_name(item.get('meta'), 'type')
            if type == "instructor":
                instructors.append(get_instructor_id(item))
            if type == "section":
                section = item
            if type == "evaluation completion":
                completion = item
    return section, instructors, completion


def _get_child_ids(meta_data):
    child_ids = []
    for item in meta_data:
        if item.get('name') == "childId":
            child_ids.append(item.get('value'))
    return child_ids


def get_eval_url(data):
    for item in data:
        if item.get('rel') == "publishedto":
            return item.get('href')


def get_value_by_name(list, name):
    for item in list:
        if item.get('name') == name:
            return item.get('value')


def _get_item_type(meta):
    for item in meta:
        if item.get('name') == 'type':
            return item.get('value')


def get_open_date(data):
    open_date = get_value_by_name(data, 'openDate')
    return _datetime_from_string(open_date)


def get_close_date(data):
    open_date = get_value_by_name(data, 'closeDate')
    return _datetime_from_string(open_date)


def get_is_online(data):
    if get_value_by_name(data, 'deliveryMethod') == "Online":
        return True
    return False


def _datetime_from_string(date_string):
    date_format = "%Y-%m-%dT%H:%M:%S"
    date_string = date_string.replace("Z", "")
    date = datetime.strptime(date_string, date_format)
    return pytz.utc.localize(date)
