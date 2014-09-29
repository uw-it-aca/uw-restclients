from restclients.sws.v4.curriculum import get_curricula_by_department as v4_get_curricula_by_department
from restclients.sws.v4.curriculum import get_curricula_by_term as v4_get_curricula_by_term

def get_curricula_by_department(*args, **kwargs):
    return v4_get_curricula_by_department(*args, **kwargs)

def get_curricula_by_term(*args, **kwargs):
    return v4_get_curricula_by_term(*args, **kwargs)

