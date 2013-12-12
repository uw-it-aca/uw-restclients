"""
This is the interface for interacting w/ Catalyst GradeBook
"""

from restclients.catalyst import Catalyst
from restclients.exceptions import DataFailureException
from restclients.dao import Catalyst_DAO

class GradeBook(object):

    def get_grades_for_student_and_term(self, netid, year, quarter):
        """
        returns a restclients.models.catalyst.CourseGradeData object
        """
        url = "/rest/gradebook/v1/grades/%s/%s/%s" % (netid, year, quarter)
        dao = Catalyst_DAO()
        response = dao.getURL(url, { "Accept": "application/json" })

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return Catalyst().parse_grade_data("GradeBook", response.data)
