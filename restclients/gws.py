"""
This is the interface for interacting with the Group Web Service.
"""

from django.template import Context, loader
from restclients.dao import GWS_DAO
from restclients.exceptions import InvalidGroupID
from restclients.exceptions import DataFailureException
from restclients.models import Group, CourseGroup, GroupUser, GroupMember
from lxml import etree


class GWS(object):
    """
    The GWS object has methods for getting group information.
    """
    QTRS = {'win': 'winter', 'spr': 'spring', 'sum': 'summer', 'aut': 'autumn'}


    def __init__(self, config={}):
        self.actas = config['actas'] if 'actas' in config else None

    def get_group_by_id(self, group_id):
        """
        Returns group data for the group identified by the passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s" % group_id
        response = dao.getURL(url, self._headers({"Accept": "text/xhtml"}))

        if response.status == 404:
            return

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._group_from_xhtml(response.data)

    def create_group(self, group):
        """
        Creates the passed group.
        """
        body = self._xhtml_from_group(group)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s" % group.name
        response = dao.putURL(url,
                              self._headers({"Accept": "text/xhtml",
                                             "Content-Type": "text/xhtml"}),
                              body)

        if response.status != 201:
            raise DataFailureException(url, response.status, response.data)

        return self._group_from_xhtml(response.data)

    def update_group(self, group):
        """
        Updates the passed group.
        """
        body = self._xhtml_from_group(group)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s" % group.name
        response = dao.putURL(url,
                              self._headers({"Accept": "text/xhtml",
                                             "Content-Type": "text/xhtml",
                                             "If-Match": "*"}),
                              body)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._group_from_xhtml(response.data)

    def delete_group(self, group):
        """
        Deletes the passed group.
        """
        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s" % group.name
        response = dao.deleteURL(url, self._headers())

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return True

    def get_members(self, group_id):
        """
        Returns a list of GroupMember models for the group identified by the
        passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s/member" % group_id
        response = dao.getURL(url, self._headers({"Accept": "text/xhtml"}))

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._members_from_xhtml(response.data)

    def update_members(self, group_id, members):
        """
        Updates the membership of the group represented by the passed group id.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        body = self._xhtml_from_members(group_id, members)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s/member" % group_id
        response = dao.putURL(url,
                              self._headers({"Content-Type": "text/xhtml",
                                             "If-Match": "*"}),
                              body)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return members

    def get_effective_members(self, group_id):
        """
        Returns a list of effective GroupMember models for the group identified
        by the passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s/effective_member" % group_id
        response = dao.getURL(url, self._headers({"Accept": "text/xhtml"}))

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._effective_members_from_xhtml(response.data)

    def is_effective_member(self, group_id, netid):
        """
        Returns True if the netid is in the group, False otherwise.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s/effective_member/%s" % (group_id, netid)
        response = dao.getURL(url, self._headers({"Accept": "text/xhtml"}))

        if response.status == 404:
            return False
        elif response.status == 200:
            return True
        else:
            raise DataFailureException(url, response.status, response.data)

    def _group_from_xhtml(self, data):
        root = etree.fromstring(data)
        course_curr = root.find('.//*[@class="course_curr"]')
        if course_curr is not None:
            group = CourseGroup()
            group.curriculum_abbreviation = course_curr.text.upper()
            group.course_number = root.find('.//*[@class="course_no"]').text
            group.year = root.find('.//*[@class="course_year"]').text
            group.quarter = self.QTRS[root.find('.//*[@class="course_qtr"]').text]
            group.section_id = root.find('.//*[@class="course_sect"]').text.upper()
            group.sln = root.find('.//*[@class="course_sln"]').text

            group.instructors = []
            instructors = root.findall('.//*[@class="course_instructors"]' +
                                       '/*[@class="course_instructor"]')
            for instructor in instructors:
                group.instructors.append(instructor.text)
        else:
            group = Group()

        group.uwregid = root.find('.//*[@class="regid"]').text
        group.name = root.find('.//*[@class="name"]').text
        group.title = root.find('.//*[@class="title"]').text
        group.description = root.find('.//*[@class="description"]').text
        group.contact = root.find('.//*[@class="contact"]').text
        group.authnfactor = root.find('.//*[@class="authnfactor"]').text
        group.classification = root.find('.//*[@class="classification"]').text
        group.emailenabled = root.find('.//*[@class="emailenabled"]').text
        group.dependson = root.find('.//*[@class="dependson"]').text
        group.publishemail = root.find('.//*[@class="publishemail"]').text
        group.reporttoorig = root.find('.//*[@class="reporttoorig"]').text

        group.admins = []
        for user in root.findall('.//*[@class="admins"]/*[@class="admin"]'):
            group.admins.append(GroupUser(name=user.text,
                                          user_type=user.get("type")))

        group.updaters = []
        for user in root.findall('.//*[@class="updaters"]/*[@class="updater"]'):
            group.updaters.append(GroupUser(name=user.text,
                                            user_type=user.get("type")))

        group.creators = []
        for user in root.findall('.//*[@class="creators"]/*[@class="creator"]'):
            group.creators.append(GroupUser(name=user.text,
                                            user_type=user.get("type")))

        group.readers = []
        for user in root.findall('.//*[@class="readers"]/*[@class="reader"]'):
            group.readers.append(GroupUser(name=user.text,
                                           user_type=user.get("type")))

        group.viewers = []
        for user in root.findall('.//*[@class="viewers"]/*[@class="viewer"]'):
            group.viewers.append(GroupUser(name=user.text,
                                           user_type=user.get("type")))
        return group

    def _xhtml_from_group(self, group):
        template = loader.get_template("gws/group.xhtml")
        context = Context({"group": group})
        return template.render(context)

    def _effective_members_from_xhtml(self, data):
        root = etree.fromstring(data)
        member_elements = root.findall('.//*[@class="members"]' +
                                       '//*[@class="effective_member"]')

        members = []
        for member in member_elements:
            members.append(GroupMember(name=member.text,
                                       member_type=member.get("type"),
                                       href=member.get("href")))

        return members

    def _members_from_xhtml(self, data):
        root = etree.fromstring(data)
        member_elements = root.findall('.//*[@class="members"]' +
                                       '//*[@class="member"]')

        members = []
        for member in member_elements:
            members.append(GroupMember(name=member.text,
                                       member_type=member.get("type"),
                                       href=member.get("href")))

        return members

    def _xhtml_from_members(self, group_id, members):
        template = loader.get_template("gws/members.xhtml")
        context = Context({"group_id": group_id, "members": members})
        return template.render(context)

    def _is_valid_group_id(self, group_id):
        if not group_id:
            return False

        return True

    def _headers(self, headers):
        if self.actas:
            headers = self._add_header(headers, "X-UW-Act-as", self.actas)

        return headers

    def _add_header(headers, header, value):
        if not headers:
            return { header: value }

        headers[header] = value
        return headers
