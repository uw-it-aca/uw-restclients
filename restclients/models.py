from django.db import models

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



    def json_data(self):
        data = {
            'uwnetid': self.uwnetid,
            'uwregid': self.uwregid,
            'first_name': self.first_name,
            'surname': self.surname,
            'full_name': self.full_name,
            'whitepages_publish': self.whitepages_publish,
        }
        return data

class Term(models.Model):
    year = models.PositiveSmallIntegerField()
    QUARTERNAME_CHOICES = (
        ('1', 'Winter'),
        ('2', 'Spring'),
        ('3', 'Summer'),
        ('4', 'Autumn')
        )
    quarter = models.CharField(max_length=1,
                               choices=QUARTERNAME_CHOICES)
    first_day_quarter = models.DateField(db_index=True)
    last_day_instruction = models.DateField(db_index=True)
    aterm_last_date = models.DateField()
    bterm_first_date = models.DateField()
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
    course_campus = models.CharField(max_length=7)
    section_type = models.CharField(max_length=2)
    class_website_url = models.URLField(max_length=255,
                              verify_exists=False)
    sln = models.PositiveIntegerField()
    summer_term = models.CharField(max_length=1)
    start_date = models.DateField()
    end_date = models.DateField()
    final_exam_date = models.DateField()
    final_exam_start_time = models.TimeField()
    final_exam_end_time = models.TimeField()
    final_exam_building = models.CharField(max_length=5)
    final_exam_room_number = models.CharField(max_length=5)
    class Meta:
        unique_together = ('term',
                           'curriculum_abbr',
                           'course_number',
                           'section_id')

    def section_label(self):
        return "%s,%s,%s,%s/%s" % (self.term.year,
            self.term.quarter, self.curriculum_abbr,
            self.course_number, self.section_id)

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
            'meetings': []
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
    meeting_type = models.CharField(max_length=2)
    building_to_be_arranged = models.BooleanField()
    building = models.CharField(max_length=5)
    room_to_be_arranged = models.BooleanField()
    room_number = models.CharField(max_length=5)
    days_to_be_arranged = models.BooleanField()
    days_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
#    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    last_verified = models.DateTimeField()
    class Meta:
        unique_together = ('term',
                           'section',
                           'meeting_index')

    def json_data(self):
        data = {
            'index': self.meeting_index,
            'type': self.meeting_type,
            'days_tbd': self.days_to_be_arranged,
            'days': self.days_week,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'building_tbd': self.building_to_be_arranged,
            'building': self.building,
            'room_tbd': self.room_to_be_arranged,
            'room': self.room_number,
            'instructors': [],
            'instructor': {
                'name': 'This isnt real',
                'email': 'fake@fake.fake',
                'phone': '206-...',
            }
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
