from restclients.canvas import Canvas
from restclients.dao import Canvas_DAO
from restclients.canvas.users import Users
from restclients.models.canvas import Section
from restclients.exceptions import DataFailureException
import json


class Sections(Canvas):
    def get_section(self, section_id, params={}):
        """
        Return section resource for given canvas section id.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.show
        """
        url = "/api/v1/sections/%s%s" % (section_id, self._params(params))
        return self._section_from_json(self._get_resource(url))

    def get_section_by_sis_id(self, sis_section_id, params={}):
        """
        Return section resource for given sis id.
        """
        return self.get_section(
            self._sis_id(sis_section_id, sis_field="section"), params)

    def get_sections_in_course(self, course_id, params={}):
        """
        Return list of sections for the passed course ID.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.index
        """
        params = self._pagination(params)
        url = "/api/v1/courses/%s/sections%s" % (course_id, self._params(params))

        sections = []
        for data in self._get_resource(url):
            sections.append(self._section_from_json(data))

        return sections

    def get_sections_in_course_by_sis_id(self, sis_course_id, params={}):
        """
        Return list of sections for the passed course SIS ID.
        """
        return self.get_sections_in_course(
            self._sis_id(sis_course_id, sis_field="course"), params)

    def get_sections_with_students_in_course(self, course_id, params={}):
        """
        Return list of sections including students for the passed course ID.
        """
        if "include" in params and params["include"] is not None:
            includes = params["include"].split(",")
            if "student" not in includes:
                params["include"] = ",".join(includes.append("students"))
        else:
            params["include"] = "students"

        return self.get_sections_in_course(course_id, params)

    def get_sections_with_students_in_course_by_sis_id(self, sis_course_id,
                                                       params={}):
        """
        Return list of sections including students for the passed sis ID.
        """
        return self.get_sections_with_students_in_course(
            self._sis_id(sis_course_id, sis_field="course"), params)

    def create_section(self, course_id, name, sis_section_id):
        """
        Create a canvas section in the given course id.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.create
        """
        url = "/api/v1/courses/%s/sections" % course_id
        body = json.dumps({"course_section": {"name": name,
                                              "sis_section_id": sis_section_id}})

        dao = Canvas_DAO()
        response = dao.postURL(url, {"Content-Type": "application/json"}, body)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return self._section_from_json(json.loads(response.data))

    def _section_from_json(self, data):
        section = Section()
        section.section_id = data["id"]
        section.sis_section_id = data["sis_section_id"] if "sis_section_id" in data else None
        section.name = data["name"]
        section.course_id = data["course_id"]
        section.nonxlist_course_id = data["nonxlist_course_id"] if "nonxlist_course_id" in data else None

        if "students" in data:
            users = Users()
            section.students = []
            for student_data in data["students"]:
                user = users._user_from_json(data)
                section.students.append(user)

        return section
