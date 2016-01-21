import pickle
from django.db import models
from django.template import Context, loader
from base64 import b64encode, b64decode
from datetime import datetime
from restclients.exceptions import InvalidCanvasIndependentStudyCourse
from restclients.exceptions import InvalidCanvasSection
from restclients.util.date_formator import abbr_week_month_day_str
from restclients.util.datetime_convertor import convert_to_begin_of_day,\
    convert_to_end_of_day
from restclients.models.base import RestClientsModel


# PWS Person
class Person(RestClientsModel):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)

    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    whitepages_publish = models.NullBooleanField()

    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    full_name = models.CharField(max_length=250)
    display_name = models.CharField(max_length=250)

    student_number = models.CharField(max_length=9)
    student_system_key = models.SlugField(max_length=10)
    employee_id = models.CharField(max_length=9)

    is_student = models.NullBooleanField()
    is_staff = models.NullBooleanField()
    is_employee = models.NullBooleanField()
    is_alum = models.NullBooleanField()
    is_faculty = models.NullBooleanField()

    email1 = models.CharField(max_length=255)
    email2 = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255)
    voicemail = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)
    touchdial = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    mailstop = models.CharField(max_length=255)
    title1 = models.CharField(max_length=255)
    title2 = models.CharField(max_length=255)
    home_department = models.CharField(max_length=255)

    student_class = models.CharField(max_length=255)
    student_department1 = models.CharField(max_length=255)
    student_department2 = models.CharField(max_length=255)
    student_department3 = models.CharField(max_length=255)

    def json_data(self):
        return {'uwnetid': self.uwnetid,
                'uwregid': self.uwregid,
                'first_name': self.first_name,
                'surname': self.surname,
                'full_name': self.full_name,
                'whitepages_publish': self.whitepages_publish,
                'email1': self.email1,
                'email2': self.email2,
                'phone1': self.phone1,
                'phone2': self.phone2,
                'title1': self.title1,
                'title2': self.title2,
                'voicemail': self.voicemail,
                'fax': self.fax,
                'touchdial': self.touchdial,
                'address1': self.address1,
                'address2': self.address2,
                'mailstop': self.mailstop,
                'home_department': self.home_department,
                }

    def __eq__(self, other):
        return self.uwregid == other.uwregid


# PWS Person
class Entity(RestClientsModel):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)
    uwnetid = models.CharField(max_length=128,
                               db_index=True,
                               unique=True)
    display_name = models.CharField(max_length=250)

    def json_data(self):
        return {'uwnetid': self.uwnetid,
                'uwregid': self.uwregid,
                'display_name': self.display_name,
                }

    def __eq__(self, other):
        return self.uwregid == other.uwregid


class LastEnrolled(RestClientsModel):
    href = models.CharField(max_length=200)
    quarter = models.CharField(max_length=16)
    year = models.PositiveSmallIntegerField()

    def json_data(self):
        return {'href': self.href,
                'quarter': self.quarter,
                'year': self.year
                }


class StudentAddress(RestClientsModel):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street_line1 = models.CharField(max_length=255)
    street_line2 = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=32)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=32)

    def json_data(self):
        return {'city': self.city,
                'country': self.country,
                'street_line1': self.street_line1,
                'street_line2': self.street_line2,
                'postal_code': self.postal_code,
                'state': self.state,
                'zip_code': self.zip_code
                }


def get_student_address_json(address):
    if address is not None:
        return address.json_data()
    return None


