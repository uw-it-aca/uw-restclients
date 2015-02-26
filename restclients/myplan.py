"""
This is the interface for interacting with MyPlan.

https://wiki.cac.washington.edu/display/MyPlan/Plan+Resource+v1

"""

from restclients.dao import MyPlan_DAO
from restclients.exceptions import DataFailureException
from restclients.models.myplan import MyPlan, MyPlanTerm
from restclients.models.myplan import MyPlanCourse, MyPlanCourseSection
import json


def get_plan(regid, year, quarter, terms=4):
    dao = MyPlan_DAO()
    url = get_plan_url(regid, year, quarter, terms)

    response = dao.getURL(url, {"Accept": "application/json"})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    data = json.loads(response.data)

    plan = MyPlan()
    for term_data in data:
        term = MyPlanTerm()
        term.year = term_data["Term"]["Year"]
        term.quarter = term_data["Term"]["Quarter"]

        for course_data in term_data["Courses"]:
            course = MyPlanCourse()
            course.curriculum_abbr = course_data["CurriculumAbbreviation"]
            course.course_number = course_data["CourseNumber"]

            is_available = course_data["RegistrationAvailable"]
            course.registrations_available = is_available

            for section_data in course_data["Sections"]:
                section = MyPlanCourseSection()
                section.section_id = section_data["SectionId"]
                course.sections.append(section)

            term.courses.append(course)
        plan.terms.append(term)
    return plan


def get_plan_url(regid, year, quarter, terms):
    return "/api/plan/v1/%s,%s,%s,%s" % (year, quarter, terms, regid)
