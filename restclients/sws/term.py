from restclients.sws.v4.term import get_term_by_year_and_quarter as v4_get_term_by_year_and_quarter
from restclients.sws.v4.term import get_current_term as v4_get_current_term
from restclients.sws.v4.term import get_next_term as v4_get_next_term
from restclients.sws.v4.term import get_previous_term as v4_get_previous_term
from restclients.sws.v4.term import get_term_before as v4_get_term_before
from restclients.sws.v4.term import get_term_after as v4_get_term_after

def get_term_by_year_and_quarter(*args, **kwargs):
    return v4_get_term_by_year_and_quarter(*args, **kwargs)

def get_current_term(*args, **kwargs):
    return v4_get_current_term(*args, **kwargs)

def get_next_term(*args, **kwargs):
    return v4_get_next_term(*args, **kwargs)

def get_previous_term(*args, **kwargs):
    return v4_get_previous_term(*args, **kwargs)

def get_term_before(*args, **kwargs):
    return v4_get_term_before(*args, **kwargs)

def get_term_after(*args, **kwargs):
    return v4_get_term_after(*args, **kwargs)

