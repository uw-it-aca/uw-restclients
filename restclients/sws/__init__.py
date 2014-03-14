"""
This is the interface for interacting with the Student Web Service.
"""
import logging
import json
import re
import warnings
from urllib import urlencode
from datetime import datetime
from lxml import etree
from restclients.thread import Thread
from restclients.pws import PWS
from restclients.dao import SWS_DAO
from restclients.models.sws import Term, Section, SectionReference
from restclients.models.sws import SectionMeeting, SectionStatus
from restclients.models.sws import Registration, ClassSchedule, FinalExam
from restclients.models.sws import Campus, College, Department, Curriculum
from restclients.models.sws import StudentGrades, StudentCourseGrade
from restclients.models.sws import GradeSubmissionDelegate
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidSectionID, InvalidSectionURL

QUARTER_SEQ = ["winter", "spring", "summer", "autumn"]
logger = logging.getLogger(__name__)


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)

def encode_section_label(label):
    return re.sub(r'\s', '%20', label)

def get_resource(url):
    """
    Issue a GET request to SWS with the given url
    and return a response in json format.
    :returns: http response with content in json
    """
    response = SWS_DAO().getURL(url, {"Accept": "application/json"})
    #logger.debug("%s ==> %s, %s" % (url, response.status, response.data))
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)
    return json.loads(response.data)

class SWSThread(Thread):
    url = None
    headers = None
    response = None

    def run(self):
        if self.url is None:
            raise Exception("SWSThread must have a url")

        args = self.headers or {}

        dao = SWS_DAO()
        self.response = dao.getURL(self.url, args)


class SWSPersonByRegIDThread(Thread):
    regid = None
    person = None

    def run(self):
        if self.regid is None:
            raise Exception("SWSPersonByRegIDThread must have a regid")

        pws = PWS()
        self.person = pws.get_person_by_regid(self.regid)


