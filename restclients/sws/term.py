from restclients.sws.v5.term import get_term_by_year_and_quarter
from restclients.sws.v5.term import get_current_term
from restclients.sws.v5.term import get_next_term
from restclients.sws.v5.term import get_previous_term
from restclients.sws.v5.term import get_term_before
from restclients.sws.v5.term import get_term_after
from restclients.sws.v5.term import get_term_by_date
from restclients.util.datetime_convertor import convert_to_begin_of_day,\
    convert_to_end_of_day


def get_specific_term(year, quarter):
    """
    Rename the get_term_by_year_and_quarter to a short name.
    """
    return get_term_by_year_and_quarter(year, quarter)


"""
The following are utility function:
bod: the beginning of day.
eod: the end of day.
"""


def get_bod_1st_day(term):
    """
    @return the datetime object of the begining of
    the first instruction day for the given (full) term.
    """
    return convert_to_begin_of_day(term.first_day_quarter)


def get_bod_1st_day_term_after(term):
    """
    Return the datetime object of the beginning of
    the first instruction day in the term after the given term.
    """
    return get_bod_1st_day(get_term_after(term))


def get_bod_aterm_grading_period(term):
    """
    Return the datetime object of the beginning of
    the summer A-term grading period openning day of the given term.
    Return None if the given term is not a summer term.
    """
    if not is_summer_term(term):
        return None
    return convert_to_begin_of_day(term.aterm_grading_period_open)


def get_bod_grading_period(term):
    """
    Return the datetime object of the beginning of
    the grading period openning day of the given (full) term.
    """
    return convert_to_begin_of_day(term.grading_period_open)


def get_bod_reg_period1_start(term):
    """
    Return the datetime object of the beginning of
    the registration period1 start day for the given term.
    """
    return convert_to_begin_of_day(term.registration_period1_start)


def get_bod_reg_period2_start(term):
    """
    Return the datetime object of the beginning of
    the registration period2 start day for the given term.
    """
    return convert_to_begin_of_day(term.registration_period2_start)


def get_bod_reg_period3_start(term):
    """
    Return the datetime object of the beginning of
    the registration period3 start day for the given term.
    """
    return convert_to_begin_of_day(term.registration_period3_start)


def get_eod_grade_submission(term):
    """
    Return the datetime object of the end of day of
    the grade submission deadline for the given term.
    """
    return convert_to_end_of_day(term.grade_submission_deadline)


def get_eod_grade_submission_term_after(term):
    """
    Return the datetime object of the end of the day of
    the grade submission deadline of the term after the given term.
    Only the summer full term is relevant.
    """
    return get_eod_grade_submission(get_term_after(term))


def get_eod_aterm_last_day_add(term):
    """
    Return the datetime object of the end of
    the last day in summer A-term to add class of the given term.
    Return None if the given term is not a summer term.
    """
    if not is_summer_term(term):
        return None
    return convert_to_end_of_day(term.aterm_last_day_add)


def get_eod_last_day_add(term):
    """
    Return the datetime object of the end of
    the last day to add class of the term after the given term.
    Only the summer full term is relevant.
    """
    return convert_to_end_of_day(term.last_day_add)


def get_eod_last_day_drop(term):
    """
    Return the datetime object of the end of
    the last day to drop class of the term after the given term.
    Only the summer full term is relevant.
    """
    return convert_to_end_of_day(term.last_day_drop)


def get_eod_last_final_exam(term):
    """
    @return the datetime object of the end of
    the last final exam day of the given term.
    Only the summer full term is relevant.
    """
    return convert_to_end_of_day(term.last_final_exam_date)


def get_eod_last_final_exam_term_after(term):
    """
    @return the datetime object of the end of
    the last final exam day of the term after the given term.
    Only the summer full term is relevant.
    """
    return get_eod_last_final_exam(get_term_after(term))


def get_eod_last_instruction(term):
    """
    Return the datetime object of the end of the last instruction day
    for the given term.
    Only the summer full term is relevant.
    """
    return convert_to_end_of_day(term.last_day_instruction)


def get_eod_last_instruction_term_after(term):
    """
    Return the datetime object of the end of the last instruction day
    of the term after the given term.
    Only the summer full term is relevant.
    """
    return get_eod_last_instruction(get_term_after(term))


def get_eod_summer_aterm(term):
    """
    @return the datetime object of the end of
    the summer quarter A-term (also the beginning of summer B-term).
    If the given term is not a summer term, return None.
    """
    if not is_summer_term(term):
        return None
    return convert_to_end_of_day(term.aterm_last_date)


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
    if is_summer_term(next_term):
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


def is_summer_term(term):
    """
    Return True if the term is a summer quarter
    """
    return term.quarter.lower() == "summer"
