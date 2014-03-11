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
    logger.debug("%s ==> %s, %s" % (url, response.status, response.data))
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

    def get_term_before(self, term):
        deprecation("Use restclients.sws.term.get_term_before")
        import restclients.sws.term
        return term.get_term_before(term)

    def get_term_after(self, term):
        deprecation("Use restclients.sws.term.get_term_after")
        import restclients.sws.term
        return term.get_term_after(term)

    def _term_from_json(self, data):
        deprecation("Use restclients.sws.term._json_to_term_model")
        import restclients.sws.term
        return term._json_to_term_model(data)

    def _get_sections_by_person_and_term(self, person, term, course_role):
        url = "/student/v4/section.json?" + urlencode({
            "year": term.year,
            "quarter": term.quarter.lower(),
            "reg_id": person.uwregid,
            "search_by": course_role,
            "include_secondaries": "on"})

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        sections = []
        for section_data in data.get("Sections", []):
            section = SectionReference(
                term=term,
                curriculum_abbr=section_data["CurriculumAbbreviation"],
                course_number=section_data["CourseNumber"],
                section_id=section_data["SectionID"],
                url=section_data["Href"])
            sections.append(section)

        return sections

    def get_sections_by_instructor_and_term(self, person, term):
        """
        Returns a list of restclients.SectionReference objects for the passed
        instructor and term.
        """
        return self._get_sections_by_person_and_term(
            person, term, course_role="Instructor")

    def get_sections_by_delegate_and_term(self, person, term):
        """
        Returns a list of restclients.SectionReference objects for the passed
        grade submission delegate and term.
        """
        return self._get_sections_by_person_and_term(
            person, term, course_role="GradeSubmissionDelegate")

    def get_sections_by_curriculum_and_term(self, curriculum, term):
        """
        Returns a list of restclients.SectionReference objects for the passed
        curriculum and term.
        """
        url = "/student/v4/section.json?" + urlencode({
            "year": term.year,
            "quarter": term.quarter.lower(),
            "curriculum_abbreviation": curriculum.label})

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        sections = []
        for section_data in data.get("Sections", []):
            section = SectionReference(
                term=term,
                curriculum_abbr=section_data["CurriculumAbbreviation"],
                course_number=section_data["CourseNumber"],
                section_id=section_data["SectionID"],
                url=section_data["Href"])
            sections.append(section)

        return sections

    def get_section_by_label(self, label):
        """
        Returns a restclients.Section object for the passed section label.
        """
        valid = re.compile('^\d{4},'                           # year
                           '(?:winter|spring|summer|autumn),'  # quarter
                           '[\w& ]+,'                          # curriculum
                           '\d{3}\/'                           # course number
                           '[A-Z][A-Z0-9]?$',                  # section id
                           re.VERBOSE)
        if not valid.match(label):
            raise InvalidSectionID(label)

        url = "/student/v4/course/%s.json" % encode_section_label(label)

        return self.get_section_by_url(url)

    def get_section_by_url(self, url):
        """
        Returns a restclients.Section object for the passed section url.
        """
        if not re.match(r"^\/student\/v4\/course\/", url):
            raise InvalidSectionURL(url)

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._section_from_json(response.data)

    def get_section_status_by_label(self, label):
        """
        Return a restclients.SectionStatus object for the passed section label.
        """
        valid = re.compile('^\d{4},'                           # year
                           '(?:winter|spring|summer|autumn),'  # quarter
                           '[\w& ]+,'                          # curriculum
                           '\d{3}\/'                           # course number
                           '[A-Z][A-Z0-9]?$',                  # section id
                           re.VERBOSE)
        if not valid.match(label):
            raise InvalidSectionID(label)

        url = "/student/v4/course/%s/status.json" % encode_section_label(label)

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._section_status_from_json(response.data)

    def get_linked_sections(self, section):
        """
        Returns a list of restclients.Section objects, representing linked
        sections for the passed section.
        """
        linked_sections = []

        for url in section.linked_section_urls:
            section = self.get_section_by_url(url)
            linked_sections.append(section)

        return linked_sections

    def get_joint_sections(self, section):
        """
        Returns a list of restclients.Section objects, representing joint
        sections for the passed section.
        """
        joint_sections = []

        for url in section.joint_section_urls:
            section = self.get_section_by_url(url)
            joint_sections.append(section)

        return joint_sections

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

        for registration in data["Registrations"]:
            grade = StudentCourseGrade()
            grade.grade = registration["Grade"]
            grade.credits = registration["Credits"].replace(" ", "")
            grade.section = self.get_section_by_url(registration["Section"]["Href"])
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

            section = self._section_from_json(response.data, term)

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

    def _section_from_json(self, data, term=None):
        """
        Returns a section model created from the passed json.
        """
        pws = PWS()
        section_data = json.loads(data)

        section = Section()

        if term is not None and (term.year == int(section_data["Course"]["Year"]) and
                                 term.quarter == section_data["Course"]["Quarter"]):
            section.term = term
        else:
            import restclients.sws.term as TermSws
            section.term = TermSws.get_by_year_and_quarter(
                section_data["Course"]["Year"],
                section_data["Course"]["Quarter"])

        section.curriculum_abbr = section_data["Course"][
            "CurriculumAbbreviation"]
        section.course_number = section_data["Course"]["CourseNumber"]
        section.course_title = section_data["Course"]["CourseTitle"]
        section.course_title_long = section_data["Course"]["CourseTitleLong"]
        section.course_campus = section_data["CourseCampus"]
        section.section_id = section_data["SectionID"]

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
                pdata = instructor_data["Person"]

                if "RegID" in pdata and pdata["RegID"] is not None:
                    instructor = pws.get_person_by_regid(pdata["RegID"])
                    instructor.TSPrint = instructor_data["TSPrint"]
                    meeting.instructors.append(instructor)

            section.meetings.append(meeting)

        section.final_exam = None
        if "FinalExam" in section_data:
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
                        final_exam.start_date = strptime(start_string, final_format)

                    if final_data["EndTime"]:
                        end_string = "%s : %s" % (final_data["Date"],
                                                  final_data["EndTime"])
                        final_exam.end_date = strptime(end_string, final_format)

                final_exam.clean_fields()
                section.final_exam = final_exam

        return section

    def _section_status_from_json(self, data):
        """
        Returns a section status model created from the passed json.
        """
        section_data = json.loads(data)

        section_status = SectionStatus()
        if section_data["AddCodeRequired"] == 'true':
            section_status.add_code_required = True
        else:
            section_status.add_code_required = False
        section_status.current_enrollment = int(section_data["CurrentEnrollment"])
        section_status.current_registration_period = int(section_data["CurrentRegistrationPeriod"])
        if section_data["FacultyCodeRequired"] == 'true':
            section_status.faculty_code_required = True
        else:
            section_status.faculty_code_required = False
        section_status.limit_estimated_enrollment = int(section_data["LimitEstimateEnrollment"])
        section_status.limit_estimate_enrollment_indicator = section_data["LimitEstimateEnrollmentIndicator"]
        section_status.room_capacity = int(section_data["RoomCapacity"])
        section_status.sln = int(section_data["SLN"])
        section_status.space_available = int(section_data["SpaceAvailable"])
        if section_data["Status"] == "open":
            section_status.is_open = True
        else:
            section_status.is_open = False

        return section_status
