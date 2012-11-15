from django.db import models
import pickle
from base64 import b64encode, b64decode


class Person(models.Model):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)

    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    whitepages_publish = models.BooleanField()

    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    full_name = models.CharField(max_length=250)

    is_student = models.BooleanField()
    is_staff = models.BooleanField()
    is_employee = models.BooleanField()
    is_alum = models.BooleanField()
    is_faculty = models.BooleanField()

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

    def json_data(self):
        data = {
            'uwnetid': self.uwnetid,
            'uwregid': self.uwregid,
            'first_name': self.first_name,
            'surname': self.surname,
            'full_name': self.full_name,
            'whitepages_publish': self.whitepages_publish,
            'email1': self.email1,
            'email2': self.email2,
            'phone1': self.phone1,
            'phone2': self.phone2,
            'voicemail': self.voicemail,
            'fax': self.fax,
            'touchdial': self.touchdial,
            'address1': self.address1,
            'address2': self.address2,
            'mailstop': self.mailstop,
        }
        return data


class Term(models.Model):
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
    first_day_quarter = models.DateField(db_index=True)
    last_day_instruction = models.DateField(db_index=True)
    aterm_last_date = models.DateField(blank=True)
    bterm_first_date = models.DateField(blank=True)
    last_final_exam_date = models.DateField()
    grading_period_open = models.DateTimeField()
    grading_period_close = models.DateTimeField()
    grade_submission_deadline = models.DateTimeField()

    class Meta:
        unique_together = ('year',
                           'quarter')


class Section(models.Model):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    curriculum_abbr = models.CharField(max_length=6,
                                       db_index=True)
    course_number = models.PositiveSmallIntegerField(db_index=True)
    section_id = models.CharField(max_length=2,
                                  db_index=True)
    course_title = models.CharField(max_length=20)
    course_title_long = models.CharField(max_length=50)
    course_campus = models.CharField(max_length=7)
    section_type = models.CharField(max_length=30)
    class_website_url = models.URLField(max_length=255,
                                        verify_exists=False,
                                        blank=True)
    sln = models.PositiveIntegerField()
    delete_flag = models.CharField(max_length=20)
#    These are for non-standard start/end dates - don't have those yet
#    start_date = models.DateField()
#    end_date = models.DateField()

#    We don't have final exam data yet :(
#    final_exam_date = models.DateField()
#    final_exam_start_time = models.TimeField()
#    final_exam_end_time = models.TimeField()
#    final_exam_building = models.CharField(max_length=5)
#    final_exam_room_number = models.CharField(max_length=5)

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

    is_primary_section = models.BooleanField()

    class Meta:
        unique_together = ('term',
                           'curriculum_abbr',
                           'course_number',
                           'section_id')

    def section_label(self):
        return "%s,%s,%s,%s/%s" % (self.term.year,
               self.term.quarter, self.curriculum_abbr,
               self.course_number, self.section_id)

    def primary_section_label(self):
        return "%s,%s,%s,%s/%s" % (self.term.year,
               self.term.quarter, self.primary_section_curriculum_abbr,
               self.primary_section_course_number, self.primary_section_id)

    def json_data(self):
        data = {
            'curriculum_abbr': self.curriculum_abbr,
            'course_number': self.course_number,
            'section_id': self.section_id,
            'course_title': self.course_title,
            'course_campus': self.course_campus,
            'class_website_url': self.class_website_url,
            'sln': self.sln,
            'summer_term': self.summer_term,
            'start_date': '',
            'end_date': '',
            'meetings': [],
        }

        for meeting in self.meetings:
            data["meetings"].append(meeting.json_data())

        return data


class SectionMeeting(models.Model):
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)
    section = models.ForeignKey(Section,
                                on_delete=models.PROTECT)
    meeting_index = models.PositiveSmallIntegerField()
    meeting_type = models.CharField(max_length=20)
    building_to_be_arranged = models.BooleanField()
    building = models.CharField(max_length=5)
    room_to_be_arranged = models.BooleanField()
    room_number = models.CharField(max_length=5)
    days_to_be_arranged = models.BooleanField()
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)

    meets_monday = models.BooleanField()
    meets_tuesday = models.BooleanField()
    meets_wednesday = models.BooleanField()
    meets_thursday = models.BooleanField()
    meets_friday = models.BooleanField()
    meets_saturday = models.BooleanField()
    meets_sunday = models.BooleanField()
#    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)

    class Meta:
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


class ClassSchedule(models.Model):
    user = models.ForeignKey(Person)
    term = models.ForeignKey(Term,
                             on_delete=models.PROTECT)

    def json_data(self):
        data = {
            'year': self.term.year,
            'quarter': self.term.quarter,
            'sections': [],
        }

        for section in self.sections:
            data["sections"].append(section.json_data())

        return data


class Campus(models.Model):
    label = models.SlugField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50)


class College(models.Model):
    campus_label = models.SlugField(max_length=15)
    label = models.SlugField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50)


class Department(models.Model):
    college_label = models.SlugField(max_length=15)
    label = models.SlugField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50)


class Curriculum(models.Model):
    department_label = models.SlugField(max_length=15)
    label = models.SlugField(max_length=15, unique=True)
    name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50)


