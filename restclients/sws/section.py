from restclients.sws.v5.section import get_sections_by_instructor_and_term
from restclients.sws.v5.section import get_sections_by_delegate_and_term
from restclients.sws.v5.section import get_sections_by_curriculum_and_term
from restclients.sws.v5.section import get_sections_by_building_and_term
from restclients.sws.v5.section import get_changed_sections_by_term
from restclients.sws.v5.section import get_section_by_url
from restclients.sws.v5.section import get_section_by_label
from restclients.sws.v5.section import get_linked_sections
from restclients.sws.v5.section import get_joint_sections
from restclients.sws.v5.section import is_valid_section_label
from restclients.models.sws import Section


def is_a_term(str):
    return str is not None and len(str) > 0 and\
        str.lower() == Section.SUMMER_A_TERM


def is_b_term(str):
    return str is not None and len(str) > 0 and\
        str.lower() == Section.SUMMER_B_TERM


def is_full_summer_term(str):
    return str is not None and len(str) > 0 and\
        str.lower() == Section.SUMMER_FULL_TERM
