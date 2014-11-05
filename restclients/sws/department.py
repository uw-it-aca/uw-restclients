from restclients.sws.v4.department import get_departments_by_college as v4_get_departments_by_college
from restclients.sws.v5.department import get_departments_by_college as v5_get_departments_by_college
from restclients.sws import use_v5_resources

def get_departments_by_college(*args, **kwargs):
    if use_v5_resources():
        return v5_get_departments_by_college(*args, **kwargs)
    else:
        return v4_get_departments_by_college(*args, **kwargs)

