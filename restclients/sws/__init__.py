"""
This is the interface for interacting with the Student Web Service.
"""
import logging
import json
import warnings
from urllib import quote
from datetime import datetime
from restclients.thread import Thread
from restclients.dao import SWS_DAO
from restclients.exceptions import DataFailureException
from django.conf import settings


QUARTER_SEQ = ["winter", "spring", "summer", "autumn"]
logger = logging.getLogger(__name__)


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def encode_section_label(label):
    return quote(label, safe="/,")


def get_resource(url):
    """
    Issue a GET request to SWS with the given url
    and return a response in json format.
    :returns: http response with content in json
    """
    response = SWS_DAO().getURL(url, {"Accept": "application/json"})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)
    return json.loads(response.data)


def get_current_sws_version():
    if getattr(settings, 'RESTCLIENTS_SWS_USE_V4', False):
        return 4
    return 5

def use_v5_resources():
    if get_current_sws_version() == 5:
        return True
    return False

class SWSThread(Thread):
    url = None # the course url to send a request
    reg_url = None
    headers = None
    response = None

    def run(self):
        if self.url is None:
            raise Exception("SWSThread must have a url")

        args = self.headers or {}

        self.response = SWS_DAO().getURL(self.url, args)


class SWS(object):
    """
    The SWS object has methods for getting information
    about courses, and everything related.
    """

    def get_term_by_year_and_quarter(self, year, quarter):
        deprecation("Use restclients.sws.term.get_term_by_year_and_quarter")
        from restclients.sws.term import get_term_by_year_and_quarter
        return get_term_by_year_and_quarter(year, quarter)

    def get_current_term(self):
        deprecation("Use restclients.sws.term.get_current_term")
        from restclients.sws.term import get_current_term
        return get_current_term()

    def get_next_term(self):
        deprecation("Use restclients.sws.term.get_next_term")
        from restclients.sws.term import get_next_term
        return get_next_term()

    def get_previous_term(self):
        deprecation("Use restclients.sws.term.get_previous_term")
        from restclients.sws.term import get_previous_term
        return get_previous_term()

    def get_term_before(self, aterm):
        deprecation("Use restclients.sws.term.get_term_before")
        from restclients.sws.term import get_term_before
        return get_term_before(aterm)

    def get_term_after(self, aterm):
        deprecation("Use restclients.sws.term.get_term_after")
        from restclients.sws.term import get_term_after
        return term.get_term_after(aterm)

    def get_sections_by_instructor_and_term(self, person, term):
        deprecation("Use restclients.sws.section.get_sections_by_instructor_and_term")
        from restclients.sws.section import get_sections_by_instructor_and_term
        return get_sections_by_instructor_and_term(person, term)

    def get_sections_by_delegate_and_term(self, person, term):
        deprecation("Use restclients.sws.section.get_sections_by_delegate_and_term")
        from restclients.sws.section import get_sections_by_delegate_and_term
        return get_sections_by_delegate_and_term(person, term)

    def get_sections_by_curriculum_and_term(self, curriculum, term):
        deprecation("Use restclients.sws.section.get_sections_by_curriculum_and_term")
        from restclients.sws.section import get_sections_by_curriculum_and_term
        return get_sections_by_curriculum_and_term(curriculum, term)

    def get_section_by_label(self, label,
                             include_instructor_not_on_time_schedule=True):
        deprecation("Use restclients.sws.section.get_section_by_label")
        from restclients.sws.section import get_section_by_label
        return get_section_by_label(label, include_instructor_not_on_time_schedule)

    def get_section_by_url(self, url,
                           include_instructor_not_on_time_schedule=True):
        deprecation("Use restclients.sws.section.get_section_by_url")
        from restclients.sws.section import get_section_by_url
        return get_section_by_url(url, include_instructor_not_on_time_schedule)

    def get_section_status_by_label(self, label):
        deprecation("Use restclients.sws.section.get_section_status_by_label")
        from restclients.sws.section_status import get_section_status_by_label
        return get_section_status_by_label(label)

    def get_linked_sections(self, asection,
                            include_instructor_not_on_time_schedule=True):
        deprecation("Use restclients.sws.section.get_linked_sections")
        from restclients.sws.section import get_linked_sections
        return get_linked_sections(asection, include_instructor_not_on_time_schedule)

    def get_joint_sections(self, asection,
                           include_instructor_not_on_time_schedule=True):
        deprecation("Use restclients.sws.section.get_joint_sections")
        from restclients.sws.section import get_joint_sections
        return get_joint_sections(asection, include_instructor_not_on_time_schedule)

    def get_all_registrations_for_section(self, section):
        deprecation(
            "Use restclients.sws.registration.get_all_registrations_by_section")
        from restclients.sws.registration import get_all_registrations_by_section
        return get_all_registrations_by_section(section)

    def get_active_registrations_for_section(self, section):
        deprecation(
            "Use restclients.sws.registration.get_active_registrations_by_section")
        from restclients.sws.registration import get_active_registrations_by_section
        return get_active_registrations_by_section(section)

    def schedule_for_regid_and_term(self, regid, term,
                                    include_instructor_not_on_time_schedule=True):
        deprecation(
            "Use restclients.sws.registration.get_schedule_by_regid_and_term")
        from restclients.sws.registration import get_schedule_by_regid_and_term
        return get_schedule_by_regid_and_term(regid, term,
                                              include_instructor_not_on_time_schedule)

    def grades_for_regid_and_term(self, regid, term):
        deprecation(
            "Use restclients.sws.enrollment.get_grades_by_regid_and_term")
        from restclients.sws.enrollment import get_grades_by_regid_and_term
        return get_grades_by_regid_and_term(regid, term)

    def get_all_campuses(self):
        deprecation(
            "Use restclients.sws.campus.get_all_campuses")
        from restclients.sws.campus import get_all_campuses
        return get_all_campuses()

    def get_all_colleges(self):
        deprecation(
            "Use restclients.sws.college.get_all_colleges")
        from restclients.sws.college import get_all_colleges
        return get_all_colleges()

    def get_departments_for_college(self, college):
        deprecation(
            "Use restclients.sws.department.get_departments_by_college")
        from restclients.sws.department import get_departments_by_college
        return get_departments_by_college(college)

    def get_curricula_for_department(self, department, future_terms=0):
        deprecation(
            "Use restclients.sws.curriculum.get_curricula_by_department")
        from restclients.sws.curriculum import get_curricula_by_department
        return get_curricula_by_department(department, future_terms)

    def get_curricula_for_term(self, term):
        deprecation(
            "Use restclients.sws.curriculum.get_curricula_by_term")
        from restclients.sws.curriculum import get_curricula_by_term
        return get_curricula_by_term(term)

