from rest_base import RestBase
from django.conf import settings
from lxml import etree


class InvalidGroupID(Exception):
    """Exception for invalid group id."""
    pass


class GWSClient(RestBase):
    """
    REST Client for retrieving group data from the UW Group Service.
    Configuration parameters for this client are:

    :GWS_URL:
        The absolute URL of the GWS host. URL must include scheme and port (if
        not 80). Ex. https://https://iam-ws.u.washington.edu:443

    :GWS_CERT:
        Path of a certficate file. Required for access to eval and production
        GWS. Ex. /usr/local/ssl/foo.cert

    :GWS_KEY:
        Path of a public key file. Required for access to eval and production
        GWS. Ex. /usr/local/ssl/foo.key

    :GWS_TIMEOUT:
        Socket timeout for each individual connection, can be a float. None
        disables timeout.

    :GWS_LOGNAME:
        Name to use for GWS client logging, defaults to module name

    """
    URL_BASE = '/group_sws/v2'
    QTRS = {'win': 'winter', 'spr': 'spring', 'sum': 'summer', 'aut': 'autumn'}

    def __init__(self):
        self._cfg = {
            'url': settings.GWS_URL,
            'cert': settings.GWS_CERT,
            'key': settings.GWS_KEY,
            'timeout': settings.GWS_TIMEOUT,
            'logname': settings.GWS_LOGNAME
        }
        RestBase.__init__(self)

    def get_xml(self, url, fields=None, headers={}):
        headers.update({'Accept': 'text/xhtml'})
        r = self.GET(url, fields, headers)
        return etree.fromstring(r.data)

    def get_group_by_id(self, group_id):
        """
        Returns group data for the group identified by the passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        root = self.get_xml(self.URL_BASE + '/group/' + group_id)
        if root is None:
            return

        group = {}
        group['reg_id'] = root.find('.//*[@class="regid"]').text
        group['name'] = root.find('.//*[@class="name"]').text
        group['title'] = root.find('.//*[@class="title"]').text
        group['description'] = root.find('.//*[@class="description"]').text

        course_curr = root.find('.//*[@class="course_curr"]')
        if course_curr is not None:
            group['curriculum_abbreviation'] = course_curr.text.upper()
            group['course_number'] = root.find('.//*[@class="course_no"]').text
            group['year'] = root.find('.//*[@class="course_year"]').text
            group['quarter'] = self.QTRS[root.find('.//*[@class="course_qtr"]').text]
            group['section_id'] = root.find('.//*[@class="course_sect"]').text.upper()
            group['sln'] = root.find('.//*[@class="course_sln"]').text

            group['instructors'] = []
            instructors = root.findall('.//*[@class="course_instructors"]' +
                                       '/*[@class="course_instructor"]')
            for instructor in instructors:
                group['instructors'].append(instructor.text)

        return group

    def group_search(self, opts={}):
        """
        Returns a list of group data for UW groups. Valid parameters for
        searching are:

        :param name:
            The entire group ID, or a portion of it.

        :param stem:
            The leading part of a group ID.
            Ex. u_netid

        :param member:
            The UW NetID of a member of returned groups.

        :param owner:
            The UW NetID of an administrator of returned groups.

        :param type:
            Specifies whether the name is itself a member or administrator, not
            in a subgroup. Default is 'direct'.

        :param scope:
            Returns only the next level of groups and stems from the search.
            Default is 'one'.

        """
        fields = {
            'name': '',
            'stem': '',
            'member': '',
            'owner': '',
            'type': 'direct',
            'scope': 'one'
        }

        for field in fields:
            if field in opts:
                fields[field] = opts[field]

        root = self.get_xml(self.URL_BASE + '/search', fields)
        if root is None:
            return

        groups = []
        group_elements = root.findall('.//*[@class="groupreference"]')

        for element in group_elements:
            name = element.find('.//*[@class="name"]')
            groups.append({
                'name': name.text,
                'href': name.get('href'),
                'reg_id': element.find('.//*[@class="regid"]').text,
                'title': element.find('.//*[@class="title"]').text,
                'description': element.find('.//*[@class="description"]').text
            })

        return groups

    def get_members(self, group_id):
        """
        Returns a list of group member data for the group identified by the
        passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        root = self.get_xml(self.URL_BASE + '/group/' + group_id + '/member')
        if root is None:
            return

        members = []
        member_elements = root.findall('.//*[@class="members"]' +
                                       '//*[@class="member"]')
        for member in member_elements:
            members.append({
                'name': member.text,
                'type': member.get('type'),
                'href': member.get('href')
            })

        return members

    def get_effective_members(self, group_id):
        """
        Returns a list of effective group member data for the group identified
        by the passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        root = self.get_xml(self.URL_BASE + '/group/' + group_id +
                            '/effective_member')
        if root is None:
            return

        members = []
        member_elements = root.findall('.//*[@class="members"]' +
                                       '//*[@class="effective_member"]')
        for member in member_elements:
            members.append({
                'name': member.text,
                'type': member.get('type'),
                'href': member.get('href')
            })

        return members

    def put_group(self):
        raise Exception("Not implemented")

    def put_members(self):
        raise Exception("Not implemented")

    def delete_group(self, group_id):
        raise Exception("Not implemented")

    def _is_valid_group_id(self, group_id):
        if not group_id:
            return False

        return True
