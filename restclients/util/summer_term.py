def is_a_term(str):
    return str is not None and len(str) > 0 and str.lower() == "a-term"


def is_b_term(str):
    return str is not None and len(str) > 0 and str.lower() == "b-term"


def is_full_summer_term(str):
    return str is not None and len(str) > 0 and str.lower() == "full-term"
