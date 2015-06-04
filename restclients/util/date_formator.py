import re
from datetime import datetime, timedelta


def full_month_date_str(adate):
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


def abbr_month_date_time_str(adatetime):
    """
    Return a date value in the format of
    "Month(abbreviated name) day, 4-digit-year at hour:minute [AP]M"
    """
    return "%s %d, %d at %s" % (adatetime.strftime("%b"),
                                adatetime.day,
                                adatetime.year,
                                time_str(adatetime))


def abbr_week_month_day_str(adatetime):
    """
    Return a string consists of abbreviated weekday, abbreviated month,
    date with no leading zero, and without a year
    e.g., Mon, Jun 2. No punctuation is shown for
    the abbreviated weekday and month.
    """
    return "%s %d" % (adatetime.strftime("%a, %b"), adatetime.day)


def past_datetime_str(adatetime):
    """
    For adatetime is since 12:00AM, return: "Today at H:MM [A]PM"
    For adatetime is between 12:00AM and 11:59PM on yesterday:
                                    "Yesterday at 6:23 PM"
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

    if last_midnight() - adatetime <= timedelta(days=7):
        for day in xrange(1, 8):
            if is_days_ago(adatetime, day):
                if day == 1:
                    return "yesterday at %s" % time_str(adatetime)
                if day == 7:
                    return "1 week ago"
                return "%d days ago" % day

    if last_midnight() - adatetime <= timedelta(days=28):
        week = get_past_weeks_count(adatetime)
        if week == 1:
            return "over %d week ago" % week
        else:
            return "over %d weeks ago" % week

    if last_midnight() - adatetime <= timedelta(days=365):
        month = get_past_months_count(adatetime)
        if month == 1:
            return "over %d month ago" % month
        else:
            return "over %d months ago" % month

    year = get_past_years_count(adatetime)
    if year == 1:
        return "over %d year ago" % year
    else:
        return "over %d years ago" % year


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
    return start_time <= adatetime <= end_time


def get_past_weeks_count(adatetime):
    """
    Return the number of weeks that the adatetime is over in the past
    7 days are counted as one week.
    """
    duration = last_midnight() - adatetime
    return get_total_seconds(duration) // get_total_seconds(timedelta(7))


def get_past_months_count(adatetime):
    """
    Return the number of months that the adatetime is over in the past
    28 days are counted as one month.
    """
    duration = last_midnight() - adatetime
    return get_total_seconds(duration) // get_total_seconds(timedelta(28))


def get_past_years_count(adatetime):
    """
    Return the number of years that the adatetime is over in the past
    365 days are counted as one year.
    """
    duration = last_midnight() - adatetime
    return get_total_seconds(duration) // get_total_seconds(timedelta(365))


def get_total_seconds(time_delta):
    """
    Returns the total number of seconds in a passed timedelta
    """
    return (time_delta.microseconds +
            (time_delta.seconds + time_delta.days * 24 * 3600) * 10**6) / 10**6
