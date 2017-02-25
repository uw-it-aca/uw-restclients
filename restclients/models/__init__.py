from restclients_core import models
from django.db import models as dj_models
import pickle
from base64 import b64encode, b64decode
import warnings

from restclients.models.base import RestClientsModel, RestClientsDjangoModel
from restclients.models.sws import Term as swsTerm
from restclients.models.sws import Person as swsPerson
from restclients.models.sws import FinalExam as swsFinalExam
from restclients.models.sws import Section as swsSection
from restclients.models.sws import SectionMeeting as swsSectionMeeting
from restclients.models.sws import ClassSchedule as swsClassSchedule
from restclients.models.sws import Campus as swsCampus
from restclients.models.sws import College as swsCollege
from restclients.models.sws import Department as swsDepartment
from restclients.models.sws import Curriculum as swsCurriculum
from restclients.models.gws import GroupReference as gwsGroupReference
from restclients.models.gws import Group as gwsGroup
from restclients.models.gws import CourseGroup as gwsCourseGroup
from restclients.models.gws import GroupUser as gwsGroupUser
from restclients.models.gws import GroupMember as gwsGroupMember
from restclients.models.canvas import CanvasCourse as canvasCourse
from restclients.models.canvas import CanvasEnrollment as canvasEnrollment


# These aliases are here for backwards compatibility
def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


def Person(*args, **kwargs):
    deprecation("Use restclients.models.sws.Person")
    return swsPerson(*args, **kwargs)


