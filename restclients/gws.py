"""
This is the interface for interacting with the Group Web Service.
"""

from django.template import Context, loader
from restclients.dao import GWS_DAO
from restclients.exceptions import InvalidGroupID
from restclients.exceptions import DataFailureException
from restclients.models import Group, CourseGroup, GroupMember
from lxml import etree


class GWS(object):
    """
    The GWS object has methods for getting group information.
    """
    QTRS = {'win': 'winter', 'spr': 'spring', 'sum': 'summer', 'aut': 'autumn'}

    def get_group_by_id(self, group_id):
        """
        Returns group data for the group identified by the passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s" % group_id
        response = dao.getURL(url, {"Accept": "text/xhtml"})

        if response.status == 404:
            return

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._group_from_xhtml(response.data)

    def update_group(self, group):
        """
        Updates the passed group.
        """
        body = self._xhtml_from_group(group)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s" % group.name
        response = dao.putURL(url, {"Accept": "text/xhtml",
                                    "Content-Type": "text/xml",
                                    "If-Match": "*"}, body)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return self._group_from_xhtml(response.data)

    def delete_group(self, group):
        """
        Deletes the passed group.
        """
        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s" % group.name
        response = dao.deleteURL(url, None)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return True

    def get_effective_members(self, group_id):
        """
        Returns a list of effective group member data for the group identified
        by the passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s/effective_member" % group_id
        response = dao.getURL(url, {"Accept": "text/xhtml"})

        if response.status == 404:
            return

        root = etree.fromstring(response.data)

        member_elements = root.findall('.//*[@class="members"]' +
                                       '//*[@class="effective_member"]')

        members = []
        for member in member_elements:
            members.append(GroupMember(name=member.text,
                                       member_type=member.get("type"),
                                       href=member.get("href")))

        return members

    def is_effective_member(self, group_id, netid):
        """
        Returns True if the netid is in the group, False otherwise.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/%s/effective_member/%s" % (group_id, netid)
        response = dao.getURL(url, {"Accept": "text/xhtml"})

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
            for instructor_data in instructors:
                group.instructors.append(instructor.text)
        else:
            group = Group()

        group.regid = root.find('.//*[@class="regid"]').text
        group.name = root.find('.//*[@class="name"]').text
        group.title = root.find('.//*[@class="title"]').text
        group.description = root.find('.//*[@class="description"]').text
        group.contact = root.find('.//*[@class="contact"]').text

        return group

    def _xhtml_from_group(self, group):
        template = loader.get_template("gws/group.xhtml")

        context = Context({"name": group.name,
                           "title": group.title,
                           "description": group.description,
                           "contact": group.contact,
                           "admins": [],
                           "readers": [{"type": "none", "name": "dc=all"}]})

        return template.render(context)

    def _is_valid_group_id(self, group_id):
        if not group_id:
            return False

        return True
