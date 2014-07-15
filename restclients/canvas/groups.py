from restclients.canvas import Canvas

class Groups(Canvas):
    def get_groups_for_sis_course_id(self, sis_course_id):
        url = "/api/v1/courses/sis_course_id:%s/groups" % sis_course_id
        data = self._get_resource(url)

        raise Exception("Not implemented")
