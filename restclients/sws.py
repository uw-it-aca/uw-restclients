"""
This is the interface for interacting with the Student Web Service.
"""

from restclients.pws import PWS
from restclients.dao import SWS_DAO
from restclients.models import Term, Section, SectionMeeting
from restclients.models import ClassSchedule
from restclients.models import Campus, College, Department, Curriculum
from restclients.exceptions import DataFailureException, InvalidSectionID
from urllib import urlencode
from datetime import datetime
import json
import re


class SWS(object):
    """
    The SWS object has methods for getting information
    about courses, and everything related.
    """

    def get_term_by_year_and_quarter(self, year, quarter):
        """
        Returns a restclients.Term object, for the passed year and quarter.
        """
        url = "/student/v4/term/%s,%s.json" % (str(year), quarter.lower())

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._term_from_json(response.data)

    def get_current_term(self):
        """
        Returns a restclients.Term object, for the current term.
        """
        url = "/student/v4/term/current.json"

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        term = self._term_from_json(response.data)

        # A term doesn't become "current" until 2 days before the start of
        # classes.  That's too late to be useful, so if we're after the last
        # day of grade submission window, use the next term resource.
        if datetime.now() > term.grade_submission_deadline:
            return self.get_next_term()

        return term


    def get_next_term(self):
        """
        Returns a restclients.Term object, for the next term.
        """
        url = "/student/v4/term/next.json"

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._term_from_json(response.data)

    def get_previous_term(self):
        """
        Returns a restclients.Term object, for the previous term.
        """
        url = "/student/v4/term/previous.json"

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._term_from_json(response.data)

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

        url = "/student/v4/course/%s.json" % re.sub(r'\s', '%20', label)

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._section_from_json(response.data)

    def get_linked_sections(self, section):
        """
        Returns a list of restclients.Section objects, representing linked
        sections for the passed section.
        """
        dao = SWS_DAO()
        linked_sections = []

        urls = section.linked_section_urls
        for url in urls:
            response = dao.getURL(url, {"Accept": "application/json"})

            if response.status != 200:
                raise DataFailureException(url, response.status,
                                           response.data)

            section = self._section_from_json(response.data)
            linked_sections.append(section)

        return linked_sections

    def schedule_for_regid_and_term(self, regid, term):
        """
        Returns a restclients.ClassSchedule for the regid and term passed in.
        """
        dao = SWS_DAO()
        pws = PWS()
        url = "/student/v4/registration.json?" + urlencode({
            'year': term.year,
            'quarter': term.quarter,
            'reg_id': regid,
            'is_active': 'on',
        })
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        term_data = json.loads(response.data)

        sections = []

        for registration in term_data["Registrations"]:
            reg_url = registration["Href"]

            # Skip a step here, and go right to the course section resource
            reg_url = re.sub('registration', 'course', reg_url)
            reg_url = re.sub('^(.*?,.*?,.*?,.*?,.*?),.*', '\\1.json', reg_url)
            reg_url = re.sub(',([^,]*).json', '/\\1.json', reg_url)
            response = dao.getURL(reg_url, {"Accept": "application/json"})

            if response.status != 200:
                raise DataFailureException(
                                            reg_url,
                                            response.status,
                                            response.data,
                                          )

            section = self._section_from_json(response.data)

            # For independent study courses, only include the one relevant 
            # instructor
            if registration["Instructor"]:
                actual_instructor = None
                regid = registration["Instructor"]["RegID"]

                for instructor in section.meetings[0].instructors:
                    if instructor.uwregid == regid:
                        actual_instructor = instructor

                if actual_instructor:
                    section.meetings[0].instructors = [ actual_instructor ]
                else:
                    section.meetings[0].instructors = [ ]
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
            colleges.append(college)

        return colleges

    def get_departments_for_college(self, college):
        """
        Returns a list of restclients.Department models, for the passed
        College model.
        """
        url = "/student/v4/college.json?" + urlencode({
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
            departments.append(department)

        return departments

    def get_curricula_for_department(self, department):
        """
        Returns a list of restclients.Curriculum models, for the passed
        Department model.
        """
        url = "/student/v4/college.json?" + urlencode({
              "department_abbreviation": department.label})
        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        curricula = []
        for curr_data in data.get("Curricula", []):
            curriculum = Curriculum()
            curriculum.department_label = department.label
            curriculum.label = curr_data["CurriculumAbbreviation"]
            curriculum.name = curr_data["CurriculumName"]
            curriculum.full_name = curr_data["CurriculumFullName"]
            curricula.append(curriculum)

        return curricula

    def _term_from_json(self, data):
        """
        Returns a term model created from the passed json.
        """
        term_data = json.loads(data)

        strptime = datetime.strptime
        day_format = "%Y-%m-%d"
        datetime_format = "%Y-%m-%dT%H:%M:%S"

        term = Term()
        term.year = term_data["Year"]
        term.quarter = term_data["Quarter"]
        term.first_day_quarter = strptime(
                                    term_data["FirstDay"], day_format
                                    )

        term.last_day_instruction = strptime(
                                    term_data["LastDayOfClasses"],
                                    day_format
                                    )

        if term_data["ATermLastDay"] is not None:
            term.aterm_last_date = strptime(
                                    term_data["ATermLastDay"],
                                    day_format
                                    )

        if term_data["BTermFirstDay"] is not None:
            term.bterm_first_date = strptime(
                                    term_data["BTermFirstDay"],
                                    day_format
                                    )

        term.last_final_exam_date = strptime(
                                    term_data["LastFinalExamDay"],
                                    day_format
                                    )

        term.grading_period_open = strptime(
                                    term_data["GradingPeriodOpen"],
                                    datetime_format
                                    )

        term.grading_period_close = strptime(
                                    term_data["GradingPeriodClose"],
                                    datetime_format
                                    )

        term.grade_submission_deadline = strptime(
                                    term_data["GradeSubmissionDeadline"],
                                    datetime_format)

        term.full_clean()
        return term

    def _section_from_json(self, data):
        """
        Returns a section model created from the passed json.
        """
        pws = PWS()
        section_data = json.loads(data)

        section = Section()
        section.term = self.get_term_by_year_and_quarter(
                                section_data["Course"]["Year"],
                                section_data["Course"]["Quarter"]
                                )
        section.curriculum_abbr = section_data["Course"][
            "CurriculumAbbreviation"]
        section.course_number = section_data["Course"]["CourseNumber"]
        section.course_title = section_data["Course"]["CourseTitle"]
        section.course_title_long = section_data["Course"]["CourseTitleLong"]
        section.course_campus = section_data["CourseCampus"]
        section.section_id = section_data["SectionID"]
        section.section_type = section_data["SectionType"]
        section.class_website_url = section_data["ClassWebsiteUrl"]
        section.sln = section_data["SLN"]
        section.summer_term = section_data["SummerTerm"]
        section.delete_flag = section_data["DeleteFlag"]

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

                    if instructor is not None:
                        meeting.instructors.append(instructor)

            section.meetings.append(meeting)

        return section