class SwsPerson(RestClientsModel):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)
    directory_release = models.NullBooleanField(null=True)
    employee_id = models.SlugField(max_length=16, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=255)
    student_number = models.SlugField(max_length=16, null=True, blank=True)
    student_system_key = models.SlugField(max_length=16, null=True, blank=True)
    last_enrolled = models.ForeignKey(
        LastEnrolled,
        on_delete=models.PROTECT,
        null=True)
    local_address = models.ForeignKey(
        StudentAddress,
        on_delete=models.PROTECT,
        null=True,
        related_name='local_address')
    local_phone = models.CharField(max_length=64, null=True, blank=True)
    permanent_address = models.ForeignKey(
        StudentAddress,
        on_delete=models.PROTECT,
        null=True,
        related_name='permanent_address')
    permanent_phone = models.CharField(max_length=64, null=True, blank=True)
    visa_type = models.CharField(max_length=2, null=True, blank=True)

    def json_data(self):
        return {
            'uwnetid': self.uwnetid,
            'uwregid': self.uwregid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'student_name': self.student_name,
            'student_number': self.student_number,
            'employee_id': self.employee_id,
            'directory_release': self.directory_release,
            'local_address': get_student_address_json(self.local_address),
            'local_phone': self.local_phone,
            'permanent_address': get_student_address_json(
                self.permanent_address),
            'permanent_phone': self.permanent_phone,
            'visa_type': self.visa_type
                }


class Term(RestClientsModel):
    SPRING = 'spring'
    SUMMER = 'summer'
    AUTUMN = 'autumn'
    WINTER = 'winter'

    QUARTERNAME_CHOICES = (
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
        (AUTUMN, 'Autumn'),
        (WINTER, 'Winter'),
    )

    quarter = models.CharField(max_length=6,
                               choices=QUARTERNAME_CHOICES)
    year = models.PositiveSmallIntegerField()
    last_day_add = models.DateField()
    last_day_drop = models.DateField()
    first_day_quarter = models.DateField(db_index=True)
    census_day = models.DateField()
    last_day_instruction = models.DateField(db_index=True)
    aterm_last_date = models.DateField(blank=True)
    bterm_first_date = models.DateField(blank=True)
    aterm_last_day_add = models.DateField(blank=True)
    bterm_last_day_add = models.DateField(blank=True)
    last_final_exam_date = models.DateField()
    grading_period_open = models.DateTimeField()
    aterm_grading_period_open = models.DateTimeField(blank=True)
    grading_period_close = models.DateTimeField()
    grade_submission_deadline = models.DateTimeField()
    registration_services_start = models.DateTimeField()
    registration_period1_start = models.DateTimeField()
    registration_period1_end = models.DateTimeField()
    registration_period2_start = models.DateTimeField()
    registration_period2_end = models.DateTimeField()
    registration_period3_start = models.DateTimeField()
    registration_period3_end = models.DateTimeField()

    class Meta(RestClientsModel.Meta):
        unique_together = ("year", "quarter")

    def __eq__(self, other):
        return self.year == other.year and self.quarter == other.quarter

    def is_grading_period_open(self):
        if self.quarter == self.SUMMER:
            open_date = self.aterm_grading_period_open
        else:
            open_date = self.grading_period_open

        return (open_date <= datetime.now() <= self.grade_submission_deadline)

    def is_grading_period_past(self):
        return (datetime.now() > self.grade_submission_deadline)

    def get_week_of_term(self):
        return self.get_week_of_term_for_date(datetime.now())

    def get_week_of_term_for_date(self, date):
        days = (date.date() - self.first_day_quarter).days
        if days >= 0:
            return (days / 7) + 1

        return (days / 7)

    def is_summer_quarter(self):
        return self.quarter.lower() == "summer"

    def get_bod_first_day(self):
        # returns a datetime object of the midnight at begining of day
        return convert_to_begin_of_day(self.first_day_quarter)

    def get_bod_reg_period1_start(self):
        return convert_to_begin_of_day(self.registration_period1_start)

    def get_bod_reg_period2_start(self):
        return convert_to_begin_of_day(self.registration_period2_start)

    def get_bod_reg_period3_start(self):
        return convert_to_begin_of_day(self.registration_period3_start)

    def get_eod_grade_submission(self):
        # returns a datetime object of the midnight at end of day
        return convert_to_end_of_day(self.grade_submission_deadline)

    def get_eod_aterm_last_day_add(self):
        if not self.is_summer_quarter():
            return None
        return convert_to_end_of_day(self.aterm_last_day_add)

    def get_eod_bterm_last_day_add(self):
        if not self.is_summer_quarter():
            return None
        return convert_to_end_of_day(self.bterm_last_day_add)

    def get_eod_last_day_add(self):
        return convert_to_end_of_day(self.last_day_add)

    def get_eod_last_day_drop(self):
        return convert_to_end_of_day(self.last_day_drop)

    def get_eod_census_day(self):
        return convert_to_end_of_day(self.census_day)

    def get_eod_last_final_exam(self):
        return convert_to_end_of_day(self.last_final_exam_date)

    def get_eod_last_instruction(self):
        return convert_to_end_of_day(self.last_day_instruction)

    def get_eod_summer_aterm(self):
        if not self.is_summer_quarter():
            return None
        return convert_to_end_of_day(self.aterm_last_date)

    def term_label(self):
        return "%s,%s" % (self.year, self.quarter)

    def canvas_sis_id(self):
        return "%s-%s" % (self.year, self.quarter.lower())

    def json_data(self):
        return {
            'quarter': self.get_quarter_display(),
            'year': self.year,
            'last_final_exam_date': self.last_final_exam_date.strftime(
                "%Y-%m-%d 23:59:59"),
            'grade_submission_deadline':
                self.grade_submission_deadline.strftime(
                "%Y-%m-%d 23:59:59")
        }


