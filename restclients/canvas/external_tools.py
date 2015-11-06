from restclients.canvas import Canvas


class ExternalToolsException(Exception):
    pass


class ExternalTools(Canvas):
    def get_external_tools_in_account(self, account_id, params={}):
        """
        Return external tools for the passed canvas account id.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        url = "/api/v1/accounts/%s/external_tools" % account_id

        external_tools = []
        for data in self._get_paged_resource(url, params=params):
            external_tools.append(self._external_tool_from_json(data))
        return external_tools

    def get_external_tools_in_account_by_sis_id(self, sis_id):
        """
        Return external tools for given account sis id.
        """
        return self.get_external_tools_in_account(self._sis_id(sis_id,
                                                               "account"))

    def get_external_tools_in_course(self, course_id, params={}):
        """
        Return external tools for the passed canvas course id.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        url = "/api/v1/courses/%s/external_tools" % course_id

        external_tools = []
        for data in self._get_paged_resource(url, params=params):
            external_tools.append(self._external_tool_from_json(data))
        return external_tools

    def get_external_tools_in_course_by_sis_id(self, sis_id):
        """
        Return external tools for given course sis id.
        """
        return self.get_external_tools_in_course(self._sis_id(sis_id,
                                                              "course"))

    def add_external_tool_to_course(self, course_id, **kwargs):
        return self._add_external_tool('courses', course_id, **kwargs)

    def add_external_tool_to_course_by_sis_id(self, sis_id, **kwargs):
        return self._add_external_tool('courses',
                                       self._sis_id(sis_id, "course"),
                                       **kwargs)

    def add_external_tool_to_account(self, account_id, **kwargs):
        return self._add_external_tool('accounts', account_id, **kwargs)

    def add_external_tool_to_account_by_sis_id(self, sis_id, **kwargs):
        return self._add_external_tool('accounts',
                                       self._sis_id(sis_id, "account"),
                                       **kwargs)

    def _add_external_tool(self, type, id, **kwargs):
        """
        Add the given external tool to the specified course or account

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create
        """
        name = kwargs.get('name'),
        privacy_level = kwargs.get('privacy_level')
        consumer_key = kwargs.get('consumer_key')
        shared_secret = kwargs.get('shared_secret')
        if not (name and privacy_level and consumer_key and shared_secret):
            raise ExternalToolsException("missing required external tool parameter")

        url = "/api/v1/%s/%s/external_tools" % (type, id)
        body = {
            "name": kwargs.get('name'),
            "privacy_level": kwargs.get('privacy_level'),
            "consumer_key": kwargs.get('consumer_key'),
            "shared_secret": kwargs.get('shared_secret'),
        }

        if kwargs.get('config_xml'):
            body['config_type'] = 'by_xml'
            body['config_xml'] = kwargs.get('config_xml')
        elif kwargs.get('config_url'):
            body['config_type'] = 'by_url'
            body['config_url'] = kwargs.get('config_url')
        else:
            params = ['description', 'url', 'domain', 'icon_url', 'text',
                      'non_selectable', 'custom_fields', 'account_navigation',
                      'user_navigation', 'course_navigation', 'editor_button',
                      'resource_selection']

            for param in params:
                if param in kwargs:
                    body[param] = kwargs.get(param)

        data = self._post_resource(url, body)
        return self._external_tool_from_json(data)

    def _external_tool_from_json(self, data):
        return data

    def _get_sessionless_launch_url(self, tool_id, context, context_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        url = "/api/v1/%ss/%s/external_tools/sessionless_launch" % (context, context_id)
        params = {
            "id": tool_id
        }

        return self._get_resource(url, params)

    def get_sessionless_launch_url_from_account(self, tool_id, account_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self._get_sessionless_launch_url(tool_id, "account", account_id)

    def get_sessionless_launch_url_from_account_sis_id(self, tool_id, account_sis_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self.get_sessionless_launch_url_from_account(
            tool_id, self._sis_id(account_sis_id, "account"))

    def get_sessionless_launch_url_from_course(self, tool_id, course_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self._get_sessionless_launch_url(tool_id, "course", course_id)

    def get_sessionless_launch_url_from_course_sis_id(self, tool_id, course_sis_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self.get_sessionless_launch_url_from_course(
            tool_id, self._sis_id(course_sis_id, "course"))
