"""
Interfacing with the Student Web Service, Registration_Search query.
"""
import logging
import json
import re
from urllib import urlencode
from decimal import *
from datetime import datetime
from restclients.models.sws import Registration, ClassSchedule
from restclients.exceptions import DataFailureException
from restclients.cache_manager import enable_cache_entry_queueing
from restclients.cache_manager import disable_cache_entry_queueing
from restclients.cache_manager import save_all_queued_entries
from restclients.pws import PWS
from restclients.thread import Thread
from restclients.sws import get_resource, SWSThread, deprecation, parse_sws_date
from restclients.sws.v5.section import _json_to_section


registration_res_url_prefix = "/student/v5/registration.json"
reg_credits_url_prefix = "/student/v5/registration/"
logger = logging.getLogger(__name__)


class SWSPersonByRegIDThread(Thread):
    regid = None
    person = None

    def run(self):
        if self.regid is None:
            raise Exception("SWSPersonByRegIDThread must have a regid")

        self.person = PWS().get_person_by_regid(self.regid)


def _registrations_for_section_with_active_flag(section, is_active,
                                                transcriptable_course=""):
    """
    Returns a list of all restclients.models.sws.Registration objects
    for a section. There can be duplicates for a person.
    If is_active is True, the objects will have is_active set to True.
    Otherwise, is_active is undefined, and out of scope for this method.
    """
    instructor_reg_id = ''
    if (section.is_independent_study and
            section.independent_study_instructor_regid is not None):
        instructor_reg_id = section.independent_study_instructor_regid

    activity_flag = ""
    if is_active:
        activity_flag = "true"

    params = {
        "year": section.term.year,
        "quarter": section.term.quarter,
        "curriculum_abbreviation": section.curriculum_abbr,
        "course_number": section.course_number,
        "section_id": section.section_id,
        "instructor_reg_id": instructor_reg_id,
        "is_active": activity_flag
    }

    if transcriptable_course != "":
        params["transcriptable_course"] = transcriptable_course

    url = "%s?%s" % (registration_res_url_prefix, urlencode(params))

    return _json_to_registrations(get_resource(url), section, is_active)


def _json_to_registrations(data, section, is_active):
    """
    Returns a list of all restclients.models.sws.Registration objects
    """
    seen_registrations = {}
    registrations = []

    # Keeping is_active on the registration resource undefined
    # unless is_active is true - the response with all registrations
    # doesn't tell us if it's active or not.
    # use get_all_registrations_for_section if you need to know that.
    is_active_flag = None
    if is_active:
        is_active_flag = True

    person_threads = []
    for reg_data in data.get("Registrations", []):
        if reg_data["RegID"] not in seen_registrations:
            registration = Registration()
            registration.section = section

            thread = SWSPersonByRegIDThread()
            thread.regid = reg_data["RegID"]
            thread.start()
            person_threads.append(thread)
            registration.is_active = is_active_flag
            registrations.append(registration)

            seen_registrations[reg_data["RegID"]] = True

    for i in range(len(person_threads)):
        thread = person_threads[i]
        thread.join()
        registration = registrations[i]

        registration.person = thread.person

    return registrations


def get_active_registrations_by_section(section, transcriptable_course=""):
    """
    Returns a list of restclients.Registration objects, representing
    active registrations for the passed section. For independent study
    sections, section.independent_study_instructor_regid limits
    registrations to that instructor.
    """
    return _registrations_for_section_with_active_flag(section, True,
                                                       transcriptable_course)


def get_all_registrations_by_section(section, transcriptable_course=""):
    """
    Returns a list of restclients.models.sws.Registration objects,
    representing all (active and inactive) registrations
    for the passed section.
    For independent study sections,
    section.independent_study_instructor_regid
    limits registrations to that instructor.
    """
    registrations = get_active_registrations_by_section(section)

    seen_registrations = {}
    for registration in registrations:
        seen_registrations[registration.person.uwregid] = True

    all_registrations = _registrations_for_section_with_active_flag(
        section, False, transcriptable_course)

    for registration in all_registrations:
        regid = registration.person.uwregid
        if regid not in seen_registrations:
            # This is just being set by induction.  The all registrations
            # resource can't know if a registration is active.
            registration.is_active = False
            seen_registrations[regid] = True
            registrations.append(registration)

    return registrations