class FinalExam(RestClientsModel):
    is_confirmed = models.NullBooleanField()
    no_exam_or_nontraditional = models.NullBooleanField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    building = models.CharField(max_length=20, null=True, blank=True)
    room_number = models.CharField(max_length=10, null=True, blank=True)

    def json_data(self):
        data = {
            "is_confirmed": self.is_confirmed,
            "no_exam_or_nontraditional": self.no_exam_or_nontraditional,
        }

        if self.start_date:
            data["start_date"] = self.start_date.strftime("%Y-%m-%d %H:%M")
            data["end_date"] = self.end_date.strftime("%Y-%m-%d %H:%M")
            data["building"] = self.building
            data["room_number"] = self.room_number

        return data


class Section(RestClientsModel):
    SUMMER_A_TERM = "a-term"
    SUMMER_B_TERM = "b-term"
    SUMMER_FULL_TERM = "full-term"

    LMS_CANVAS = "CANVAS"
    LMS_CATALYST = "CATALYST"
    LMS_MOODLE = "MOODLE"
    LMS_NONE = "NONE"

    PRIMARY_LMS_CHOICES = (
        (LMS_CANVAS, LMS_CANVAS),
        (LMS_CATALYST, LMS_CATALYST),
        (LMS_MOODLE, LMS_MOODLE),
        (LMS_NONE, LMS_NONE),
    )

    LMS_OWNER_CAMPUS = "CAMPUS"
    LMS_OWNER_AP = "PCE_AP"
    LMS_OWNER_IELP = "PCS_IELP"
    LMS_OWNER_OL = "PCE_OL"

    LMS_OWNER_CHOICES = (
        (LMS_OWNER_CAMPUS, LMS_OWNER_CAMPUS),
        (LMS_OWNER_AP, LMS_OWNER_AP),
        (LMS_OWNER_IELP, LMS_OWNER_IELP),
        (LMS_OWNER_OL, LMS_OWNER_OL),
    )

    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    final_exam = models.ForeignKey(FinalExam,
                                   on_delete=models.PROTECT,
                                   null=True)

    curriculum_abbr = models.CharField(max_length=6,
                                       db_index=True)
    course_number = models.PositiveSmallIntegerField(db_index=True)
    section_id = models.CharField(max_length=2,
                                  db_index=True)
    course_title = models.CharField(max_length=20)
    course_title_long = models.CharField(max_length=50)
    course_campus = models.CharField(max_length=7)
    section_type = models.CharField(max_length=30)
    is_independent_study = models.NullBooleanField()
    independent_study_instructor_regid = models.CharField(max_length=32,
                                                          null=True)
    institute_name = models.CharField(max_length=200, null=True)
    class_website_url = models.URLField(max_length=255,
                                        blank=True)
    sln = models.PositiveIntegerField()
    summer_term = models.CharField(max_length=12, null=True)
    delete_flag = models.CharField(max_length=20)
    is_withdrawn = models.NullBooleanField()
    primary_lms = models.CharField(max_length=12, choices=PRIMARY_LMS_CHOICES,
                                   null=True)
    lms_ownership = models.CharField(max_length=12, choices=LMS_OWNER_CHOICES)
    is_independent_start = models.NullBooleanField()
    current_enrollment = models.IntegerField()
    auditors = models.IntegerField()

    # These are for non-standard start/end dates - don't have those yet
    # start_date = models.DateField()
    # end_date = models.DateField()

    # We don't have final exam data yet :(
    # final_exam_date = models.DateField()
    # final_exam_start_time = models.TimeField()
    # final_exam_end_time = models.TimeField()
    # final_exam_building = models.CharField(max_length=5)
    # final_exam_room_number = models.CharField(max_length=5)

    primary_section_href = models.CharField(
                                            max_length=200,
                                            null=True,
                                            blank=True,
                                            )
    primary_section_curriculum_abbr = models.CharField(
                                                        max_length=6,
                                                        null=True,
                                                        blank=True,
                                                        )
    primary_section_course_number = models.PositiveSmallIntegerField(
                                                            null=True,
                                                            blank=True,
                                                            )
    primary_section_id = models.CharField(max_length=2, null=True, blank=True)
    is_primary_section = models.NullBooleanField()
    allows_secondary_grading = models.NullBooleanField()
    is_auditor = models.NullBooleanField()
    student_credits = models.DecimalField(max_digits=3, decimal_places=1)
    student_grade = models.CharField(max_length=6, null=True, blank=True)
    grade_date = models.DateField(null=True, blank=True, default=None)

    class Meta(RestClientsModel.Meta):
        unique_together = ('term',
                           'curriculum_abbr',
                           'course_number',
                           'section_id')

    def section_label(self):
        return "%s,%s,%s,%s/%s" % (
            self.term.year,
            self.term.quarter,
            self.curriculum_abbr,
            self.course_number,
            self.section_id)

    def primary_section_label(self):
        return "%s,%s,%s,%s/%s" % (
            self.term.year,
            self.term.quarter,
            self.primary_section_curriculum_abbr,
            self.primary_section_course_number,
            self.primary_section_id)

    def get_instructors(self):
        instructors = []
        for meeting in self.meetings:
            instructors.extend(meeting.instructors)
        return instructors

    def is_instructor(self, person):
        for meeting in self.meetings:
            if person in meeting.instructors:
                return True
        return False

    def is_grade_submission_delegate(self, person):
        for delegate in self.grade_submission_delegates:
            if person == delegate.person:
                return True
        return False

    def is_grading_period_open(self):
        now = datetime.now()
        if self.is_summer_a_term():
            open_date = self.term.aterm_grading_period_open
        else:
            open_date = self.term.grading_period_open

        return (open_date <= now <= self.term.grade_submission_deadline)

    def canvas_course_sis_id(self):
        if self.is_primary_section:
            sis_id = "%s-%s-%s-%s" % (
                self.term.canvas_sis_id(),
                self.curriculum_abbr.upper(),
                self.course_number,
                self.section_id.upper())

            if self.is_independent_study:
                if self.independent_study_instructor_regid is None:
                    raise InvalidCanvasIndependentStudyCourse(
                        "Undefined " +
                        ("instructor for independent study section: %s" %
                         sis_id))
                sis_id += "-%s" % self.independent_study_instructor_regid
        else:
            sis_id = "%s-%s-%s-%s" % (
                self.term.canvas_sis_id(),
                self.primary_section_curriculum_abbr.upper(),
                self.primary_section_course_number,
                self.primary_section_id.upper())

        return sis_id

    def canvas_section_sis_id(self):
        if self.is_primary_section:
            sis_id = self.canvas_course_sis_id()

            if not self.is_independent_study and len(self.linked_section_urls):
                raise InvalidCanvasSection(sis_id)

            sis_id += "--"
        else:
            sis_id = "%s-%s-%s-%s" % (
                self.term.canvas_sis_id(),
                self.curriculum_abbr.upper(),
                self.course_number,
                self.section_id.upper())

        return sis_id

    def get_grade_date_str(self):
        """
        return next due date in the ISO format (yyyy-mm-dd).
        If the next_due is None, return None.
        """
        if self.grade_date is not None:
            return str(self.grade_date)
        return None

    def is_summer_a_term(self):
        return self.summer_term is not None and\
            len(self.summer_term) > 0 and\
            self.summer_term.lower() == self.SUMMER_A_TERM

    def is_summer_b_term(self):
        return self.summer_term is not None and\
            len(self.summer_term) > 0 and\
            self.summer_term.lower() == self.SUMMER_B_TERM

    def is_half_summer_term(self):
        return (self.is_summer_a_term() or
                self.is_summer_b_term())

    def is_full_summer_term(self):
        return self.summer_term is not None and\
            len(self.summer_term) > 0 and\
            self.summer_term.lower() == self.SUMMER_FULL_TERM

    def is_same_summer_term(self, summer_term):
        return (self.summer_term is None or len(self.summer_term) == 0) and\
            (summer_term is None or len(self.summer_term) == 0) or\
            self.summer_term is not None and summer_term is not None and\
            self.summer_term.lower() == summer_term.lower()

    def json_data(self):
        data = {
            'curriculum_abbr': self.curriculum_abbr,
            'course_number': self.course_number,
            'section_id': self.section_id,
            'is_primary_section': self.is_primary_section,
            'course_title': self.course_title,
            'course_campus': self.course_campus,
            'class_website_url': self.class_website_url,
            'sln': self.sln,
            'summer_term': self.summer_term,
            'start_date': '',
            'end_date': '',
            'current_enrollment': self.current_enrollment,
            'auditors': self.auditors,
            'meetings': [],
            'credits': str(self.student_credits),
            'is_auditor':  self.is_auditor,
            'grade': self.student_grade,
            'grade_date': self.get_grade_date_str()
        }

        if self.final_exam is not None:
            data["final_exam"] = self.final_exam.json_data()

        for meeting in self.meetings:
            data["meetings"].append(meeting.json_data())

        return data


