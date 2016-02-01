"""
This class interfaces with the Student Web Service, Term resource.
"""
import logging
from datetime import datetime
from restclients.sws import get_resource, QUARTER_SEQ, get_current_sws_version, parse_sws_date
from restclients.models.sws import Term as TermModel
from restclients.exceptions import DataFailureException
from restclients.models.sws import TimeScheduleConstruction


term_res_url_prefix = "/student/v5/term"
logger = logging.getLogger(__name__)


def get_term_by_year_and_quarter(year, quarter):
    """
    Returns a restclients.models.sws.Term object,
    for the passed year and quarter.
    """
    url = "%s/%s,%s.json" % (term_res_url_prefix, str(year), quarter.lower())
    return _json_to_term_model(get_resource(url))


def get_current_term():
    """
    Returns a restclients.models.sws.Term object,
    for the current term.
    """
    url = "%s/current.json" % term_res_url_prefix
    term = _json_to_term_model(get_resource(url))

    # A term doesn't become "current" until 2 days before the start of
    # classes.  That's too late to be useful, so if we're after the last
    # day of grade submission window, use the next term resource.
    if datetime.now() > term.grade_submission_deadline:
        return get_next_term()

    return term


def get_next_term():
    """
    Returns a restclients.models.sws.Term object,
    for the next term.
    """
    url = "%s/next.json" % term_res_url_prefix
    return _json_to_term_model(get_resource(url))


def get_previous_term():
    """
    Returns a restclients.models.sws.Term object,
    for the previous term.
    """
    url = "%s/previous.json" % term_res_url_prefix
    return _json_to_term_model(get_resource(url))


def get_term_before(aterm):
    """
    Returns a restclients.models.sws.Term object,
    for the term before the term given.
    """
    prev_year = aterm.year
    prev_quarter = QUARTER_SEQ[QUARTER_SEQ.index(aterm.quarter) - 1]

    if prev_quarter == "autumn":
        prev_year -= 1

    return get_term_by_year_and_quarter(prev_year, prev_quarter)


def get_term_after(aterm):
    """
    Returns a restclients.models.sws.Term object,
    for the term after the term given.
    """
    next_year = aterm.year
    if aterm.quarter == "autumn":
        next_quarter = QUARTER_SEQ[0]
    else:
        next_quarter = QUARTER_SEQ[QUARTER_SEQ.index(aterm.quarter) + 1]

    if next_quarter == "winter":
        next_year += 1

    return get_term_by_year_and_quarter(next_year, next_quarter)


def get_term_by_date(date):
    """
    Returns a term for the datetime.date object given.
    """
    year = date.year

    term = None
    for quarter in ('autumn', 'summer', 'spring', 'winter'):
        term = get_term_by_year_and_quarter(year, quarter)

        if date >= term.first_day_quarter:
            break

    # If we're in a year, before the start of winter quarter, we need to go
    # to the previous year's autumn term:
    if date < term.first_day_quarter:
        term = get_term_by_year_and_quarter(year - 1, 'autumn')

    # Autumn quarter should always last through the end of the year,
    # with winter of the next year starting in January.  But this makes sure
    # we catch it if not.
    term_after = get_term_after(term)
    if term_after.first_day_quarter > date:
        return term
    else:
        return term_after

    pass

def _json_to_term_model(term_data):
    """
    Returns a term model created from the passed json data.
    param: term_data loaded json data
    """

    strptime = datetime.strptime
    day_format = "%Y-%m-%d"
    datetime_format = "%Y-%m-%dT%H:%M:%S"

    term = TermModel()
    term.year = term_data["Year"]
    term.quarter = term_data["Quarter"]

    term.last_day_add = parse_sws_date(term_data["LastAddDay"])

    term.first_day_quarter = parse_sws_date(term_data["FirstDay"])

    term.last_day_instruction = parse_sws_date(term_data["LastDayOfClasses"])

    term.last_day_drop = parse_sws_date(term_data["LastDropDay"])

    term.census_day = parse_sws_date(term_data["CensusDay"])

    if term_data["ATermLastDay"] is not None:
        term.aterm_last_date = parse_sws_date(term_data["ATermLastDay"])

    if term_data["BTermFirstDay"] is not None:
        term.bterm_first_date = parse_sws_date(term_data["BTermFirstDay"])

    if term_data["LastAddDayATerm"] is not None:
        term.aterm_last_day_add = parse_sws_date(term_data["LastAddDayATerm"])

    if term_data["LastAddDayBTerm"] is not None:
        term.bterm_last_day_add = parse_sws_date(term_data["LastAddDayBTerm"])

    term.last_final_exam_date = parse_sws_date(term_data["LastFinalExamDay"])

    term.grading_period_open = strptime(
        term_data["GradingPeriodOpen"], datetime_format)

    if term_data["GradingPeriodOpenATerm"] is not None:
        term.aterm_grading_period_open = strptime(
            term_data["GradingPeriodOpenATerm"], datetime_format)

    term.grading_period_close = strptime(
        term_data["GradingPeriodClose"], datetime_format)

    term.grade_submission_deadline = strptime(
        term_data["GradeSubmissionDeadline"], datetime_format)

    term.registration_services_start = parse_sws_date(term_data["RegistrationServicesStart"])

    term.registration_period1_start = parse_sws_date(term_data["RegistrationPeriods"][0]["StartDate"])
    term.registration_period1_end = parse_sws_date(term_data["RegistrationPeriods"][0]["EndDate"])

    term.registration_period2_start = parse_sws_date(term_data["RegistrationPeriods"][1]["StartDate"])
    term.registration_period2_end = parse_sws_date(term_data["RegistrationPeriods"][1]["EndDate"])

    term.registration_period3_start = parse_sws_date(term_data["RegistrationPeriods"][2]["StartDate"])
    term.registration_period3_end = parse_sws_date(term_data["RegistrationPeriods"][2]["EndDate"])

    term.time_schedule_construction = []
    for campus in term_data["TimeScheduleConstruction"]:
        tsc = TimeScheduleConstruction(
            campus=campus.lower(),
            is_on=(term_data["TimeScheduleConstruction"][campus] is True))
        term.time_schedule_construction.append(tsc)

    term.clean_fields()
    return term
