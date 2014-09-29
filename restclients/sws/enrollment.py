from restclients.sws.v4.enrollment import get_grades_by_regid_and_term as v4_get_grades_by_regid_and_term
from restclients.sws.v4.enrollment import get_enrollment_by_regid_and_term as v4_get_enrollment_by_regid_and_term

def get_grades_by_regid_and_term(*args, **kwargs):
    return v4_get_grades_by_regid_and_term(*args, **kwargs)

def get_enrollment_by_regid_and_term(*args, **kwargs):
    return v4_get_enrollment_by_regid_and_term(*args, **kwargs)

