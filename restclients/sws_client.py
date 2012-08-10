from rest_base import RestBase
from django.conf import settings
import json
import re


class InvalidCourseID(Exception):
    """Exception for invalid course id."""
    pass


class InvalidSectionID(Exception):
    """Exception for invalid section id."""
    pass


class SWSClient(RestBase):
    """
    Client for retrieving person data from the UW Student Web Service. Configuration
    parameters for this client are:

    :SWS_URL:
        The absolute URL of the SWS host. URL must include scheme and port (if not 80).
        Ex. https://ucswseval1.cac.washington.edu:443

    :SWS_CERT:
        Path of a certficate file. Required for access to eval and production SWS.
        Ex. /usr/local/ssl/foo.cert

    :SWS_KEY:
        Path of a public key file. Required for access to eval and production SWS.
        Ex. /usr/local/ssl/foo.key

    :SWS_TIMEOUT:
        Socket timeout for each individual connection, can be a float. None disables timeout.

    :SWS_LOG:
        Path of a file where logging will be written.
        Ex. /usr/local/logs/eval/log

    """
    URL_BASE = '/student/v4'

    def __init__(self):
        self._cfg = {
            'url': settings.SWS_URL,
            'cert': settings.SWS_CERT,
            'key': settings.SWS_KEY,
            'timeout': settings.SWS_TIMEOUT,
            'log': settings.SWS_LOG,
            'logname': __name__
        }
        RestBase.__init__(self)

    def get_json(self, url, fields=None):
        headers = {'Accept': 'application/json'}
        r = self.GET(url, fields, headers)
        return json.loads(r.data)

    def get_current_term(self):
        """
        Returns term data for the current term.
        """
        return self.get_json(self.URL_BASE + '/term/current.json')

    def get_next_term(self):
        """
        Returns term data for the next term.
        """
        return self.get_json(self.URL_BASE + '/term/next.json')

    def get_previous_term(self):
        """
        Returns term data for the previous term.
        """
        return self.get_json(self.URL_BASE + '/term/previous.json')

    def get_term(self, year, quarter):
        """
        Returns term data for the term identified by the passed year and
        quarter.
        """
        return self.get_json(self.URL_BASE + '/term/' +
                             str(year) + ',' + quarter + '.json')

    def get_campuses(self):
        """
        Returns a list of campus data for all UW campuses.
        """
        fields = {
            'page_size': '100',
            'page_start': 1
        }

        data = self.get_json(self.URL_BASE + '/campus.json', fields)
        return data.get('Campuses', None)

    def get_colleges(self, opts={}):
        """
        Returns a list of college data for UW colleges. Valid parameters are:

        :param year:
            Term year. Defaults to current term year.

        :param quarter:
            Term quarter. Defaults to current term quarter.

        :param campus_short_name:
            Unique campus identifier

        :param future_terms:
            Number of future terms to search: 0|1|2. Default is 0.

        """
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

    def get_departments(self, opts={}):
        """
        Returns a list of department data for UW departments. Valid parameters
        are:

        :param year:
            Term year. Defaults to current term year.

        :param quarter:
            Term quarter. Defaults to current term quarter.

        :param college_abbreviation:
            Unique college identifier

        :param future_terms:
            Number of future terms to search: 0|1|2. Default is 0.

        """
        fields = {
            'year': '',
            'quarter': '',
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
            data = self.get_json(self.URL_BASE + '/department.json', fields)

            total_count = int(data.get('TotalCount', '0'))
            if not total_count:
                break

            departments = data.get('Departments', [])
            for department in departments:
                ret.append(department)

            next_page = data.get('Next', None)
            if not next_page:
                break
            else:
                fields['page_start'] = int(next_page['PageStart'])

        return ret

    def get_curricula(self, opts={}):
        """
        Returns a list of curriculum data for UW curricula. Valid parameters
        are:

        :param year:
            Term year. Defaults to current term year.

        :param quarter:
            Term quarter. Defaults to current term quarter.

        :param department_abbreviation:
            Unique department identifier

        :param college_abbreviation:
            Unique college identifier

        :param future_terms:
            Number of future terms to search: 0|1|2. Default is 0.

        """
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
        """
        Returns course data for the course identified by the passed course ID.
        """
        if not re.match(r'^\d{4},(?:winter|spring|summer|autumn),[\w& ]+,\d+$',
                        course_id):
            raise InvalidCourseID(course_id)

        return self.get_json(self.URL_BASE + '/course/' +
                             re.sub(r'\s', '%20', course_id) + '.json')

    def get_courses(self, opts={}):
        """
        Returns a list of course data for UW courses. Valid parameters for
        searching are:

        :param year:
            Term year. Defaults to current term year.

        :param quarter:
            Term quarter. Defaults to current term quarter.

        :param curriculum_abbreviation:
            Unique curriculum identifier

        :param course_number:
            Three-digit identifier for a course

        :param course_title_starts:

        :param course_title_contains:

        :param future_terms:
            Number of future terms to search: 0|1|2. Default is 0.

        """
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
        """
        Returns course section data for the section identified by the passed
        dict of section data. Required parameters are:
            year, quarter, curriculum_abbreviation, course_number, section_id
        """
        section_id = ','.join([
            params.get('year', ''),
            params.get('quarter', ''),
            params.get('curriculum_abbreviation', ''),
            params.get('course_number', '')
        ])
        section_id += '/' + params.get('section_id', '')
        return self.get_section_by_id(section_id)

    def get_section_by_id(self, section_id):
        """
        Returns course section data for the section identified by the passed
        section ID.
        """
        if not re.match(r'^\d{4},(?:winter|spring|summer|autumn),[\w& ]+,\d+\/[A-Z][A-Z0-9]?$',
                        section_id):
            raise InvalidSectionID(section_id)

        return self.get_json(self.URL_BASE + '/course/' +
                             re.sub(r'\s', '%20', section_id) + '.json')

    def section_search(self, opts={}):
        """
        Returns a list of section data for UW course sections. Valid
        parameters for searching are:

        :param year:
            Term year. Defaults to current term year.

        :param quarter:
            Term quarter. Defaults to current term quarter.

        :param curriculum_abbreviation:
            Unique curriculum identifier

        :param course_number:
            Three-digit identifier for a course

        :param reg_id:
            Instructor or GradeSubmissionDelegate UW RegID.

        :param search_by:
            Specifies whether search is for Instructor or GradeSubmissionDelegate,
            when reg_id is included.

        :param include_secondaries:
            Include secondary sections, effective only when reg_id is included.
            Default is 'on'.

        """
        fields = {
            'year': '',
            'quarter': '',
            'curriculum_abbreviation': '',
            'course_number': '',
            'reg_id': '',
            'search_by': 'Instructor',  # Instructor|GradeSubmissionDelegate
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
        return data.get('Sections', [])

    def get_sections(self, opts={}):
        """
        Returns a list of "full" section data for UW course sections, using
        search parameters for section_search().
        """
        sections = self.section_search(opts)

        ret = []
        for section in sections:
            section_data = self.get_json(section['Href'])
            if section_data:
                ret.append(section_data)

        return ret

    def registration_search(self, opts={}):
        """
        Returns a list of section data for UW course sections. Valid
        parameters for searching are:

        :param year:
            Term year. Defaults to current term year.

        :param quarter:
            Term quarter. Defaults to current term quarter.

        :param curriculum_abbreviation:
            Unique curriculum identifier

        :param course_number:
            Three-digit identifier for a course

        :param section_id:
            Unique section identifier

        :param reg_id:
            Student UW RegID

        :param instructor_reg_id:
            Instructor UW RegID, for independent study sections

        :param is_active:
            Specifies whether to include only active registrations. Default
            is ''.

        """
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

        if (fields['curriculum_abbreviation'] or fields['course_number'] or
                fields['section_id']):
            if (not fields['curriculum_abbreviation'] or not
                    fields['course_number'] or not fields['section_id']):
                raise Exception("Curriculum_abbreviation, course_number, " +
                                "and section_id are required")
        else:
            if not fields['reg_id']:
                raise Exception("Student reg_id is required")

        if (not fields['year'] or not fields['quarter']):
            curr_term = self.get_current_term()
            fields['year'] = curr_term['Year']
            fields['quarter'] = curr_term['Quarter']

        is_active = str(fields['is_active'])
        if 'on' != is_active:
            fields['is_active'] = ''

        data = self.get_json(self.URL_BASE + '/registration.json', fields)
        return data.get('Registrations', [])

    def get_registrations(self, opts={}):
        """
        Returns a list of "full" registration data for UW course sections,
        using search parameters for registration_search().
        """
        registrations = self.registration_search(opts)
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