class SWS(object):
    """
    The SWS object has methods for getting information
    about courses, and everything related.
    """

    def get_term_by_year_and_quarter(self, year, quarter):
        deprecation("Use restclients.sws.term.get_by_year_and_quarter")
        import restclients.sws.term
        return term.get_by_year_and_quarter(year, quarter)

    def get_current_term(self):
        deprecation("Use restclients.sws.term.get_current")
        import restclients.sws.term
        return term.get_current()

    def get_next_term(self):
        deprecation("Use restclients.sws.term.get_next")
        import restclients.sws.term
        return term.get_next()

    def get_previous_term(self):
        deprecation("Use restclients.sws.term.get_previous")
        import restclients.sws.term
        return term.get_previous()

    def get_term_before(self, aterm):
        deprecation("Use restclients.sws.term.get_term_before")
        import restclients.sws.term
        return term.get_term_before(aterm)

    def get_term_after(self, aterm):
        deprecation("Use restclients.sws.term.get_term_after")
        import restclients.sws.term
        return term.get_term_after(aterm)

    def get_sections_by_instructor_and_term(self, person, term):
        deprecation("Use restclients.sws.section.get_sections_by_instructor_and_term")
        import restclients.sws.section
        return section.get_sections_by_instructor_and_term(person, term)

    def get_sections_by_delegate_and_term(self, person, term):
        deprecation("Use restclients.sws.section.get_sections_by_delegate_and_term")
        import restclients.sws.section
        return section.get_sections_by_delegate_and_term(person, term)

    def get_sections_by_curriculum_and_term(self, curriculum, term):
        deprecation("Use restclients.sws.section.get_sections_by_curriculum_and_term")
        import restclients.sws.section
        return section.get_sections_by_curriculum_and_term(curriculum, term)

    def get_section_by_label(self, label):
        deprecation("Use restclients.sws.section.get_section_by_label")
        import restclients.sws.section
        return section.get_section_by_label(label)

    def get_section_by_url(self, url):
        deprecation("Use restclients.sws.section.get_section_by_url")
        import restclients.sws.section
        return section.get_section_by_url(url)

    def get_section_status_by_label(self, label):
        deprecation("Use restclients.sws.section.get_section_status_by_label")
        import restclients.sws.section
        return section.get_section_status_by_label(label)

    def get_linked_sections(self, asection):
        deprecation("Use restclients.sws.section.get_linked_sections")
        import restclients.sws.section
        return section.get_linked_sections(asection)

    def get_joint_sections(self, asection):
        deprecation("Use restclients.sws.section.get_joint_sections")
        import restclients.sws.section
        return section.get_joint_sections(asection)

    def get_all_registrations_for_section(self, section):
        """
        Returns a list of restclients.Registration objects, representing
        all (active and inactive) registrations for the passed section. For
        independent study sections, section.independent_study_instructor_regid
        limits registrations to that instructor.
        """
        registrations = self.get_active_registrations_for_section(section)

        seen_registrations = {}
        for registration in registrations:
            seen_registrations[registration.person.uwregid] = True

        all_registrations = self._registrations_for_section_with_active_flag(section, False)

        for registration in all_registrations:
            regid = registration.person.uwregid
            if regid not in seen_registrations:
                # This is just being set by induction.  The all registrations
                # resource can't know if a registration is active.
                registration.is_active = False
                seen_registrations[regid] = True
                registrations.append(registration)

        return registrations

    def _registrations_for_section_with_active_flag(self, section, is_active):
        """
        Returns a list of all restclients.Registration objects for a section.
        There can be duplicates for a person.
        If is_active is True, the objects will have is_active set to True.
        Otherwise, is_active is undefined, and out of scope for this method.
        """
        instructor_reg_id = ''
        if (section.is_independent_study and
                section.independent_study_instructor_regid is not None):
            instructor_reg_id = section.independent_study_instructor_regid

        activity_flag = ""
        if is_active:
            activity_flag = "on"

        url = "/student/v4/registration.json?" + urlencode({
            "year": section.term.year,
            "quarter": section.term.quarter,
            "curriculum_abbreviation": section.curriculum_abbr,
            "course_number": section.course_number,
            "section_id": section.section_id,
            "instructor_reg_id": instructor_reg_id,
            "is_active": activity_flag})

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        pws = PWS()
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

    def get_active_registrations_for_section(self, section):
        """
        Returns a list of restclients.Registration objects, representing
        active registrations for the passed section. For independent study
        sections, section.independent_study_instructor_regid limits
        registrations to that instructor.
        """
        return self._registrations_for_section_with_active_flag(section, True)

    def grades_for_regid_and_term(self, regid, term):
        """
        Returns a StudentGrades model for the regid and term.
        """
        dao = SWS_DAO()
        pws = PWS()
        url = "/student/v4/enrollment/%s,%s,%s.json" % (term.year, term.quarter, regid)

        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)
        pws = PWS()

        grades = StudentGrades()
        grades.term = term
        grades.user = pws.get_person_by_regid(regid)

        grades.grade_points = data["QtrGradePoints"]
        grades.credits_attempted = data["QtrGradedAttmp"]
        grades.non_grade_credits = data["QtrNonGrdEarned"]
        grades.grades = []

        import restclients.sws.section as SectionSws

        for registration in data["Registrations"]:
            grade = StudentCourseGrade()
            grade.grade = registration["Grade"]
            grade.credits = registration["Credits"].replace(" ", "")
            grade.section = SectionSws.get_section_by_url(registration["Section"]["Href"])
            grades.grades.append(grade)

        return grades

    def schedule_for_regid_and_term(self, regid, term):
        """
        Returns a restclients.ClassSchedule for the regid and term passed in.
        """
        dao = SWS_DAO()
        pws = PWS()
        url = "/student/v4/registration.json?" + urlencode([
            ('reg_id', regid),
            ('quarter', term.quarter),
            ('is_active', 'on'),
            ('year', term.year),
        ])

        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        term_data = json.loads(response.data)

        sections = []

        sws_threads = []
        for registration in term_data["Registrations"]:
            reg_url = registration["Href"]

            # Skip a step here, and go right to the course section resource
            reg_url = re.sub('registration', 'course', reg_url)
            reg_url = re.sub('^(.*?,.*?,.*?,.*?,.*?),.*', '\\1.json', reg_url)
            reg_url = re.sub(',([^,]*).json', '/\\1.json', reg_url)

            thread = SWSThread()
            thread.url = reg_url
            thread.headers = {"Accept": "application/json"}
            thread.start()
            sws_threads.append(thread)

        for thread in sws_threads:
            thread.join()

        for thread in sws_threads:
            response = thread.response

            if response.status != 200:
                raise DataFailureException(reg_url,
                                           response.status,
                                           response.data)
            import restclients.sws.section as sectionsws
            section = sectionsws._json_to_section(json.loads(response.data), term)

            # For independent study courses, only include the one relevant
            # instructor
            if registration["Instructor"]:
                actual_instructor = None
                regid = registration["Instructor"]["RegID"]

                for instructor in section.meetings[0].instructors:
                    if instructor.uwregid == regid:
                        actual_instructor = instructor

                if actual_instructor:
                    section.meetings[0].instructors = [actual_instructor]
                else:
                    section.meetings[0].instructors = []
                section.independent_study_instructor_regid = registration["Instructor"]
            sections.append(section)

        schedule = ClassSchedule()
        schedule.sections = sections
        schedule.term = term

        return schedule

    def get_all_campuses(self):
        """
        Returns a list of restclients.Campus models, representing all
        campuses.
        """
        url = "/student/v4/campus.json"
        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        campuses = []
        for campus_data in data.get("Campuses", []):
            campus = Campus()
            campus.label = campus_data["CampusShortName"]
            campus.name = campus_data["CampusName"]
            campus.full_name = campus_data["CampusFullName"]
            campus.clean_fields()
            campuses.append(campus)

        return campuses

    def get_all_colleges(self):
        """
        Returns a list of restclients.College models, representing all
        colleges.
        """
        url = "/student/v4/college.json"
        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        colleges = []
        for college_data in data.get("Colleges", []):
            college = College()
            college.campus_label = college_data["CampusShortName"]
            college.label = college_data["CollegeAbbreviation"]
            college.name = college_data["CollegeName"]
            college.full_name = college_data["CollegeFullName"]
            college.clean_fields()
            colleges.append(college)

        return colleges

    def get_departments_for_college(self, college):
        """
        Returns a list of restclients.Department models, for the passed
        College model.
        """
        url = "/student/v4/department.json?" + urlencode({
              "college_abbreviation": college.label})
        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        departments = []
        for dept_data in data.get("Departments", []):
            department = Department()
            department.college_label = college.label
            department.label = dept_data["DepartmentAbbreviation"]
            department.name = dept_data["DepartmentFullName"]
            department.full_name = dept_data["DepartmentFullName"]
            department.clean_fields()
            departments.append(department)

        return departments

    def get_curricula_for_department(self, department, future_terms=0):
        """
        Returns a list of restclients.Curriculum models, for the passed
        Department model.
        """
        if future_terms < 0 or future_terms > 2:
            raise ValueError(future_terms)

        url = "/student/v4/curriculum.json?" + urlencode({
              "department_abbreviation": department.label,
              "future_terms": future_terms})
        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        curricula = []
        for curr_data in data.get("Curricula", []):
            curricula.append(self._curriculum_from_json(curr_data))

        return curricula

    def get_curricula_for_term(self, term):
        """
        Returns a list of restclients.Curriculum models, for the passed
        Term model.
        """
        url = "/student/v4/curriculum.json?" + urlencode({
            "year": term.year,
            "quarter": term.quarter.lower()})
        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        curricula = []
        for curr_data in data.get("Curricula", []):
            curricula.append(self._curriculum_from_json(curr_data))

        return curricula

    def _curriculum_from_json(self, data):
        """
        Returns a curriculum model created from the passed json.
        """
        curriculum = Curriculum()
        curriculum.label = data["CurriculumAbbreviation"]
        curriculum.name = data["CurriculumName"]
        curriculum.full_name = data["CurriculumFullName"]
        curriculum.clean_fields()
        return curriculum

