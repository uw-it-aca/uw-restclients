from restclients.sws.v4.college import get_all_colleges as v4_get_all_colleges
from restclients.sws.v5.college import get_all_colleges as v5_get_all_colleges
from restclients.sws import use_v5_resources

def get_all_colleges(*args, **kwargs):
    if use_v5_resources():
        return v5_get_all_colleges(*args, **kwargs)
    else:
        return v4_get_all_colleges(*args, **kwargs)

