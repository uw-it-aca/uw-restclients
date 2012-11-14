from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException


class NWSTestChannel(TestCase):
    #Expected values will have to change when the json files are updated
    def test_channel_channel_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            channel = nws.get_channel_by_channel_id("b779df7b-d6f6-4afb-8165-8dbe6232119f")
            self._assert_channel(channel)

    def test_channel_sln(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            channels = nws.get_channels_by_sln("uw_student_courseavailable", "12345")
            self.assertEquals(len(channels), 1)

    def test_channel_surrogate_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            channel = nws.get_channels_by_surrogate_id("uw_student_courseavailable", "2012,autumn,cse,100,w")
            self._assert_channel(channel)

    def _assert_channel(self, channel):
        self.assertEquals(channel.channel_id, "b779df7b-d6f6-4afb-8165-8dbe6232119f")
        self.assertEquals(channel.surrogate_id, "2012,autumn,cse,100,w")
        self.assertEquals(channel.type, "uw_student_courseavailable")
        self.assertEquals(channel.name, "FLUENCY IN INFORMATION TECHNOLOGY")
        self.assertEquals(channel.template_surrogate_id, "CourseAvailableNotificationTemplate")
        self.assertEquals(channel.description, "Introduces skills, concepts, and capabilities necessary to effectively use information technology. Includes logical reasoning, managing complexity, operation of computers and networks, and contemporary applications such as effective web searching and database manipulation, ethical aspects, and social impacts of information technology. Offered: jointly with INFO 100.\n")
        self.assertEquals(str(channel.expires), "2012-11-13 22:51:51+00:00")
        self.assertEquals(str(channel.last_modified), "2012-11-13 22:51:51+00:00")
