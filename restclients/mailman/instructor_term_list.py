"""
Interface for interacting with the mailman uwnetid resource
"""

from restclients.mailman.basic_list import exists


def get_instructor_term_list_name(instructor_entid, year, quarter):
    """
    Return the list address of UW instructor email list for
    the given year and quarter
    """
    return "%s_%s%s" % (
        instructor_entid,
        quarter.lower()[:2],
        str(year)[-2:])


def exists_instructor_term_list(instructor_entid, year, quarter):
    """
    Return True if a combined mailman list exists for all courses
    taught by the UW instructor in the given term
    """
    return exists(get_instructor_term_list_name(instructor_entid,
                                                year, quarter))
