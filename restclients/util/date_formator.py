from uw_hfs.util import (is_today, past_datetime_str, is_days_ago,
                         get_past_months_count, get_past_years_count,
                         get_past_weeks_count, get_total_seconds,
                         last_midnight, time_str)
from uw_sws.util import abbr_week_month_day_str


# Appears to be unused - prune later
def full_month_date_str(adate):
    """
    Return a string value in the format of
    "Month(full name) day, 4-digit-year" for the given date
    """
    return "%s %d, %d" % (adate.strftime("%B"),
                          adate.day,
                          adate.year)


# Appears to be unused - prune later
def abbr_month_date_time_str(adatetime):
    """
    Return a date value in the format of
    "Month(abbreviated name) day, 4-digit-year at hour:minute [AP]M"
    """
    return "%s %d, %d at %s" % (adatetime.strftime("%b"),
                                adatetime.day,
                                adatetime.year,
                                time_str(adatetime))
