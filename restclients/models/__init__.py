from django.db import models
import pickle
from base64 import b64encode, b64decode
import warnings

from restclients.models.sws import Term as swsTerm
from restclients.models.sws import Person as swsPerson
from restclients.models.sws import Section as swsSection
from restclients.models.sws import SectionMeeting as swsSectionMeeting
from restclients.models.sws import ClassSchedule as swsClassSchedule
from restclients.models.sws import Campus as swsCampus
from restclients.models.sws import College as swsCollege
from restclients.models.sws import Department as swsDepartment
from restclients.models.sws import Curriculum as swsCurriculum


# These aliases are here for backwards compatibility
def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)

def Person(*args, **kwargs):
    deprecation("Use restclients.models.sws.Person")
    return swsPerson(*args, **kwargs)

def Term(*args, **kwargs):
    deprecation("Use restclients.models.sws.Person")
    return swsTerm(*args, **kwargs)

def Section(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsSection(*args, **kwargs)

def SectionMeeting(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsSectionMeeting(*args, **kwargs)

def ClassSchedule(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsClassSchedule(*args, **kwargs)

def Campus(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsCampus(*args, **kwargs)

def College(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsCollege(*args, **kwargs)

def Department(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsDepartment(*args, **kwargs)

def Curriculum(*args, **kwargs):
    deprecation("Use restclients.models.sws.Term")
    return swsCurriculum(*args, **kwargs)


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

    def set_message_class(self, message_class):
        pass

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
            "Endpoint": self.end_point,
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
    #TODO: Need to learn how to use the Section and Term model instead
    quarter = models.CharField(max_length=6)
    year = models.PositiveSmallIntegerField()
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

