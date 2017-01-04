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


def is_class_list_available(course_section):
    """
    Return True if the corresponding mailman list is avaliable
    for the given Section object
    """
    # print "%s" % course_section.json_data()
    # print "%s" % course_section.term.json_data()

    if course_section.is_campus_bothell():
        curriculum = re.sub(r'^B ', 'b', course_section.curriculum_abbr)
    elif course_section.is_campus_tacoma():
        curriculum = re.sub(r'^T ', 't', course_section.curriculum_abbr)
    else:
        curriculum = course_section.curriculum_abbr

    list_name = "%s%s%s_%s%s" % (
        curriculum.lower(),
        course_section.course_number,
        course_section.section_id.lower(),
        course_section.term.quarter.lower()[:2],
        str(course_section.term.year)[-2:]
        )
    print list_name
    return _process_json(get_resource(URL % list_name))


def is_list_available(list_name):
    """
    Return True if the corresponding mailman list is avaliable
    for the given list name
    """
    return _process_json(get_resource(URL % list_name))


def _process_json(response_body):
    """
    Returns a UwPassword objects
    """
    data = json.loads(response_body)
    return "Available" in data and data["Available"] == "True"
