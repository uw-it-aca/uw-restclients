import re
from datetime import datetime, timedelta


def month_full_name_date_str(adate):
    """
    Return a string value in the format of 
    "Month(full name) day, 4-digit-year" for the given date
    """
    return "%s %d, %d" % (adate.strftime("%B"),
                          adate.day,
                          adate.year)


def time_str(adatetime):
    """
    Return the format of "at hour:minute [AP]M",
    where the hour doesn't have a leading zero.
    """
    return re.sub(r'^0', '', adatetime.strftime("%I:%M %p"))


def month_full_name_datetime_str(adatetime):
    """
    Return a date value in the format of 
    "Month(full name) day, 4-digit-year at hour:minute [AP]M"
    """
    return "%s %d, %d at %s" % (adatetime.strftime("%B"),
                                adatetime.day,
                                adatetime.year,
                                time_str(adatetime))


def past_datetime_str(adatetime):
    """
    For adatetime is since 12:00AM, return: "Today at H:MM [A]PM"
    For adatetime is between 12:00AM and 11:59PM on yesterday: "Yesterday at 6:23 PM"
    For adatetime is between 2 and 6 days ago: "[2-6] days ago"
    For adatetime is 7 days ago: "1 week ago"
    For adatetime is 8-14 days ago: "Over 1 week ago"
    For adatetime is 15-21 days ago: "Over 2 weeks ago"
    For adatetime is 22-28 days ago: "Over 3 weeks ago"
    For adatetime is 29-56 days ago: "Over 1 month ago"
    For adatetime is 57-84 days ago: "Over 2 months ago"
    For adatetime is 85-112 days ago: "Over 3 months ago"
    and so on, in increments of 28 days, until T-365, 
    at which point: "Over 1 year ago", 
    then after another 365 days "Over 2 years ago", etc
    """
    if is_today(adatetime):
        return "today at %s" % time_str(adatetime)

    if last_midnight() - adatetime < timedelta(days=8):
        for day in xrange (1,8):
            if is_days_ago(adatetime, day):
                if day == 1:
                    return "yesterday at %s" % time_str(adatetime)
                if day == 7:
                    return "1 week ago"
                return "%d days ago" % day

    if last_midnight() - adatetime < timedelta(days=29):
        for week in xrange (1,4):
            if is_over_weeks_ago(adatetime, week):
                if week == 1:
                    return "over %d week ago" % week
                else:
                    return "over %d weeks ago" % week

    if last_midnight() - adatetime < timedelta(days=366):
        for month in xrange (1,12):
            if is_over_months_ago(adatetime, month):
                if month == 1:
                    return "over %d month ago" % month
                else:
                    return "over %d months ago" % month

    for year in xrange (1,100):
        if is_over_years_ago(adatetime, year):
            if year == 1:
                return "over %d year ago" % year
            else:
                return "over %d years ago" % year

    return "over a hundred years ago"
    

def last_midnight():
    """
    return a datetime of last mid-night
    """
    now = datetime.now()
    return datetime(now.year, now.month, now.day)
    

def is_today(adatetime):
    """
    Return true if the adatetime is since this morning 12:00AM
    """
    return last_midnight() <= adatetime


def is_days_ago(adatetime, days):
    """
    :param days: a positive integer.
    Return true if the adatetime is on the specified days ago
    """
    if days == 1:
        end_time = last_midnight()
        start_time = end_time - timedelta(days=1)
    else:
        start_time = last_midnight() - timedelta(days=days)
        end_time = start_time + timedelta(days=1)
    return start_time <= adatetime and adatetime <= end_time


def is_over_weeks_ago(adatetime, weeks):
    """
    :param weeks: a positive integer.
    Return true if the adatetime is over (more than) the specified weeks ago
    """
    end_time = last_midnight() - timedelta(weeks=weeks)
    start_time = end_time - timedelta(weeks=1)
    return start_time <= adatetime and adatetime <= end_time


def is_over_months_ago(adatetime, months):
    """
    :param months: a positive integer.
    28 days are counted as one month.
    Return true if the adatetime is in the specified months ago
    """
    end_time = last_midnight() - timedelta(weeks=(months*4))
    start_time = end_time - timedelta(weeks=4)
    return start_time <= adatetime and adatetime <= end_time


def is_over_years_ago(adatetime, years):
    """
    :param years: a positive integer.
    Return true if the adatetime is in the specified years ago
    """
    end_time = last_midnight() - timedelta(days=(years*365))
    start_time = end_time - timedelta(days=365)
    return start_time <= adatetime and adatetime <= end_time