class SectionReference(RestClientsModel):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    curriculum_abbr = models.CharField(max_length=6)
    course_number = models.PositiveSmallIntegerField()
    section_id = models.CharField(max_length=2)
    url = models.URLField(max_length=255,
                          blank=True)

    def section_label(self):
        return "%s,%s,%s,%s/%s" % (
            self.term.year,
            self.term.quarter, self.curriculum_abbr,
            self.course_number, self.section_id)


class SectionStatus(RestClientsModel):
    add_code_required = models.NullBooleanField()
    current_enrollment = models.IntegerField()
    current_registration_period = models.IntegerField()
    faculty_code_required = models.NullBooleanField()
    limit_estimated_enrollment = models.IntegerField()
    limit_estimate_enrollment_indicator = models.CharField(max_length=8)
    room_capacity = models.IntegerField()
    sln = models.PositiveIntegerField()
    space_available = models.IntegerField()
    is_open = models.CharField(max_length=6)

    def json_data(self):
        data = {
            'add_code_required': self.add_code_required,
            'current_enrollment': self.current_enrollment,
            'current_registration_period': self.current_registration_period,
            'faculty_code_required': self.faculty_code_required,
            'limit_estimated_enrollment': self.limit_estimated_enrollment,
            'limit_estimate_enrollment_indicator':
                self.limit_estimate_enrollment_indicator,
            'room_capacity': self.room_capacity,
            'sln': self.sln,
            'space_available': self.space_available,
            'is_open': self.status,
        }
        return data


