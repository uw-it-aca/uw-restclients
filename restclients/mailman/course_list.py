"""
Interface for interacting with the mailman uwnetid resource
"""
import re
from restclients.mailman.basic_list import exists


def _get_list_name_curr_abbr(curriculum_abbr):
    """
    @return mailman specific curriculum abbr
    """
    curr_abbr = curriculum_abbr.lower()
    if re.match(r'^b [&\w]+', curr_abbr):
        return re.sub(r'^b ', 'b', curr_abbr)
    elif re.match(r'^t [&\w]+', curr_abbr):
        return re.sub(r'^t ', 't', curr_abbr)
    else:
        return curr_abbr


def get_course_list_name(curriculum_abbr, course_number, section_id,
                         quarter, year):
    """
    Return the list address of UW course email list
    """
    return "%s%s%s_%s%s" % (
        _get_list_name_curr_abbr(curriculum_abbr),
        course_number,
        section_id.lower(),
        quarter.lower()[:2],
        str(year)[-2:]
        )


def exists_course_list(curriculum_abbr, course_number, section_id,
                       quarter, year):
    """
    Return True if the corresponding mailman list exists for the course
    """
    return exists(get_course_list_name(curriculum_abbr, course_number,
                                       section_id, quarter, year))


def get_section_list_name(section):
    """
    Return the list address of UW course section email list
    """
    return get_course_list_name(section.curriculum_abbr,
                                section.course_number,
                                section.section_id,
                                section.term.quarter,
                                section.term.year)


def exists_section_list(course_section):
    """
    Return True if the corresponding mailman list exists
    for the course section
    @param course_section a valid Section object
    """
    return exists(get_section_list_name(course_section))


def get_secondary_combined_list_name(curriculum_abbr,
                                     course_number,
                                     primary_section_id,
                                     quarter,
                                     year):
    return "multi_%s%s%s_%s%s" % (
        _get_list_name_curr_abbr(curriculum_abbr),
        course_number,
        primary_section_id.lower(),
        quarter.lower()[:2],
        str(year)[-2:]
        )


def exists_secondary_combined_list(curriculum_abbr,
                                   course_number,
                                   primary_section_id,
                                   quarter,
                                   year):
    """
    Return True if a combined mailman list exists for all
    the secondary course sections in the given quarter and year
    """
    return exists(get_secondary_combined_list_name(curriculum_abbr,
                                                   course_number,
                                                   primary_section_id,
                                                   quarter,
                                                   year))


def get_section_secondary_combined_list_name(section):
    if section.is_primary_section:
        section_id = section.section_id
    else:
        section_id = section.primary_section_id

    return get_secondary_combined_list_name(section.curriculum_abbr,
                                            section.course_number,
                                            section_id,
                                            section.term.quarter,
                                            section.term.year)


def exists_section_secondary_combined_list(course_section):
    """
    Return True if a combined mailman list exists
    for all the secondary course sections
    """
    return exists(
        get_section_secondary_combined_list_name(course_section))
