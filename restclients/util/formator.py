import re
from datetime import date, datetime, timedelta


def standard_date_str(adate):
    """
    Return a string value in the format of 
    "Month(full name) day, 4-digit-year" for the given date
    """
    return "%s %d, %d" % (adate.strftime("%B"),
                          adate.day,
                          adate.year)


def standard_datetime_str(adatetime):
    """
    Return a date value in the format of 
    "Month(full name) day, 4-digit-year at hour:minute [ap].m."
    """
    time_value = re.sub(r'^0', '', adatetime.strftime("%I:%M %p"))
    time_value = re.sub(r'AM$', 'a.m.', time_value)
    time_value = re.sub(r'PM$', 'p.m.', time_value)
    return "%s %d, %d at %s" % (adatetime.strftime("%B"),
                                adatetime.day,
                                adatetime.year,
                                time_value)


def truncate_time_str(adatetime, older_than_days_to_omit_time=0):
    """
    Return a string of formated date value.
    If adatetime is older than older_than_days_to_omit_time days,
    the time portion would be omitted.
    The default is to omit nothing.
    """
    if older_than_days_to_omit_time > 0 and (datetime.now() - adatetime) > timedelta(days=older_than_days_to_omit_time):
        return standard_date_str(adatetime.date())
    else:
        return standard_datetime_str(adatetime)