class Registration(RestClientsModel):
    section = models.ForeignKey(Section,
                                on_delete=models.PROTECT)
    person = models.ForeignKey(Person,
                               on_delete=models.PROTECT)
    is_active = models.NullBooleanField()


class SectionMeeting(RestClientsModel):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    section = models.ForeignKey(Section,
                                on_delete=models.PROTECT)
    meeting_index = models.PositiveSmallIntegerField()
    meeting_type = models.CharField(max_length=20)
    building_to_be_arranged = models.NullBooleanField()
    building = models.CharField(max_length=5)
    room_to_be_arranged = models.NullBooleanField()
    room_number = models.CharField(max_length=5)
    days_to_be_arranged = models.NullBooleanField()
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)

    meets_monday = models.NullBooleanField()
    meets_tuesday = models.NullBooleanField()
    meets_wednesday = models.NullBooleanField()
    meets_thursday = models.NullBooleanField()
    meets_friday = models.NullBooleanField()
    meets_saturday = models.NullBooleanField()
    meets_sunday = models.NullBooleanField()
    # instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)

    class Meta(RestClientsModel.Meta):
        unique_together = ('term',
                           'section',
                           'meeting_index')

    def json_data(self):
        data = {
            'index': self.meeting_index,
            'type': self.meeting_type,
            'days_tbd': self.days_to_be_arranged,
            'meeting_days': {
                'monday': self.meets_monday,
                'tuesday': self.meets_tuesday,
                'wednesday': self.meets_wednesday,
                'thursday': self.meets_thursday,
                'friday': self.meets_friday,
                'saturday': self.meets_saturday,
                'sunday': self.meets_sunday,
            },
            'start_time': self.start_time,
            'end_time': self.end_time,
            'building_tbd': self.building_to_be_arranged,
            'building': self.building,
            'room_tbd': self.room_to_be_arranged,
            'room': self.room_number,
            'instructors': [],
        }

        for instructor in self.instructors:
            data["instructors"].append(instructor.json_data())

        return data


