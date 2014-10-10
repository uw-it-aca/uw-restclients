from restclients.sws.v4.enrollment import get_grades_by_regid_and_term as v4_get_grades_by_regid_and_term
from restclients.sws.v4.enrollment import get_enrollment_by_regid_and_term as v4_get_enrollment_by_regid_and_term
from restclients.sws.v5.enrollment import get_grades_by_regid_and_term as v5_get_grades_by_regid_and_term
from restclients.sws.v5.enrollment import get_enrollment_by_regid_and_term as v5_get_enrollment_by_regid_and_term
from restclients.sws import use_v5_resources

def get_grades_by_regid_and_term(*args, **kwargs):
    if use_v5_resources():
        return v5_get_grades_by_regid_and_term(*args, **kwargs)
    else:
        return v4_get_grades_by_regid_and_term(*args, **kwargs)

def get_enrollment_by_regid_and_term(*args, **kwargs):
    if use_v5_resources():
        return v5_get_enrollment_by_regid_and_term(*args, **kwargs)
    else:
        return v4_get_enrollment_by_regid_and_term(*args, **kwargs)

