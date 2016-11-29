"""
Interfacing with the Student Web Service, for Section and Course resources.
"""
import logging
import re
from datetime import datetime
from urllib import urlencode
from restclients.thread import generic_prefetch
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidSectionID, InvalidSectionURL
from restclients.models.sws import Section, SectionReference, FinalExam
from restclients.models.sws import SectionMeeting
from restclients.models.sws import GradeSubmissionDelegate
from restclients.models.sws import Person
from restclients.pws import PWS
from restclients.sws import get_resource, encode_section_label
from restclients.sws.term import get_term_by_year_and_quarter


course_url_pattern = re.compile(r'^\/student\/v5\/course\/')
course_res_url_prefix = "/student/v5/course"
section_res_url_prefix = "/student/v5/section.json"
section_label_pattern = re.compile(
    '^\d{4},'                           # year
    '(?:winter|spring|summer|autumn),'  # quarter
    '[\w& ]+,'                          # curriculum
    '\d{3}\/'                           # course number
    '[A-Z][A-Z0-9]?$',                  # section id
    re.VERBOSE
)
logger = logging.getLogger(__name__)


def get_sections_by_instructor_and_term(person, term):
    """
    Returns a list of restclients.models.sws.SectionReference objects
    for the passed instructor and term.
    """
    return _get_sections_by_person_and_term(
        person, term, course_role="Instructor")


def get_sections_by_delegate_and_term(person, term):
    """
    Returns a list of restclients.models.sws.SectionReference objects
    for the passed grade submission delegate and term.
    """
    return _get_sections_by_person_and_term(
        person, term, course_role="GradeSubmissionDelegate")


def get_sections_by_curriculum_and_term(curriculum, term):
    """
    Returns a list of restclients.models.sws.SectionReference objects
    for the passed curriculum and term.
    """
    url = "%s?%s" % (section_res_url_prefix,
                     urlencode({"year": term.year,
                                "quarter": term.quarter.lower(),
                                "curriculum_abbreviation": curriculum.label}))
    return _json_to_sectionref(get_resource(url), term)


def get_changed_sections_by_term(changed_since_date, term, **kwargs):
    kwargs.update({"year": term.year,
                   "quarter": term.quarter.lower(),
                   "changed_since_date": changed_since_date,
                   "page_size": 1000})
    url = "%s?%s" % (section_res_url_prefix, urlencode(kwargs))

    sections = []
    while url is not None:
        data = get_resource(url)
        sections.extend(_json_to_sectionref(data, term))

        url = None
        if data.get("Next") is not None:
            url = data.get("Next").get("Href", None)

    return sections


def _json_to_sectionref(data, aterm):
    """
    Returns a list of SectionReference object created from
    the passed json data.
    """
    sections = []
    for section_data in data.get("Sections", []):
        section = SectionReference(
            term=aterm,
            curriculum_abbr=section_data["CurriculumAbbreviation"],
            course_number=section_data["CourseNumber"],
            section_id=section_data["SectionID"],
            url=section_data["Href"])
        sections.append(section)
    return sections


def _get_sections_by_person_and_term(person, term, course_role,
                                     include_secondaries="on"):
    """
    Returns a list of restclients.models.sws.SectionReference object
    for the passed course_role and term (including secondaries).
    """
    url = "%s?%s" % (
        section_res_url_prefix,
        urlencode({"year": term.year,
                   "quarter": term.quarter.lower(),
                   "reg_id": person.uwregid,
                   "search_by": course_role,
                   "include_secondaries": include_secondaries
                   }))

    return _json_to_sectionref(get_resource(url), term)


def get_section_by_url(url,
                       include_instructor_not_on_time_schedule=True):
    """
    Returns a restclients.models.sws.Section object
    for the passed section url.
    """
    if not course_url_pattern.match(url):
        raise InvalidSectionURL(url)

    return _json_to_section(
        get_resource(url),
        include_instructor_not_on_time_schedule=(
            include_instructor_not_on_time_schedule))