class StudentGrades(RestClientsModel):
    user = models.ForeignKey(Person)
    term = models.ForeignKey(Term)

    grade_points = models.DecimalField(max_digits=5, decimal_places=2)
    credits_attempted = models.DecimalField(max_digits=3, decimal_places=1)
    non_grade_credits = models.DecimalField(max_digits=3, decimal_places=1)


class StudentCourseGrade(RestClientsModel):
    grade = models.CharField(max_length=10)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    section = models.ForeignKey(Section,
                                on_delete=models.PROTECT)


class ClassSchedule(RestClientsModel):
    user = models.ForeignKey(Person)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)

    def json_data(self):
        data = {
            'year': self.term.year,
            'quarter': self.term.quarter,
            'term': self.term.json_data(),
            'sections': [],
        }

        for section in self.sections:
            data["sections"].append(section.json_data())

        return data


class Campus(RestClientsModel):
    label = models.SlugField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=60)


class College(RestClientsModel):
    campus_label = models.SlugField(max_length=15)
    label = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=60)
    full_name = models.CharField(max_length=60)


class Department(RestClientsModel):
    college_label = models.CharField(max_length=15)
    label = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=60)
    full_name = models.CharField(max_length=60)


class Curriculum(RestClientsModel):
    label = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=60)
    full_name = models.CharField(max_length=60)


class GradeRoster(RestClientsModel):
    section = models.ForeignKey(Section,
                                on_delete=models.PROTECT)
    instructor = models.ForeignKey(Person,
                                   on_delete=models.PROTECT)
    section_credits = models.FloatField()
    allows_writing_credit = models.NullBooleanField()

    def graderoster_label(self):
        return "%s,%s,%s,%s,%s,%s" % (
            self.section.term.year,
            self.section.term.quarter,
            self.section.curriculum_abbr,
            self.section.course_number,
            self.section.section_id,
            self.instructor.uwregid)

    def xhtml(self):
        template = loader.get_template("sws/graderoster.xhtml")
        context = Context({
            "graderoster": self,
            "section_id": self.section.section_label()
        })
        return template.render(context)


