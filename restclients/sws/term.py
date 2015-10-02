from restclients.sws.v5.term import get_term_by_year_and_quarter
from restclients.sws.v5.term import get_current_term
from restclients.sws.v5.term import get_next_term
from restclients.sws.v5.term import get_previous_term
from restclients.sws.v5.term import get_term_before
from restclients.sws.v5.term import get_term_after
from restclients.sws.v5.term import get_term_by_date


def get_specific_term(year, quarter):
    """
    Rename the get_term_by_year_and_quarter to a short name.
    """
    return get_term_by_year_and_quarter(year, quarter.lower())


"""
The following are utility function:
(Note, the acronym "bod" stands for the midnight at the beginning of day
and "eod" the midnight at the end of day)
"""


def get_bod_1st_day_term_after(term):
    """
    Return the datetime object of the beginning of
    the first instruction day in the term after the given term.
    """
    return get_term_after(term).get_bod_first_day()


def get_next_autumn_term(term):
    """
    Return the Term object for the next autumn quarter
    in the same year as the given term
    """
    return get_specific_term(term.year, 'autumn')


def get_next_non_summer_term(term):
    """
    Return the Term object for the quarter after
    as the given term (skip the summer quarter)
    """
    next_term = get_term_after(term)
    if next_term.is_summer_quarter():
        return get_next_autumn_term(next_term)
    return next_term


def is_a_term(str):
    return str is not None and str.lower() == "a-term"


def is_b_term(str):
    return str is not None and str.lower() == "b-term"


def is_half_summer_term(str):
    """
    return True if the given str is A-term or B-term
    @return True if the given str is A-term or B-term
    """
    return is_a_term(str) or is_b_term(str)


def is_full_summer_term(str):
    return str is not None and str.lower() == "full-term"


def is_same_summer_term(str1, str2):
    return str1 is not None and str2 is not None and\
        str1.lower() == str2.lower()
