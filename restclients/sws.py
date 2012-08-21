"""
This is the interface for interacting with the Student Web Service.
"""

from restclients.dao import SWS_DAO
from restclients.models import Term
import json
import re

class SWS(object):
    """
    The SWS object has methods for getting information
    about courses, and everything related.
    """

    def get_current_term(self):
        """
        Returns a restclients.Term object, for the current term.
        """
        dao = SWS_DAO()
        url = "/student/v4/term/current.json"
        response = dao.getURL(url, {"Accept": "application/json"})

        if response.status != 200:
            raise DataFailureException(url, response.status, response.read())

        term_data = json.loads(response.data)
        term = Term()
        term.year = term_data["Year"]
        term.quarter = term_data["Quarter"]
        term.first_day_quarter = term_data["FirstDay"]
        term.last_day_instruction = term_data["LastDayOfClasses"]
        term.aterm_last_date = term_data["ATermLastDay"]
        term.bterm_first_date = term_data["BTermFirstDay"]
        term.last_final_exam_date = term_data["LastFinalExamDay"]

        return term
