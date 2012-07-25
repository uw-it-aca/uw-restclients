from rest_base import RestBase
import xml.etree.ElementTree


class GWSClient(RestBase):
    URL_BASE = '/group_sws/v2/group'
    QTRS = {'win': 'winter', 'spr': 'spring', 'sum': 'summer', 'aut': 'autumn'}

    def __init__(self, cfg):
        self._cfg = {
            'host': settings.GWS_HOST,
            'port': settings.GWS_PORT,
            'cert': settings.GWS_CERT,
            'key': settings.GWS_KEY,
            'timeout': settings.GWS_TIMEOUT,
            'log': settings.GWS_LOG,
            'logname': __name__
        }
        RestBase.__init__(self)

    def get_xml(self, url, fields=None, headers={}):
        headers.update({'Accept': 'text/xhtml'})
        r = self.GET(url, fields, headers)
        return xml.etree.ElementTree.fromstring(r.data)

    def get_group_by_id(self, group_id):
        if not self._is_valid_group_id(group_id):
            raise Exception("Missing or invalid group ID")

        root = self.get_xml(self.URL_BASE + '/' + group_id)
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

    def get_groups(self, opts):
        raise Exception("Not implemented")

    def get_members(self, group_id):
        if not self._is_valid_group_id(group_id):
            raise Exception("Missing or invalid group ID")

        root = self.get_xml(self.URL_BASE + '/' + group_id + '/member')
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
        if not self._is_valid_group_id(group_id):
            raise Exception("Missing or invalid group ID")

        root = self.get_xml(self.URL_BASE + '/' + group_id +
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
