from restclients.sws.v4.registration import get_active_registrations_by_section as v4_get_active_registrations_by_section
from restclients.sws.v4.registration import get_all_registrations_by_section as v4_get_all_registrations_by_section
from restclients.sws.v4.registration import get_credits_by_section_and_regid as v4_get_credits_by_section_and_regid
from restclients.sws.v4.registration import get_schedule_by_regid_and_term as v4_get_schedule_by_regid_and_term

def get_active_registrations_by_section(*args, **kwargs):
    return v4_get_active_registrations_by_section(*args, **kwargs)

def get_all_registrations_by_section(*args, **kwargs):
    return v4_get_all_registrations_by_section(*args, **kwargs)

def get_credits_by_section_and_regid(*args, **kwargs):
    return v4_get_credits_by_section_and_regid(*args, **kwargs)

def get_schedule_by_regid_and_term(*args, **kwargs):
    return v4_get_schedule_by_regid_and_term(*args, **kwargs)

