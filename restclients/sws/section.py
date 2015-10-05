from restclients.sws.v5.section import get_sections_by_instructor_and_term
from restclients.sws.v5.section import get_sections_by_delegate_and_term
from restclients.sws.v5.section import get_sections_by_curriculum_and_term
from restclients.sws.v5.section import get_changed_sections_by_term
from restclients.sws.v5.section import get_section_by_url
from restclients.sws.v5.section import get_section_by_label
from restclients.sws.v5.section import get_linked_sections
from restclients.sws.v5.section import get_joint_sections


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
