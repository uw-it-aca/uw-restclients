"""
Interfacing with the Student Web Service, Enrollment resource.
"""
import logging
from restclients.pws import PWS
from restclients.models.sws import Term
from restclients.models.sws import StudentGrades, StudentCourseGrade
from restclients.sws import get_resource
from restclients.sws.section import get_section_by_url


logger = logging.getLogger(__name__)
enrollment_res_url_prefix = "/student/v4/enrollment"


def get_grades_by_regid_and_term(regid, term):
    """
    Returns a StudentGrades model for the regid and term.
    """
    url = "%s/%s,%s,%s.json" % (enrollment_res_url_prefix,
                                term.year, 
                                term.quarter, 
                                regid)
    return _json_to_grades(get_resource(url), regid, term)


def _json_to_grades(data, regid, term): 
    grades = StudentGrades()
    grades.term = term
    grades.user = PWS().get_person_by_regid(regid)

    grades.grade_points = data["QtrGradePoints"]
    grades.credits_attempted = data["QtrGradedAttmp"]
    grades.non_grade_credits = data["QtrNonGrdEarned"]
    grades.grades = []

    for registration in data["Registrations"]:
        grade = StudentCourseGrade()
        grade.grade = registration["Grade"]
        grade.credits = registration["Credits"].replace(" ", "")
        grade.section = get_section_by_url(registration["Section"]["Href"])
        grades.grades.append(grade)

    return grades