def get_section_by_label(label,
                         include_instructor_not_on_time_schedule=True):
    """
    Returns a restclients.models.sws.Section object for
    the passed section label.
    """
    if not section_label_pattern.match(label):
        raise InvalidSectionID(label)

    url = "%s/%s.json" % (
        course_res_url_prefix,
        encode_section_label(label))

    return get_section_by_url(url,
                              include_instructor_not_on_time_schedule)


def get_linked_sections(section,
                        include_instructor_not_on_time_schedule=True):
    """
    Returns a list of restclients.models.sws.Section objects,
    representing linked sections for the passed section.
    """
    linked_sections = []

    for url in section.linked_section_urls:
        section = get_section_by_url(url,
                                     include_instructor_not_on_time_schedule)
        linked_sections.append(section)

    return linked_sections


def get_joint_sections(section,
                       include_instructor_not_on_time_schedule=True):
    """
    Returns a list of restclients.models.sws.Section objects,
    representing joint sections for the passed section.
    """
    joint_sections = []

    for url in section.joint_section_urls:
        section = get_section_by_url(url,
                                     include_instructor_not_on_time_schedule)
        joint_sections.append(section)

    return joint_sections


def get_prefetch_for_section_data(section_data):
    """
    This will return a list of methods that can be called to prefetch (in
    threads) content that would be fetched while building the section.

    This depends on a good cache backend.  Without that, this will just double
    the work that's needed :(

    Each method is identified by a key, so they can be deduped if multiple
    sections want the same data, such as a common instructor.
    """
    pws = PWS()
    prefetch = []
    for meeting_data in section_data["Meetings"]:
        for instructor_data in meeting_data["Instructors"]:
            pdata = instructor_data["Person"]
            if "RegID" in pdata and pdata["RegID"] is not None:
                prefetch.append(["person-%s" % pdata["RegID"],
                                 prefetch_method(pws.get_person_by_regid,
                                                 [pdata["RegID"]])])

    return prefetch

