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


def get_instructor_term_list_name(instructor_entid, term):
    return "%s_%s%s" % (
        instructor_entid,
        term.quarter.lower()[:2],
        str(term.year)[-2:])


def exists_instructor_term_combined_list(instructor_entid, term):
    """
    Return True if a combined mailman list exists
    for the multilpe courses taught by the given instructor
    in the course year and quarter
    """
    return exists(
        get_instructor_term_list_name(instructor_entid, term))


def _get_list_name_curr_abbr(section):
    """
    @return mailman specific curriculum abbr
    """
    cur_abbr = section.curriculum_abbr.lower()
    if re.match(r'^b [&\w]+', cur_abbr):
        return re.sub(r'^b ', 'b', cur_abbr)
    elif re.match(r'^t [&\w]+', cur_abbr):
        return re.sub(r'^t ', 't', cur_abbr)
    else:
        return cur_abbr


def get_section_list_name(section):
    return "%s%s%s_%s%s" % (
        _get_list_name_curr_abbr(section),
        section.course_number,
        section.section_id.lower(),
        section.term.quarter.lower()[:2],
        str(section.term.year)[-2:]
        )


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
        _get_list_name_curr_abbr(section),
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
