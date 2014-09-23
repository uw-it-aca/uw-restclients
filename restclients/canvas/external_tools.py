from restclients.canvas import Canvas
#from restclients.models.canvas import ExternalTool


class ExternalTools(Canvas):
    def get_external_tools_in_account(self, account_id):
        """
        Return external tools for the passed canvas account id.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        url = "/api/v1/accounts/%s/external_tools" % account_id

        external_tools = []
        for data in self._get_resource(url):
            external_tools.append(self._external_tool_from_json(data))
        return external_tools

    def get_external_tools_in_account_by_sis_id(self, sis_id):
        """
        Return external tools for given account sis id.
        """
        return self.get_external_tools_in_account(self._sis_id(sis_id,
                                                               "account"))

    def get_external_tools_in_course(self, course_id):
        """
        Return external tools for the passed canvas course id.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        url = "/api/v1/courses/%s/external_tools" % course_id

        external_tools = []
        for data in self._get_resource(url):
            external_tools.append(self._external_tool_from_json(data))
        return external_tools

    def get_external_tools_in_course_by_sis_id(self, sis_id):
        """
        Return external tools for given course sis id.
        """
        return self.get_external_tools_in_course(self._sis_id(sis_id,
                                                              "course"))

    def _external_tool_from_json(self, data):
        return data