# This function won't work when the dup_code is not empty
def get_credits_by_section_and_regid(section, regid):
    """
    Returns a restclients.models.sws.Registration object
    for the section and regid passed in.
    """
    deprecation("Use get_credits_by_reg_url")
    # note trailing comma in URL, it's required for the optional dup_code param
    url = "%s%s,%s,%s,%s,%s,%s,.json" % (
        reg_credits_url_prefix,
        section.term.year,
        section.term.quarter,
        re.sub(' ', '%20', section.curriculum_abbr),
        section.course_number,
        section.section_id,
        regid
    )

    reg_data = get_resource(url)

    try:
        return Decimal(reg_data['Credits'].strip())
    except InvalidOperation:
        pass


def get_credits_by_reg_url(url):
    """
    Returns a decimal value of the course credits
    """
    reg_data = get_resource(url)

    try:
        return Decimal(reg_data['Credits'].strip())
    except InvalidOperation:
        pass


def get_schedule_by_regid_and_term(regid, term,
                                   include_instructor_not_on_time_schedule=True):
    """
    Returns a restclients.models.sws.ClassSchedule object
    for the regid and term passed in.
    """
    url = "%s?%s" % (
        registration_res_url_prefix,
        urlencode([('reg_id', regid),
                   ('quarter', term.quarter),
                   ('is_active', 'true'),
                   ('year', term.year)
                   ]))

    return _json_to_schedule(get_resource(url), term, regid,
                             include_instructor_not_on_time_schedule)


def _json_to_schedule(term_data, term, regid,
                      include_instructor_not_on_time_schedule=True):
    sections = []
    sws_threads = []
    term_credit_hours = Decimal("0.0")

    enable_cache_entry_queueing()
    try:
        for registration in term_data["Registrations"]:
            reg_url = registration["Href"]

            # Skip a step here, and go right to the course section resource
            course_url = re.sub('registration', 'course', reg_url)
            course_url = re.sub('^(.*?,.*?,.*?,.*?,.*?),.*', '\\1.json', course_url)
            course_url = re.sub(',([^,]*).json', '/\\1.json', course_url)

            thread = SWSThread()
            thread.url = course_url
            thread.reg_url = reg_url
            thread.headers = {"Accept": "application/json"}
            thread.start()
            sws_threads.append(thread)

        for thread in sws_threads:
            thread.join()

        for thread in sws_threads:
            response = thread.response
            if not response:
                raise DataFailureException(thread.url,
                                           500,
                                           thread.exception)
            if response.status != 200:
                raise DataFailureException(thread.url,
                                           response.status,
                                           response.data)

            section = _json_to_section(json.loads(response.data), term,
                                       include_instructor_not_on_time_schedule)
            _add_credits_grade_to_section(thread.reg_url, section)
            if section.student_credits is not None:
                term_credit_hours += section.student_credits
            # For independent study courses, only include the one relevant
            # instructor
            if registration["Instructor"]:
                actual_instructor = None
                instructor_regid = registration["Instructor"]["RegID"]

                for instructor in section.meetings[0].instructors:
                    if instructor.uwregid == instructor_regid:
                        actual_instructor = instructor

                if actual_instructor:
                    section.meetings[0].instructors = [actual_instructor]
                else:
                    section.meetings[0].instructors = []
                section.independent_study_instructor_regid = registration["Instructor"]
            sections.append(section)

        term.credits = term_credit_hours
        term.section_count = len(sections)
        schedule = ClassSchedule()
        schedule.sections = sections
        schedule.term = term

        save_all_queued_entries()
        disable_cache_entry_queueing()
    except Exception as ex:
        save_all_queued_entries()
        disable_cache_entry_queueing()
        raise ex
    return schedule


def _add_credits_grade_to_section(url, section):
    """
    Given the registration url passed in,
    add credits, grade, grade date in the section object
    """
    section_reg_data = get_resource(url)
    if section_reg_data is not None:
        section.student_grade = section_reg_data['Grade']
        section.is_auditor = section_reg_data['Auditor']
        if len(section_reg_data['GradeDate']) > 0:
            section.grade_date = parse_sws_date(section_reg_data['GradeDate']).date()
        try:
            section.student_credits = Decimal(section_reg_data['Credits'].strip())
        except InvalidOperation:
            pass
