from restclients.sws.v4.curriculum import get_curricula_by_department as v4_get_curricula_by_department
from restclients.sws.v4.curriculum import get_curricula_by_term as v4_get_curricula_by_term
from restclients.sws.v5.curriculum import get_curricula_by_department as v5_get_curricula_by_department
from restclients.sws.v5.curriculum import get_curricula_by_term as v5_get_curricula_by_term
from restclients.sws import use_v5_resources

def get_curricula_by_department(*args, **kwargs):
    if use_v5_resources():
        return v5_get_curricula_by_department(*args, **kwargs)
    else:
        return v4_get_curricula_by_department(*args, **kwargs)

def get_curricula_by_term(*args, **kwargs):
    if use_v5_resources():
        return v5_get_curricula_by_term(*args, **kwargs)
    else:
        return v4_get_curricula_by_term(*args, **kwargs)
