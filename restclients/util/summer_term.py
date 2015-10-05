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
