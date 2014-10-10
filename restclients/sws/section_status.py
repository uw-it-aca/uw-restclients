from restclients.sws.v4.section_status import get_section_status_by_label as v4_get_section_status_by_label
from restclients.sws.v5.section_status import get_section_status_by_label as v5_get_section_status_by_label
from restclients.sws import use_v5_resources

def get_section_status_by_label(*args, **kwargs):
    if use_v5_resources():
        return v5_get_section_status_by_label(*args, **kwargs)
    else:
        return v4_get_section_status_by_label(*args, **kwargs)

