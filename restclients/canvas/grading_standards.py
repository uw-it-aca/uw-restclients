from restclients.canvas import Canvas
from restclients.models.canvas import GradingStandard


class GradingStandards(Canvas):
    def create_grading_standard_for_course(self, course_id, name, grading_scheme):
        """
        Create a new grading standard for the passed course.
        
        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create
        """
        url = "/api/v1/courses/%s/grading_standards" % course_id
        body = {"title": name,
                "grading_scheme": grading_scheme}

        data = self._post_resource(url, body)

        return self._grading_standard_from_json(data)

    def _grading_standard_from_json(self, data):
        grading_standard = GradingStandard()
        grading_standard.grading_standard_id = data["id"]
        grading_standard.title = data["title"]
        grading_standard.context_type = data["context_type"]
        grading_standard.context_id = data["context_id"]
        grading_standard.grading_scheme = data["grading_scheme"]
        return grading_standard
