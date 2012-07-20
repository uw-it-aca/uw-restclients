from rest_base import RestBase
import json
import re


class SWSClient(RestBase):
    URL_BASE = '/student/v4'

    def __init__(self, cfg):
        self._cfg = cfg
        self._cfg['logname'] = __name__
        RestBase.__init__(self)

    def get_json(self, url, fields=None):
        headers = {'Accept': 'application/json'}
        r = self.GET(url, fields, headers)
        return json.loads(r.data)

    def get_current_term(self):
        return self.get_json(self.URL_BASE + '/term/current.json')

    def get_next_term(self):
        return self.get_json(self.URL_BASE + '/term/next.json')

    def get_previous_term(self):
        return self.get_json(self.URL_BASE + '/term/previous.json')

    def get_term(self, year, quarter):
        return self.get_json(self.URL_BASE + '/term/' +
                             str(year) + ',' + quarter + '.json')

    def get_campuses(self):
        fields = {
            'page_size': '100',
            'page_start': 1
        }

        data = self.get_json(self.URL_BASE + '/campus.json', fields)
        return data.get('Campuses', None)

    def get_colleges(self, opts={}):
        fields = {
            'year': '',
            'quarter': '',
            'campus_short_name': '',
            'future_terms': '0',
            'page_size': '100',
            'page_start': 1
        }

        for field in fields:
            if field in opts:
                fields[field] = opts[field]

        if (not fields['year'] or not fields['quarter']):
            curr_term = self.get_current_term()
            fields['year'] = curr_term['Year']
            fields['quarter'] = curr_term['Quarter']

        total_count = 1
        ret = []
        while fields['page_start'] <= total_count:
            data = self.get_json(self.URL_BASE + '/college.json', fields)

            total_count = int(data.get('TotalCount', '0'))
            if not total_count:
                break

            colleges = data.get('Colleges', [])
            for college in colleges:
                ret.append(college)

            next_page = data.get('Next', None)
            if not next_page:
                break
            else:
                fields['page_start'] = int(next_page['PageStart'])

        return ret

    def get_curricula(self, opts={}):
        fields = {
            'year': '',
            'quarter': '',
            'department_abbreviation': '',
            'college_abbreviation': '',
            'future_terms': '0',
            'page_size': '100',
            'page_start': 1
        }

        for field in fields:
            if field in opts:
                fields[field] = opts[field]

        if (not fields['year'] or not fields['quarter']):
            curr_term = self.get_current_term()
            fields['year'] = curr_term['Year']
            fields['quarter'] = curr_term['Quarter']

        total_count = 1
        ret = []
        while fields['page_start'] <= total_count:
            data = self.get_json(self.URL_BASE + '/curriculum.json', fields)

            total_count = int(data.get('TotalCount', '0'))
            if not total_count:
                break

            curricula = data.get('Curricula', [])
            for curriculum in curricula:
                ret.append(curriculum)

            next_page = data.get('Next', None)
            if not next_page:
                break
            else:
                fields['page_start'] = int(next_page['PageStart'])

        return ret

    def get_course_by_id(self, course_id):
        if not re.match(r'^\d{4},(?:winter|spring|summer|autumn),[\w& ]+,\d+$',
                        course_id):
            raise Exception("Invalid course id: " + course_id)

        return self.get_json(self.URL_BASE + '/course/' +
                             re.sub(r'\s', '%20', course_id) + '.json')

    def get_courses(self, opts={}):
        fields = {
            'year': '',
            'quarter': '',
            'curriculum_abbreviation': '',
            'course_number': '',
            'course_title_starts': '',
            'course_title_contains': '',
            'sort_by': 'on',
            'future_terms': '0',
            'page_size': '100',
            'page_start': 1
        }

        for field in fields:
            if field in opts:
                fields[field] = opts[field]

        if (not fields['year'] or not fields['quarter']):
            curr_term = self.get_current_term()
            fields['year'] = curr_term['Year']
            fields['quarter'] = curr_term['Quarter']

        total_count = 1
        ret = []
        while fields['page_start'] <= total_count:
            data = self.get_json(self.URL_BASE + '/course.json', fields)

            total_count = int(data.get('TotalCount', '0'))
            if not total_count:
                break

            courses = data.get('Courses', [])
            for course in courses:
                ret.append(course)

            next_page = data.get('Next', None)
            if not next_page:
                break
            else:
                fields['page_start'] = int(next_page['PageStart'])

        return ret

    def get_section(self, params={}):
        section_id = ','.join([
            params.get('year', ''),
            params.get('quarter', ''),
            params.get('curriculum_abbreviation', ''),
            params.get('course_number', '')
        ])
        section_id += '/' + params.get('section_id', '')
        return self.get_section_by_id(section_id)

    def get_section_by_id(self, section_id):
        if not re.match(r'^\d{4},(?:winter|spring|summer|autumn),[\w& ]+,\d+\/[A-Z][A-Z0-9]?$',
                        section_id):
            raise Exception("Invalid section id: " + section_id)

        return self.get_json(self.URL_BASE + '/course/' +
                             re.sub(r'\s', '%20', section_id) + '.json')

    def get_sections(self, opts={}):
        fields = {
            'year': '',
            'quarter': '',
            'curriculum_abbreviation': '',
            'course_number': '',
            'reg_id': '',
            'search_by': 'Instructor',
            'include_secondaries': 'on'
        }

        for field in fields:
            if field in opts:
                fields[field] = opts[field]

        if (not fields['curriculum_abbreviation'] and not fields['reg_id']):
            raise Exception("Either curriculum_abbreviation or reg_id " +
                            "is required")

        if (not fields['year'] or not fields['quarter']):
            curr_term = self.get_current_term()
            fields['year'] = curr_term['Year']
            fields['quarter'] = curr_term['Quarter']

        data = self.get_json(self.URL_BASE + '/section.json', fields)
        sections = data.get('Sections', [])

        ret = []
        for section in sections:
            section_data = self.get_json(section['Href'])
            if section_data:
                ret.append(section_data)

        return ret

    def get_registrations(self, opts={}):
        fields = {
            'year': '',
            'quarter': '',
            'curriculum_abbreviation': '',
            'course_number': '',
            'section_id': '',
            'reg_id': '',
            'instructor_reg_id': '',
            'is_active': ''
        }

        for field in fields:
            if field in opts:
                fields[field] = opts[field]

        if (not fields['curriculum_abbreviation'] or
                not fields['course_number'] or not fields['section_id']):
            raise Exception("Curriculum_abbreviation, course_number, and " +
                            "section_id are required")

        if (not fields['year'] or not fields['quarter']):
            curr_term = self.get_current_term()
            fields['year'] = curr_term['Year']
            fields['quarter'] = curr_term['Quarter']

        is_active = str(fields['is_active'])
        if 'on' != is_active:
            fields['is_active'] = ''

        data = self.get_json(self.URL_BASE + '/registration.json', fields)
        return data.get('Registrations', [])

    def get_full_registrations(self, opts={}):
        registrations = self.get_registrations(opts)
        registrations.reverse()

        seen = {}
        ret = []
        for registration in registrations:
            # Prevent duplicate registrations, the reverse above ensures that
            # we keep the latest duplicate
            if registration['RegID'] in seen:
                continue
            seen[registration['RegID']] = True

            reg_data = self.get_json(registration['Href'])
            if reg_data:
                ret.append(reg_data)

        return ret
