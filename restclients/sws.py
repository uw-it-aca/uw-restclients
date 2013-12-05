"""
This is the interface for interacting with the Student Web Service.
"""

from restclients.pws import PWS
from restclients.dao import SWS_DAO
from restclients.models.sws import Term, Section, SectionReference
from restclients.models.sws import TimeScheduleConstruction
from restclients.models.sws import SectionMeeting, SectionStatus
from restclients.models.sws import Registration, ClassSchedule, FinalExam
from restclients.models.sws import Campus, College, Department, Curriculum
from restclients.models.sws import GradeRoster, GradeRosterItem
from restclients.models.sws import GradeSubmissionDelegate
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidSectionID, InvalidSectionURL
from urllib import urlencode
from datetime import datetime
from lxml import etree
import json
import re


QUARTER_SEQ = ["winter", "spring", "summer", "autumn"]


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

    def get_term_before(self, term):
        """
        Returns a restclients.Term object, for the term after the term given.
        """
        prev_year = term.year
        prev_quarter = QUARTER_SEQ[QUARTER_SEQ.index(term.quarter) - 1]

        if prev_quarter == "autumn":
            prev_year = prev_year - 1

        return self.get_term_by_year_and_quarter(prev_year, prev_quarter)

    def get_term_after(self, term):
        """
        Returns a restclients.Term object, for the term after the term given.
        """
        next_year = term.year
        if term.quarter == "autumn":
            next_quarter = QUARTER_SEQ[0]
        else:
            next_quarter = QUARTER_SEQ[QUARTER_SEQ.index(term.quarter) + 1]

        if next_quarter == "winter":
            next_year = next_year + 1

        return self.get_term_by_year_and_quarter(next_year, next_quarter)

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
        return self._get_sections_by_person_and_term(person, term,
            course_role="Instructor")

    def get_sections_by_delegate_and_term(self, person, term):
        """
        Returns a list of restclients.SectionReference objects for the passed
        grade submission delegate and term.
        """
        return self._get_sections_by_person_and_term(person, term,
            course_role="GradeSubmissionDelegate")

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

        url = "/student/v4/course/%s.json" % re.sub(r'\s', '%20', label)

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
        Returns a restclients.SectionStatus object for the passed section label.
        """
        valid = re.compile('^\d{4},'                           # year
                           '(?:winter|spring|summer|autumn),'  # quarter
                           '[\w& ]+,'                          # curriculum
                           '\d{3}\/'                           # course number
                           '[A-Z][A-Z0-9]?$',                  # section id
                           re.VERBOSE)
        if not valid.match(label):
            raise InvalidSectionID(label)

        url = "/student/v4/course/%s/status.json" % re.sub(r'\s', '%20', label)

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

        instructor_reg_id = ''
        if (section.is_independent_study and
                section.independent_study_instructor_regid is not None):
            instructor_reg_id = section.independent_study_instructor_regid

        url = "/student/v4/registration.json?" + urlencode({
            "year": section.term.year,
            "quarter": section.term.quarter,
            "curriculum_abbreviation": section.curriculum_abbr,
            "course_number": section.course_number,
            "section_id": section.section_id,
            "instructor_reg_id": instructor_reg_id,
            "is_active": ""})

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        all_registration_data = []
        for reg_data in data.get("Registrations", []):
            all_registration_data.append(reg_data)

        all_registration_data.reverse()

        pws = PWS()
        for reg_data in all_registration_data:
            # Prevent duplicate registrations, the reverse() above ensures we
            # keep the latest duplicate
            if reg_data["RegID"] not in seen_registrations:
                registration = Registration()
                registration.section = section
                registration.person = pws.get_person_by_regid(reg_data["RegID"])
                registration.is_active = False
                registrations.append(registration)

                seen_registrations[reg_data["RegID"]] = True

        return registrations

    def get_active_registrations_for_section(self, section):
        """
        Returns a list of restclients.Registration objects, representing
        active registrations for the passed section. For independent study
        sections, section.independent_study_instructor_regid limits
        registrations to that instructor.
        """
        instructor_reg_id = ''
        if (section.is_independent_study and
                section.independent_study_instructor_regid is not None):
            instructor_reg_id = section.independent_study_instructor_regid

        url = "/student/v4/registration.json?" + urlencode({
            "year": section.term.year,
            "quarter": section.term.quarter,
            "curriculum_abbreviation": section.curriculum_abbr,
            "course_number": section.course_number,
            "section_id": section.section_id,
            "instructor_reg_id": instructor_reg_id,
            "is_active": "on"})

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        pws = PWS()
        seen_registrations = {}
        registrations = []
        for reg_data in data.get("Registrations", []):
            if reg_data["RegID"] not in seen_registrations:
                registration = Registration()
                registration.section = section
                registration.person = pws.get_person_by_regid(reg_data["RegID"])
                registration.is_active = True
                registrations.append(registration)

                seen_registrations[reg_data["RegID"]] = True

        return registrations

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

        for registration in term_data["Registrations"]:
            reg_url = registration["Href"]

            # Skip a step here, and go right to the course section resource
            reg_url = re.sub('registration', 'course', reg_url)
            reg_url = re.sub('^(.*?,.*?,.*?,.*?,.*?),.*', '\\1.json', reg_url)
            reg_url = re.sub(',([^,]*).json', '/\\1.json', reg_url)
            response = dao.getURL(reg_url, {"Accept": "application/json"})

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
            campus.full_clean()
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
            college.full_clean()
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
            department.full_clean()
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

    def get_graderoster(self, section, instructor):
        """
        Returns a restclients.GradeRoster model for the passed Section model
        and instructor Person.
        """
        url = "/student/v4/graderoster/%s,%s" % (
            section.section_label().replace('/', ','),
            instructor.uwregid)

        response = SWS_DAO().getURL(url, {"Accept": "text/xhtml",
                                          "X-UW-Act-as": instructor.uwnetid})

        if response.status != 200:
            root = etree.fromstring(response.data)
            msg = root.find('.//*[@class="status_description"]').text.strip()
            raise DataFailureException(url, response.status, msg)

        return self._graderoster_from_xhtml(response.data, section, instructor)

    def update_graderoster(self, graderoster):
        """
        Updates the graderoster for the passed Section model, using the passed
        restclients.GradeRoster model. A new restclients.GradeRoster is
        returned.
        """
        section_id = graderoster.section.section_label().replace('/', ',')
        reg_id = graderoster.instructor.uwregid
        url = "/student/v4/graderoster/%s,%s" % (section_id, reg_id)
        body = graderoster.xhtml()

        dao = SWS_DAO()
        response = dao.putURL(url, {"Content-Type": "application/xhtml+xml",
                                    "X-UW-Act-as": graderoster.instructor.uwnetid},
                              body)

        if response.status != 200:
            root = etree.fromstring(response.data)
            msg = root.find('.//*[@class="status_description"]').text.strip()
            raise DataFailureException(url, response.status, msg)

        return self._graderoster_from_xhtml(response.data,
                                            graderoster.section,
                                            graderoster.instructor)

    def _curriculum_from_json(self, data):
        """
        Returns a curriculum model created from the passed json.
        """
        curriculum = Curriculum()
        curriculum.label = data["CurriculumAbbreviation"]
        curriculum.name = data["CurriculumName"]
        curriculum.full_name = data["CurriculumFullName"]
        curriculum.full_clean()
        return curriculum

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

        term.last_day_add = strptime(
            term_data["LastAddDay"], day_format)

        term.first_day_quarter = strptime(
            term_data["FirstDay"], day_format)

        term.last_day_instruction = strptime(
            term_data["LastDayOfClasses"], day_format)

        term.last_day_drop = strptime(
            term_data["LastDropDay"], day_format)

        if term_data["ATermLastDay"] is not None:
            term.aterm_last_date = strptime(
                term_data["ATermLastDay"], day_format)

        if term_data["BTermFirstDay"] is not None:
            term.bterm_first_date = strptime(
                term_data["BTermFirstDay"], day_format)

        if term_data["LastAddDayATerm"] is not None:
            term.aterm_last_day_add = strptime(
                term_data["LastAddDayATerm"], day_format)

        if term_data["LastAddDayBTerm"] is not None:
            term.bterm_last_day_add = strptime(
                term_data["LastAddDayBTerm"], day_format)

        term.last_final_exam_date = strptime(
            term_data["LastFinalExamDay"], day_format)

        term.grading_period_open = strptime(
            term_data["GradingPeriodOpen"], datetime_format)

        if term_data["GradingPeriodOpenATerm"] is not None:
            term.aterm_grading_period_open = strptime(
                term_data["GradingPeriodOpenATerm"], datetime_format)

        term.grading_period_close = strptime(
            term_data["GradingPeriodClose"], datetime_format)

        term.grade_submission_deadline = strptime(
            term_data["GradeSubmissionDeadline"], datetime_format)

        term.time_schedule_construction = []
        for campus in term_data["TimeScheduleConstructionOn"]:
            tsc = TimeScheduleConstruction(campus=campus.lower(),
                                           is_on = (term_data["TimeScheduleConstructionOn"][campus] == True))
            term.time_schedule_construction.append(tsc)

        term.full_clean()
        return term

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
            section.term = self.get_term_by_year_and_quarter(
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

                final_exam.full_clean()
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

    def _graderoster_from_xhtml(self, data, section, instructor):
        pws = PWS()
        people = {instructor.uwregid: instructor}
        root = etree.fromstring(data)

        graderoster = GradeRoster()
        graderoster.section = section
        graderoster.instructor = instructor
        graderoster.section_credits = root.find('.//*[@class="section_credits"]').text.strip()

        writing_credit = root.find('.//*[@class="writing_credit_display"]').get("checked")
        graderoster.allows_writing_credit = True if writing_credit == "checked" else False

        default_section_id = root.find('.//*[@rel="section"]//*[@class="section_id"]').text.upper()

        graderoster.authorized_grade_submitters = []
        graderoster.grade_submission_delegates = []
        graderoster.items = []

        auth_grade_submitters = root.findall('.//*[@rel="authorized_grade_submitter"]')
        for ags in auth_grade_submitters:
            reg_id = ags.find('.//*[@class="reg_id"]').text.strip()
            if reg_id not in people:
                people[reg_id] = pws.get_person_by_regid(reg_id)

            graderoster.authorized_grade_submitters.append(people[reg_id])

        grade_submission_delegates = root.findall('.//*[@class="grade_submission_delegate"]')
        for gsd in grade_submission_delegates:
            reg_id = gsd.find('.//*[@class="reg_id"]').text.strip()
            delegate_level = gsd.find('.//*[@class="delegate_level"]').text.strip()
            if reg_id not in people:
                people[reg_id] = pws.get_person_by_regid(reg_id)
            delegate = GradeSubmissionDelegate(person=people[reg_id],
                                               delegate_level=delegate_level)
            graderoster.grade_submission_delegates.append(delegate)

        strptime = datetime.strptime
        day_format = "%Y-%m-%d"
        item_elements = root.findall('.//*[@class="graderoster_item"]')
        for item in item_elements:
            gr_item = GradeRosterItem()

            section_element = item.find('.//*[@class="section_id"]')
            gr_item.section_id = section_element.text if section_element is not None else default_section_id

            reg_id = item.find('.//*[@class="reg_id"]').text.strip()
            gr_item.student = pws.get_person_by_regid(reg_id)

            duplicate_code = item.find('.//*[@class="duplicate_code"]').text
            if duplicate_code is not None:
                duplicate_code = duplicate_code.strip()
                duplicate_code = duplicate_code if len(duplicate_code) else None
            gr_item.duplicate_code = duplicate_code

            gr_item.student_number = item.find('.//*[@class="student_number"]').text.strip()

            student_former_name = item.find('.//*[@class="student_former_name"]').text
            if student_former_name is not None:
                student_former_name = student_former_name.strip()
                student_former_name = student_former_name if len(student_former_name) else None
            gr_item.student_former_name = student_former_name

            gr_item.student_credits = item.find('.//*[@class="student_credits"]').text.strip()

            auditor = item.find('.//*[@class="auditor"]').get("checked")
            gr_item.is_auditor = True if auditor == "checked" else False

            gr_item.grade_choices = []
            gr_item.grade = None
            for grade in item.findall('.//*[@class="grade"]'):
                grade_value = grade.get("value").strip()
                gr_item.grade_choices.append(grade_value)
                if grade.get("selected") == "selected":
                    gr_item.grade = grade_value

            incomplete_node = item.find('.//*[@class="incomplete"]')
            gr_item.allows_incomplete = False if incomplete_node.get("disabled") == "disabled" else True
            gr_item.has_incomplete = True if incomplete_node.get("checked") == "checked" else False

            writing_credit = item.find('.//*[@class="writing_course"]').get("checked")
            gr_item.has_writing_credit = True if writing_credit == "checked" else False

            no_grade_now = item.find('.//*[@class="no_grade_now"]').get("checked")
            gr_item.no_grade_now = True if no_grade_now == "checked" else False

            date_withdrawn = item.find('.//*[@class="date_withdrawn date"]').text
            if date_withdrawn is not None:
                gr_item.date_withdrawn = date_withdrawn.strip()

            grade_select = item.find('.//*[@class="grades"]')
            gr_item.allows_grade_change = False if grade_select.get("disabled") == "disabled" else True

            gr_item.grade_document_id = item.find('.//*[@class="grade_document_id"]').text

            date_graded = item.find('.//*[@class="date_graded date"]').text
            if date_graded is not None:
                gr_item.date_graded = date_graded.strip()

            gsp = item.find('.//*[@rel="grade_submitter_person"]')
            if gsp is not None:
                reg_id = gsp.find('.//*[@class="reg_id"]').text.strip()
                if reg_id not in people:
                    people[reg_id] = pws.get_person_by_regid(reg_id)
                gr_item.grade_submitter_person = people[reg_id]

            gr_item.grade_submitter_source = item.find('.//*[@class="grade_submitter_source"]').text

            graderoster.items.append(gr_item)

        return graderoster
