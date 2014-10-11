"""
Interfacing with the Student Web Service, Enrollment resource.
"""
import logging
from restclients.pws import PWS
from restclients.models.sws import Term
from restclients.models.sws import StudentGrades, StudentCourseGrade
from restclients.models.sws import Enrollment, Major, Minor
from restclients.sws import get_resource
from restclients.sws.section import get_section_by_url


logger = logging.getLogger(__name__)
enrollment_res_url_prefix = "/student/v5/enrollment"


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


def get_enrollment_by_regid_and_term(regid, term):
    url = "%s/%s,%s,%s.json" % (enrollment_res_url_prefix,
                                term.year,
                                term.quarter,
                                regid)
    return _json_to_enrollment(get_resource(url))


def _json_to_enrollment(json_data):
    enrollment = Enrollment()
    enrollment.regid = json_data['RegID']
    enrollment.class_level = json_data['ClassLevel']
    enrollment.is_honors = json_data['HonorsProgram']

    enrollment.majors = []
    if json_data.get('Majors') is not None and len(json_data['Majors']) > 0:
        for major in json_data['Majors']:
            enrollment.majors.append(_json_to_major(major))

    enrollment.minors = []
    if json_data.get('Minors') is not None and len(json_data['Minors']) > 0:
        for minor in json_data['Minors']:
            enrollment.minors.append(_json_to_minor(minor))
    return enrollment


def _json_to_major(json_data):
    major = Major()
    major.degree_abbr = json_data['Abbreviation']
    major.degree_name = json_data['DegreeName']
    major.full_name = json_data['FullName']
    major.major_name = json_data['MajorName']
    major.short_name = json_data['ShortName']
    major.campus = json_data['Campus']
    return major


def _json_to_minor(json_data):
   minor = Minor()
   minor.abbr = json_data['Abbreviation']
   minor.campus = json_data['CampusName']
   minor.name = json_data['Name']
   minor.full_name = json_data['FullName']
   minor.short_name = json_data['ShortName']
   return minor

