from restclients.sws.v4.campus import get_all_campuses as v4_get_all_campuses
from restclients.sws.v5.campus import get_all_campuses as v5_get_all_campuses
from restclients.sws import use_v5_resources

def get_all_campuses(*args, **kwargs):
    if use_v5_resources():
        return v5_get_all_campuses(*args, **kwargs)
    else:
        return v4_get_all_campuses(*args, **kwargs)