def _json_to_section(section_data,
                     term=None,
                     include_instructor_not_on_time_schedule=True):
    """
    Returns a section model created from the passed json.
    """
    pws = PWS()
    section = Section()

    if term is not None and (
            term.year == int(section_data["Course"]["Year"]) and
            term.quarter == section_data["Course"]["Quarter"]):
        section.term = term
    else:
        section.term = get_term_by_year_and_quarter(
            section_data["Course"]["Year"],
            section_data["Course"]["Quarter"])

    section.curriculum_abbr = section_data["Course"][
        "CurriculumAbbreviation"]
    section.course_number = section_data["Course"]["CourseNumber"]
    section.course_title = section_data["CourseTitle"]
    section.course_title_long = section_data["CourseTitleLong"]
    section.course_campus = section_data["CourseCampus"]
    section.section_id = section_data["SectionID"]
    section.institute_name = section_data.get("InstituteName", "")
    section.primary_lms = section_data.get("PrimaryLMS", None)
    section.lms_ownership = section_data.get("LMSOwnership", None)
    section.is_independent_start = section_data.get("IsIndependentStart",
                                                    False)

    date_format = "%Y-%m-%d"
    if section_data.get("StartDate", None):
        str_date = section_data["StartDate"]
        section.start_date = datetime.strptime(str_date, date_format).date()

    if section_data.get("EndDate", None):
        str_date = section_data["EndDate"]
        section.end_date = datetime.strptime(str_date, date_format).date()

    section.section_type = section_data["SectionType"]
    if "independent study" == section.section_type:
        section.is_independent_study = True
    else:
        section.is_independent_study = False

    section.class_website_url = section_data["ClassWebsiteUrl"]
    section.sln = section_data["SLN"]
    if "SummerTerm" in section_data:
        section.summer_term = section_data["SummerTerm"]
    else:
        section.summer_term = ""

    section.delete_flag = section_data["DeleteFlag"]
    if "withdrawn" == section.delete_flag:
        section.is_withdrawn = True
    else:
        section.is_withdrawn = False

    section.current_enrollment = int(section_data['CurrentEnrollment'])
    section.auditors = int(section_data['Auditors'])
    section.allows_secondary_grading = section_data["SecondaryGradingOption"]

    primary_section = section_data["PrimarySection"]
    if (primary_section is not None and
            primary_section["SectionID"] != section.section_id):
        section.is_primary_section = False
        section.primary_section_href = primary_section["Href"]
        section.primary_section_id = primary_section["SectionID"]
        section.primary_section_curriculum_abbr = primary_section[
            "CurriculumAbbreviation"]
        section.primary_section_course_number = primary_section[
            "CourseNumber"]
    else:
        section.is_primary_section = True

    section.linked_section_urls = []
    for linked_section_type in section_data["LinkedSectionTypes"]:
        for linked_section_data in linked_section_type["LinkedSections"]:
            url = linked_section_data["Section"]["Href"]
            section.linked_section_urls.append(url)

    section.joint_section_urls = []
    for joint_section_data in section_data.get("JointSections", []):
        url = joint_section_data["Href"]
        section.joint_section_urls.append(url)

    section.grade_submission_delegates = []
    for del_data in section_data["GradeSubmissionDelegates"]:
        delegate = GradeSubmissionDelegate(
            person=pws.get_person_by_regid(del_data["Person"]["RegID"]),
            delegate_level=del_data["DelegateLevel"])
        section.grade_submission_delegates.append(delegate)

    section.meetings = []
    for meeting_data in section_data["Meetings"]:
        meeting = SectionMeeting()
        meeting.section = section
        meeting.term = section.term
        meeting.meeting_index = meeting_data["MeetingIndex"]
        meeting.meeting_type = meeting_data["MeetingType"]

        meeting.building = meeting_data["Building"]
        if meeting_data["BuildingToBeArranged"]:
            meeting.building_to_be_arranged = True
        else:
            meeting.building_to_be_arranged = False

        meeting.room_number = meeting_data["RoomNumber"]
        if meeting_data["RoomToBeArranged"]:
            meeting.room_to_be_arranged = True
        else:
            meeting.room_to_be_arranged = False

        if meeting_data["DaysOfWeekToBeArranged"]:
            meeting.days_to_be_arranged = True
        else:
            meeting.days_to_be_arranged = False

        for day_data in meeting_data["DaysOfWeek"]["Days"]:
            attribute = "meets_%s" % day_data["Name"].lower()
            setattr(meeting, attribute, True)

        meeting.start_time = meeting_data["StartTime"]
        meeting.end_time = meeting_data["EndTime"]

        meeting.instructors = []
        for instructor_data in meeting_data["Instructors"]:
            # TSPrint: True
            # Instructor information currently listed on the Time Schedule
            if (instructor_data["TSPrint"] or
                    include_instructor_not_on_time_schedule):
                pdata = instructor_data["Person"]

                if "RegID" in pdata and pdata["RegID"] is not None:
                    try:
                        instructor = pws.get_person_by_regid(pdata["RegID"])
                    except:
                        instructor = Person(uwregid=pdata["RegID"],
                                            display_name=pdata["Name"])
                    instructor.TSPrint = instructor_data["TSPrint"]
                    meeting.instructors.append(instructor)

        section.meetings.append(meeting)

    section.final_exam = None
    if "FinalExam" in section_data and section_data["FinalExam"] is not None:
        if "MeetingStatus" in section_data["FinalExam"]:
            final_exam = FinalExam()
            final_data = section_data["FinalExam"]
            status = final_data["MeetingStatus"]
            final_exam.no_exam_or_nontraditional = False
            final_exam.is_confirmed = False
            if (status == "2") or (status == "3"):
                final_exam.is_confirmed = True
            elif status == "1":
                final_exam.no_exam_or_nontraditional = True

            final_exam.building = final_data["Building"]
            final_exam.room_number = final_data["RoomNumber"]

            final_format = "%Y-%m-%d : %H:%M"

            strptime = datetime.strptime
            if final_data["Date"] and final_data["Date"] != "0000-00-00":
                if final_data["StartTime"]:
                    start_string = "%s : %s" % (final_data["Date"],
                                                final_data["StartTime"])
                    final_exam.start_date = strptime(start_string,
                                                     final_format)

                if final_data["EndTime"]:
                    end_string = "%s : %s" % (final_data["Date"],
                                              final_data["EndTime"])
                    final_exam.end_date = strptime(end_string, final_format)

            final_exam.clean_fields()
            section.final_exam = final_exam

    return section
