from restclients.canvas import Canvas
from restclients.models.canvas import Assignment
import dateutil.parser


class Assignments(Canvas):
    def get_assignments(self, course_id):
        """
        List assignments for a given course

        https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
        """
        url = "/api/v1/courses/%s/assignments" % course_id
        data = self._get_resource(url)
        assignments = []
        for assignment in data:
            assignment = self._assignment_from_json(assignment)
            assignments.append(assignment)
        return assignments
        
    def get_assignments_by_sis_id(self, sis_id):
        """
        List assignments for a given course by sid_id

        https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
        """
        return self.get_assignments(self._sis_id(sis_id, "course"))

    def _assignment_from_json(self, data):
        assignment = Assignment()
        assignment.assignment_id = data['id']
        if data['due_at']:
            assignment.due_at = dateutil.parser.parse(data['due_at'])
        assignment.points_possible = data['points_possible']
        assignment.position = data['position']
        assignment.name = data['name']
        assignment.muted = data['muted']
        assignment.html_url = data['html_url']
        return assignment

    
