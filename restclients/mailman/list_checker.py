"""
Interface for interacting with the mailman uwnetid resource
"""

import json
import logging
import re
from django.conf import settings
from restclients.mailman import get_resource


logger = logging.getLogger(__name__)
URL = "/%s/admin/v1.0/uwnetid/available/?uwnetid=%s"


def _get_url_path(list_name):
    """
    Live Dao requires RESTCLIENTS_MAILMAN_KEY in the settings.py
    """
    access_key = getattr(settings,
                         "RESTCLIENTS_MAILMAN_KEY",
                         "__mock_key__")
    return URL % (access_key, list_name)


def exists(list_name):
    """
    Return True if the corresponding mailman list is avaliable
    for the given list name string
    @param list_name: a non_empty string
    """
    return _process_json(get_resource(_get_url_path(list_name)))


def get_instructor_term_list_name(instructor_entid, year, quarter):
    """
    Return the list address of UW instructor email list for
    the given year and quarter
    """
    return "%s_%s%s" % (
        instructor_entid,
        quarter.lower()[:2],
        str(year)[-2:])


def exists_instructor_term_combined_list(instructor_entid, year, quarter):
    """
    Return True if a combined mailman list exists for all courses
    taught by the UW instructor in the given term
    """
    return exists(get_instructor_term_list_name(instructor_entid,
                                                year, quarter))


def _get_list_name_curr_abbr(curriculum_abbr):
    """
    @return mailman specific curriculum abbr
    """
    curr_abbr = curriculum_abbr.lower()
    if re.match(r'^b [&\w]+', curr_abbr):
        return re.sub(r'^b ', 'b', curr_abbr)
    elif re.match(r'^t [&\w]+', curr_abbr):
        return re.sub(r'^t ', 't', curr_abbr)
    else:
        return curr_abbr


def get_course_list_name(curriculum_abbr, course_number, section_id,
                         quarter, year):
    """
    Return the list address of UW course email list
    """
    return "%s%s%s_%s%s" % (
        _get_list_name_curr_abbr(curriculum_abbr),
        course_number,
        section_id.lower(),
        quarter.lower()[:2],
        str(year)[-2:]
        )


def exists_course_list(curriculum_abbr, course_number, section_id,
                       quarter, year):
    """
    Return True if the corresponding mailman list exists for the course
    """
    return exists(get_course_list_name(curriculum_abbr, course_number,
                                       section_id, quarter, year))


def get_section_list_name(section):
    """
    Return the list address of UW course section email list
    """
    return get_course_list_name(section.curriculum_abbr,
                                section.course_number,
                                section.section_id,
                                section.term.quarter,
                                section.term.year)


def exists_section_list(course_section):
    """
    Return True if the corresponding mailman list exists
    for the course section
    @param course_section a valid Section object
    """
    return exists(get_section_list_name(course_section))


def get_secondary_section_combined_list_name(section):
    if section.is_primary_section:
        section_id = section.section_id
    else:
        section_id = section.primary_section_id

    return "multi_%s%s%s_%s%s" % (
        _get_list_name_curr_abbr(section.curriculum_abbr),
        section.course_number,
        section_id.lower(),
        section.term.quarter.lower()[:2],
        str(section.term.year)[-2:]
        )


def exists_secondary_section_combined_list(course_section):
    """
    Return True if a combined mailman list exists
    for all the secondary course sections
    """
    return exists(get_secondary_section_combined_list_name(course_section))


def _process_json(response_body):
    """
    Returns True the list already exists
    """
    data = json.loads(response_body)
    return "Available" in data and data["Available"] == "False"