class CacheEntry(models.Model):
    service = models.CharField(max_length=50, db_index=True)
    url = models.CharField(max_length=255, unique=True, db_index=True)
    status = models.PositiveIntegerField()
    header_pickle = models.TextField()
    content = models.TextField()
    headers = None

    class Meta:
        unique_together = ('service', 'url')

    def getHeaders(self):
        if self.headers is None:
            if self.header_pickle is None:
                self.headers = {}
            else:
                self.headers = pickle.loads(b64decode(self.header_pickle))
        return self.headers

    def setHeaders(self, headers):
        self.headers = headers

    def save(self, *args, **kwargs):
        pickle_content = ""
        if self.headers:
            pickle_content = pickle.dumps(self.headers)
        else:
            pickle_content = pickle.dumps({})

        self.header_pickle = b64encode(pickle_content)
        super(CacheEntry, self).save(*args, **kwargs)


class CacheEntryTimed(CacheEntry):
    time_saved = models.DateTimeField()


class CacheEntryExpires(CacheEntry):
    time_expires = models.DateTimeField()


class Book(models.Model):
    isbn = models.CharField(max_length=15)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    used_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_required = models.BooleanField()
    notes = models.TextField()
    cover_image_url = models.CharField(max_length=2048)

    def json_data(self):
        data = {
            'isbn': self.isbn,
            'title': self.title,
            'authors': [],
            'price': self.price,
            'used_price': self.used_price,
            'is_required': self.is_required,
            'notes': self.notes,
            'cover_image_url': self.cover_image_url,
        }

        for author in self.authors:
            data["authors"].append(author.json_data())
        return data


class BookAuthor(models.Model):
    name = models.CharField(max_length=255)

    def json_data(self):
        data = {'name': self.name}

        return data


class Group(models.Model):
    regid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)

    name = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)


class CourseGroup(Group):
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

    curriculum_abbreviation = models.CharField(max_length=8)
    course_number = models.CharField(max_length=3)
    year = models.PositiveSmallIntegerField()
    quarter = models.CharField(max_length=6,
                               choices=QUARTERNAME_CHOICES)
    section_id = models.CharField(max_length=2,
                                  db_index=True)

    sln = models.PositiveIntegerField()


class MockAmazonSQSQueue(models.Model):
    name = models.CharField(max_length=80, unique=True, db_index=True)

    def new_message(self, body=""):
        message = MockAmazonSQSMessage()
        message.body = body
        message.queue = self
        return message

    def write(self, message):
        message.save()
        return message

    def read(self):
        rs = self.get_messages(1)
        if len(rs) == 1:
            return rs[0]
        else:
            return None

    def delete_message(self, message):
        message.delete()
        return True

    def get_messages(self, num_messages=1):
        rs = MockAmazonSQSMessage.objects.filter(queue=self)
        rs = rs.order_by('pk')
        rs = rs[0:num_messages]

        return rs


class MockAmazonSQSMessage(models.Model):
    body = models.CharField(max_length=8192)
    queue = models.ForeignKey(MockAmazonSQSQueue,
                             on_delete=models.PROTECT)

    def get_body(self):
        return self.body


class SMSRequest(models.Model):
    body = models.CharField(max_length=8192)
    to = models.CharField(max_length=40)
    from_number = models.CharField(max_length=40)

    def get_body(self):
        return self.body

    def get_to(self):
        return self.to

    def get_from_number(self):
        return self.from_number


class SMSResponse(models.Model):
    body = models.CharField(max_length=8192)
    to = models.CharField(max_length=40)
    status = models.CharField(max_length=8192)
    #all sms requests have some sort of response id
    rid = models.CharField(max_length=8192)

    def get_body(self):
        return self.body

    def get_to(self):
        return self.to

    def get_status(self):
        return self.status

    def get_rid(self):
        return self.id

class Subscription(models.Model):
    #PrimaryKey
    subscription_id = models.CharField(max_length=36, db_index=True)
    channel_id = models.CharField(max_length=36)
    end_point = models.CharField(max_length=255)
    protocol = models.CharField(max_length=40)
    subscriber_id = models.CharField(max_length=80)
    owner_id = models.CharField(max_length=80)

    def json_data(self):
        return {
            "ChannelID": self.channel_id,
            "EndPoint": self.end_point,
            "Protocol": self.protocol,
            "SubscriberID": self.subscriber_id,
            "SubscriptionID": self.subscription_id,
        }

class Channel(models.Model):
    channel_id = models.CharField(max_length=36)
    surrogate_id = models.CharField(max_length=140)
    type = models.CharField(max_length=140)
    name = models.CharField(max_length=255)
    template_surrogate_id = models.CharField(max_length=140)
    description = models.TextField()
    expires = models.DateTimeField(blank=True)
    last_modified = models.DateTimeField()


class Notification(models.Model):
    subject = models.CharField(max_length=8192)
    short = models.CharField(max_length=140) #SMS max body length
    full = models.CharField(max_length=8192)  


class CourseAvailableEvent(models.Model):
    status = models.CharField(max_length=10)
    space_available = models.PositiveIntegerField()
    term = models.ForeignKey(Term)
    curriculum_abbr = models.CharField(max_length=6)
    course_number = models.PositiveSmallIntegerField()
    section_id = models.CharField(max_length=2)


class CanvasEnrollment(models.Model):
    course_url = models.CharField(max_length=2000)
    sis_id = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)

    def sws_course_id(self):
        parts = self.sis_id.split("-")

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                    parts[4])

        return sws_id


class CanvasCourse(models.Model):
    course_url = models.CharField(max_length=2000)
    sis_id = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)

    def sws_course_id(self):
        parts = self.sis_id.split("-")

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                    parts[4])

        return sws_id