class GradeRosterItem(RestClientsModel):
    student_uwregid = models.CharField(max_length=32)
    student_first_name = models.CharField(max_length=100)
    student_surname = models.CharField(max_length=100)
    student_former_name = models.CharField(max_length=120, null=True)
    student_number = models.PositiveIntegerField()
    student_type = models.CharField(max_length=20, null=True)
    student_credits = models.FloatField()
    duplicate_code = models.CharField(max_length=8, null=True)
    section_id = models.CharField(max_length=2)
    is_auditor = models.BooleanField(default=False)
    allows_incomplete = models.BooleanField(default=False)
    has_incomplete = models.BooleanField(default=False)
    has_writing_credit = models.BooleanField(default=False)
    no_grade_now = models.BooleanField(default=False)
    date_withdrawn = models.DateField(null=True)
    grade = models.CharField(max_length=20, null=True, default=None)
    allows_grade_change = models.BooleanField(default=False)
    date_graded = models.DateField(null=True)
    grade_submitter_person = models.ForeignKey(Person,
                                               related_name="grade_submitter",
                                               null=True)
    grade_submitter_source = models.CharField(max_length=8, null=True)
    status_code = models.CharField(max_length=3, null=True)
    status_message = models.CharField(max_length=500, null=True)

    def student_label(self, separator=","):
        label = self.student_uwregid
        if self.duplicate_code is not None and len(self.duplicate_code):
            label += "%s%s" % (separator, self.duplicate_code)
        return label

    def __eq__(self, other):
        return (self.student_uwregid == other.student_uwregid and
                self.duplicate_code == other.duplicate_code)


class GradeSubmissionDelegate(RestClientsModel):
    person = models.ForeignKey(Person,
                               on_delete=models.PROTECT)
    delegate_level = models.CharField(max_length=20)


class TimeScheduleConstruction(RestClientsModel):
    campus = models.SlugField(max_length=15)
    is_on = models.NullBooleanField()


class NoticeAttribute(RestClientsModel):
    name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)

    _url_value = models.URLField(blank=True)
    _string_value = models.CharField(max_length=100, blank=True)
    _date_value = models.DateField(blank=True)

    def get_value(self):
        if self.data_type == "date":
            return self._date_value.strftime("%Y-%m-%d")
        if self.data_type == "string":
            return self._string_value
        if self.data_type == "url":
            return self._url_value

    def get_formatted_date_value(self):
        if self._date_value:
            return abbr_week_month_day_str(self._date_value)
        return None


class Notice(RestClientsModel):
    notice_category = models.CharField(max_length=100)
    notice_content = models.TextField()
    notice_type = models.CharField(max_length=100)
    custom_category = models.CharField(max_length=100,
                                       default="Uncategorized"
                                       )
    # long_notice: if it is a short notice, this attribute
    # will point to the corresponding long notice

    def json_data(self, include_abbr_week_month_day_format=False):

        attrib_data = []

        for attrib in self.attributes:
            if attrib.data_type == "date" and\
                    include_abbr_week_month_day_format:
                attrib_data.append(
                    {'name': attrib.name,
                     'data_type': attrib.data_type,
                     'value': attrib.get_value(),
                     'formatted_value': attrib.get_formatted_date_value()
                     })
            else:
                attrib_data.append(
                    {'name': attrib.name,
                     'data_type': attrib.data_type,
                     'value': attrib.get_value()
                     })

        data = {
            'notice_content': self.notice_content,
            'attributes': attrib_data
        }
        return data


class Finance(RestClientsModel):
    tuition_accbalance = models.FloatField()
    pce_accbalance = models.FloatField()

    def json_data(self):
        return {'tuition_accbalance': self.tuition_accbalance,
                'pce_accbalance': self.pce_accbalance
                }

    def __str__(self):
        return "{tuition_accbalance: %s, pce_accbalance: %s}" % (
            self.tuition_accbalance, self.pce_accbalance)


class Enrollment(RestClientsModel):
    is_honors = models.NullBooleanField()
    class_level = models.CharField(max_length=100)
    regid = models.CharField(max_length=32,
                             db_index=True,
                             unique=True)


class Major(RestClientsModel):
    degree_name = models.CharField(max_length=100)
    degree_abbr = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    major_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    campus = models.CharField(max_length=8)

    def json_data(self):
        return {'degree_abbr': self.degree_abbr,
                'degree_name': self.degree_name,
                'campus': self.campus,
                'name': self.major_name,
                'full_name': self.full_name,
                'short_name': self.short_name
                }


class Minor(RestClientsModel):
    abbr = models.CharField(max_length=50)
    campus = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)

    def json_data(self):
        return {'abbr': self.abbr,
                'campus': self.campus,
                'name': self.name,
                'full_name': self.full_name,
                'short_name': self.short_name
                }
