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
