"""
Interface for interacting with the mailman uwnetid resource
"""

from datetime import datetime
import json
import logging
import re
from restclients.mailman import get_resource


logger = logging.getLogger(__name__)
URL = "/tkVouryGMUBY4j9uLVfqKtJkgZZT/admin/v1.0/uwnetid/available/?uwnetid=%s"


def exists(list_name):
    """
    Return True if the corresponding mailman list is avaliable
    for the given list name string
    @param list_name: a non_empty string
    """
    return _process_json(get_resource(URL % list_name))


def exists_instructor_term_combined_list(instructor_entid, term):
    """
    Return True if a combined mailman list exists
    for the multilpe courses taught by the given instructor
    in the course year and quarter
    """
    list_name = "%s_%s%s" % (
        instructor_entid,
        term.quarter.lower()[:2],
        str(term.year)[-2:])
    return exists(list_name)


def _get_curriculum_abbr(course_section):
    """
    @return mailman specific curriculum abbr
    """
    if course_section.is_campus_bothell():
        return re.sub(r'^b ', 'b', course_section.curriculum_abbr.lower())
    elif course_section.is_campus_tacoma():
        return re.sub(r'^t ', 't', course_section.curriculum_abbr.lower())
    else:
        return course_section.curriculum_abbr.lower()


def exists_section_list(course_section):
    """
    Return True if the corresponding mailman list exists
    for the course section
    @param course_section a valid Section object
    """
    list_name = "%s%s%s_%s%s" % (
        _get_curriculum_abbr(course_section),
        course_section.course_number,
        course_section.section_id.lower(),
        course_section.term.quarter.lower()[:2],
        str(course_section.term.year)[-2:]
        )
    return exists(list_name)


def exists_secondary_section_combined_list(course_section):
    """
    Return True if a combined mailman list exists
    for all the secondary course sections
    """
    list_name = "multi_%s%sa_%s%s" % (
        _get_curriculum_abbr(course_section),
        course_section.course_number,
        course_section.term.quarter.lower()[:2],
        str(course_section.term.year)[-2:]
        )
    return exists(list_name)


def _process_json(response_body):
    """
    Returns True the list already exists
    """
    data = json.loads(response_body)
    return "Available" in data and data["Available"] == "False"