def Term(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsTerm(*args, **kwargs)


def FinalExam(*args, **kwargs):
    deprecation("Use restclients.models.sws.FinalExam")
    return swsFinalExam(*args, **kwargs)


def Section(*args, **kwargs):
    deprecation("Use restclients.models.sws.Section")
    return swsSection(*args, **kwargs)


def SectionMeeting(*args, **kwargs):
    deprecation("Use restclients.models.sws.SectionMeeting")
    return swsSectionMeeting(*args, **kwargs)


def ClassSchedule(*args, **kwargs):
    deprecation("Use restclients.models.sws.ClassSchedule")
    return swsClassSchedule(*args, **kwargs)


def Campus(*args, **kwargs):
    deprecation("Use restclients.models.sws.Campus")
    return swsCampus(*args, **kwargs)


def College(*args, **kwargs):
    deprecation("Use restclients.models.sws.College")
    return swsCollege(*args, **kwargs)


def Department(*args, **kwargs):
    deprecation("Use restclients.models.sws.Department")
    return swsDepartment(*args, **kwargs)


def Curriculum(*args, **kwargs):
    deprecation("Use restclients.models.sws.Curriculum")
    return swsCurriculum(*args, **kwargs)


def GroupReference(*args, **kwargs):
    deprecation("Use restclients.models.gws.GroupReference")
    return gwsGroupReference(*args, **kwargs)


def Group(*args, **kwargs):
    deprecation("Use restclients.models.gws.Group")
    return gwsGroup(*args, **kwargs)


def CourseGroup(*args, **kwargs):
    deprecation("Use restclients.models.gws.CourseGroup")
    return gwsCourseGroup(*args, **kwargs)


def GroupUser(*args, **kwargs):
    deprecation("Use restclients.models.gws.GroupUser")
    return gwsGroupUser(*args, **kwargs)


def GroupMember(*args, **kwargs):
    deprecation("Use restclients.models.gws.GroupMember")
    return gwsGroupMember(*args, **kwargs)


def CanvasCourse(*args, **kwargs):
    deprecation("Use restclients.models.canvas.CanvasCourse")
    return canvasCourse(*args, **kwargs)


def CanvasEnrollment(*args, **kwargs):
    deprecation("Use restclients.models.canvas.CanvasEnrollment")
    return canvasEnrollment(*args, **kwargs)


class CacheEntry(RestClientsDjangoModel):
    service = dj_models.CharField(max_length=50, db_index=True)
    url = dj_models.CharField(max_length=255, unique=True, db_index=True)
    status = dj_models.PositiveIntegerField()
    header_pickle = dj_models.TextField()
    content = dj_models.TextField()
    headers = None

    class Meta(RestClientsDjangoModel.Meta):
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
    def __init__(self,  *args, **kwargs):
        super(RestClientsDjangoModel, self).__init__(*args, **kwargs)
    time_saved = dj_models.DateTimeField()


class CacheEntryExpires(CacheEntry):
    time_expires = dj_models.DateTimeField()


class Book(RestClientsModel):
    isbn = models.CharField(max_length=15)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    used_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_required = models.NullBooleanField()
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


class BookAuthor(RestClientsModel):
    name = models.CharField(max_length=255)

    def json_data(self):
        data = {'name': self.name}

        return data


class MockAmazonSQSQueue(RestClientsDjangoModel):
    name = dj_models.CharField(max_length=80, unique=True, db_index=True)

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

    def set_message_class(self, message_class):
        pass


class MockAmazonSQSMessage(RestClientsDjangoModel):
    body = dj_models.CharField(max_length=8192)
    queue = dj_models.ForeignKey(MockAmazonSQSQueue,
                                 on_delete=models.PROTECT)

    def get_body(self):
        return self.body


class SMSRequest(RestClientsDjangoModel):
    body = dj_models.CharField(max_length=8192)
    to = dj_models.CharField(max_length=40)
    from_number = dj_models.CharField(max_length=40)

    def get_body(self):
        return self.body

    def get_to(self):
        return self.to

    def get_from_number(self):
        return self.from_number


class SMSResponse(RestClientsModel):
    body = models.TextField(max_length=8192)
    to = models.TextField(max_length=40)
    status = models.TextField(max_length=8192)
    # all sms requests have some sort of response id
    rid = models.TextField(max_length=8192)

    def get_body(self):
        return self.body

    def get_to(self):
        return self.to

    def get_status(self):
        return self.status

    def get_rid(self):
        return self.id


class Notification(RestClientsModel):
    subject = models.CharField(max_length=8192)
    short = models.CharField(max_length=140)  # SMS max body length
    full = models.CharField(max_length=8192)


class CourseAvailableEvent(RestClientsModel):
    event_id = models.CharField(max_length=40)
    event_create_date = models.CharField(max_length=40)
    message_timestamp = models.CharField(max_length=40)
    space_available = models.PositiveIntegerField()
    quarter = models.CharField(max_length=6)
    year = models.PositiveSmallIntegerField()
    curriculum_abbr = models.CharField(max_length=6)
    course_number = models.CharField(max_length=3)
    section_id = models.CharField(max_length=2)
    sln = models.PositiveSmallIntegerField()
    notification_msg_0 = models.CharField(max_length=40)

    def get_logging_description(self):
        return "%s,%s,%s,%s/%s - %s" % (
            self.year,
            self.quarter,
            self.curriculum_abbr,
            self.course_number,
            self.section_id
        )

    def get_surrogate_id(self):
        """
        This is responsible for building the surrogate id from the model
        """
        surrogate_id = "%s,%s,%s,%s,%s" % (self.year,
                                           self.quarter,
                                           self.curriculum_abbr.lower(),
                                           self.course_number,
                                           self.section_id.lower())

        return surrogate_id

    def json_data(self):
        return{
            "Event": {
                "EventID": self.event_id,
                "EventCreateDate": self.event_create_date,
                "Section": {
                    "Course": {
                        "CourseNumber": self.course_number,
                        "CurriculumAbbreviation": self.curriculum_abbr.upper(),
                        "Quarter": self.quarter,
                        "Year": self.year
                    },
                    "SLN": self.sln,
                    "SectionID": self.section_id.upper()
                },
                "SpaceAvailable": self.space_available,
                "NotificationMsg0": self.notification_msg_0
            }
        }
