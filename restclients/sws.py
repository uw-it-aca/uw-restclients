"""
This is the interface for interacting with the Student Web Service.
"""

from restclients.pws import PWS
from restclients.dao import SWS_DAO
from restclients.models import Term, Section, SectionMeeting
from restclients.models import ClassSchedule
from restclients.exceptions import DataFailureException
from urllib import urlencode
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
            raise DataFailureException(url, response.status, response.read())

        return self._term_from_json(response.data)

    def get_current_term(self):
        """
        Returns a restclients.Term object, for the current term.
        """
        url = "/student/v4/term/current.json"

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.read())

        return self._term_from_json(response.data)

    def get_next_term(self):
        """
        Returns a restclients.Term object, for the next term.
        """
        url = "/student/v4/term/next.json"

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.read())

        return self._term_from_json(response.data)

    def get_previous_term(self):
        """
        Returns a restclients.Term object, for the previous term.
        """
        url = "/student/v4/term/previous.json"

        dao = SWS_DAO()
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.read())

        return self._term_from_json(response.data)

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
            raise DataFailureException(url, response.status, response.read())

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
                raise DataFailureException(reg_url, response.status, response.read())

            section_data = json.loads(response.data)

            section = Section()
            section_term = Term()
            section_term.year = section_data["Course"]["Year"]
            section_term.quarter = section_data["Course"]["Quarter"]
            section.term = section_term

            section.curriculum_abbr = section_data["Course"]["CurriculumAbbreviation"]
            section.course_number = section_data["Course"]["CourseNumber"]
            section.section_id = section_data["SectionID"]
            section.course_title = section_data["Course"]["CourseTitle"]
            section.course_campus = section_data["CourseCampus"]
            section.section_type = section_data["SectionType"]
            section.class_website_url = section_data["ClassWebsiteUrl"]
            section.sln = section_data["SLN"]
            section.summer_term = section_data["SummerTerm"]

            # These come from the Term resource
            # section.start_date = ...
            # section.end_date = ...
            # final exam schedule...

            section_meetings = []
            for meeting_data in section_data["Meetings"]:
                meeting = SectionMeeting()
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

                meeting.days_week = meeting_data["DaysOfWeek"]["Text"]
                if meeting_data["DaysOfWeekToBeArranged"]:
                    meeting.days_to_be_arranged = True
                else:
                    meeting.days_to_be_arranged = False

                meeting.start_time = meeting_data["StartTime"]
                meeting.end_time = meeting_data["EndTime"]

                instructors = []
                for instructor_data in meeting_data["Instructors"]:
                    instructor = pws.get_person_by_regid(instructor_data["Person"]["RegID"])

                    if instructor is not None:
                        instructors.append(instructor)

                meeting.instructors = instructors
                section_meetings.append(meeting)

            section.meetings = section_meetings
            sections.append(section)

        schedule = ClassSchedule()
        schedule.sections = sections
        schedule.term = term

        return schedule

    def _term_from_json(self, data):
        term_data = json.loads(data)
        term = Term()
        term.year = term_data["Year"]
        term.quarter = term_data["Quarter"]
        term.first_day_quarter = term_data["FirstDay"]
        term.last_day_instruction = term_data["LastDayOfClasses"]
        term.aterm_last_date = term_data["ATermLastDay"]
        term.bterm_first_date = term_data["BTermFirstDay"]
        term.last_final_exam_date = term_data["LastFinalExamDay"]
        term.grading_period_open = term_data["GradingPeriodOpen"]
        term.grading_period_close = term_data["GradingPeriodClose"]
        term.grade_submission_deadline = term_data["GradeSubmissionDeadline"]

        return term
