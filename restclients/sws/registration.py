from restclients.sws.v4.registration import get_active_registrations_by_section as v4_get_active_registrations_by_section
from restclients.sws.v4.registration import get_all_registrations_by_section as v4_get_all_registrations_by_section
from restclients.sws.v4.registration import get_credits_by_section_and_regid as v4_get_credits_by_section_and_regid
from restclients.sws.v4.registration import get_schedule_by_regid_and_term as v4_get_schedule_by_regid_and_term
from restclients.sws.v5.registration import get_active_registrations_by_section as v5_get_active_registrations_by_section
from restclients.sws.v5.registration import get_all_registrations_by_section as v5_get_all_registrations_by_section
from restclients.sws.v5.registration import get_credits_by_section_and_regid as v5_get_credits_by_section_and_regid
from restclients.sws.v5.registration import get_schedule_by_regid_and_term as v5_get_schedule_by_regid_and_term
from restclients.sws import use_v5_resources

def get_active_registrations_by_section(*args, **kwargs):
    if use_v5_resources():
        return v5_get_active_registrations_by_section(*args, **kwargs)
    else:
        return v4_get_active_registrations_by_section(*args, **kwargs)

def get_all_registrations_by_section(*args, **kwargs):
    if use_v5_resources():
        return v5_get_all_registrations_by_section(*args, **kwargs)
    else:
        return v4_get_all_registrations_by_section(*args, **kwargs)

def get_credits_by_section_and_regid(*args, **kwargs):
    if use_v5_resources():
        return v5_get_credits_by_section_and_regid(*args, **kwargs)
    else:
        return v4_get_credits_by_section_and_regid(*args, **kwargs)

def get_schedule_by_regid_and_term(*args, **kwargs):
    if use_v5_resources():
        return v5_get_schedule_by_regid_and_term(*args, **kwargs)
    else:
        return v4_get_schedule_by_regid_and_term(*args, **kwargs)
