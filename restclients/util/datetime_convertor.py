from datetime import date, datetime, timedelta


def convert_to_begin_of_day(a_date):
    """
    @return the naive datetime object of the beginning of day
    for the give date or datetime object
    """
    return datetime(a_date.year, a_date.month, a_date.day, 0, 0, 0)


def convert_to_end_of_day(a_date):
    """
    @return the naive datetime object of the end of day
    for the give date or datetime object
    """
    return convert_to_begin_of_day(a_date) + timedelta(days=1)
