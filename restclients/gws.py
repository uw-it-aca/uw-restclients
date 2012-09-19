"""
This is the interface for interacting with the Group Web Service.
"""

from restclients.dao import GWS_DAO
from restclients.exceptions import InvalidRegID, InvalidNetID
from restclients.models import Group, CourseGroup, Person
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
        url = "/group_sws/v2/group/"+group_id
        response = dao.getURL(url, {"Accept": "text/xhtml"})


        if response.status == 404:
            return

        root = etree.fromstring(response.read())
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
#            for instructor_data in instructors:
#                instructor = Person()
#                group.instructors.append(instructor.text)
        else:
            group = Group()

        group.regid = root.find('.//*[@class="regid"]').text
        group.name = root.find('.//*[@class="name"]').text
        group.title = root.find('.//*[@class="title"]').text
        group.description = root.find('.//*[@class="description"]').text

        return group


    def get_effective_members(self, group_id):
        """
        Returns a list of effective group member data for the group identified
        by the passed group ID.
        """
        if not self._is_valid_group_id(group_id):
            raise InvalidGroupID(group_id)

        dao = GWS_DAO()
        url = "/group_sws/v2/group/"+group_id+"/effective_member"
        response = dao.getURL(url, {"Accept": "text/xhtml"})


        if response.status == 404:
            return

        root = etree.fromstring(response.read())

        members = []
        member_elements = root.findall('.//*[@class="members"]' +
                                       '//*[@class="effective_member"]')
        for member in member_elements:
            person = Person()
            person.uwnetid = member.text

            members.append(person)

        return members

    def _is_valid_group_id(self, group_id):
        if not group_id:
            return False

        return True

