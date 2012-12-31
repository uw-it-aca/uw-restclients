from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException
from vm.v1.viewmodels import Channel
from unittest import skipIf

class NWSTestChannel(TestCase):
    def test_create_channel(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            channel = Channel()
            channel.surrogate_id = "2012,autumn,uwit,100,a"
            channel.type =  "uw_student_courseavailable"
            channel.name = "TEST CREATE CHANNEL"
            channel.description = "TEST CREATE CHANNEL \n"

            nws = NWS()
            response_status = nws.create_new_channel(channel)
            self.assertEquals(response_status, 201)

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
            channel = nws.get_channel_by_surrogate_id("uw_student_courseavailable", "2012,autumn,cse,100,w")
            self._assert_channel(channel)

    def _assert_channel(self, channel):
        self.assertEquals(channel.channel_id, "b779df7b-d6f6-4afb-8165-8dbe6232119f")
        self.assertEquals(channel.surrogate_id, "2012,autumn,cse,100,w")
        self.assertEquals(channel.type, "uw_student_courseavailable")
        self.assertEquals(channel.name, "FLUENCY IN INFORMATION TECHNOLOGY")
        self.assertEquals(channel.description, "Introduces skills, concepts, and capabilities necessary to effectively use information technology. Includes logical reasoning, managing complexity, operation of computers and networks, and contemporary applications such as effective web searching and database manipulation, ethical aspects, and social impacts of information technology. Offered: jointly with INFO 100.\n")

    @skipIf(True, "Used only for live testing")
    def test_channel_live(self):
        with self.settings(
                    RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            self._create_channel_live()
            self._channel_channel_id_live()
            self._delete_channel_live()

    def _create_channel_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            channel = Channel()
            channel.channel_id = "ce1d46fe-1cdf-4c5a-a316-20f6c99789b7"
            channel.surrogate_id = "2012,autumn,uwit,100,a"
            channel.type =  "uw_student_courseavailable"
            channel.name = "TEST CREATE CHANNEL"
            channel.template_surrogate_id = "CourseAvailableNotificationTemplate"
            channel.description = "TEST CREATE CHANNEL \n"

            nws = NWS()
            response_status = nws.create_new_channel(channel)
            self.assertEquals(response_status, 201)

    def _channel_channel_id_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            channel = nws.get_channel_by_channel_id("ce1d46fe-1cdf-4c5a-a316-20f6c99789b7")
            self.assertTrue(channel is not None)
    
    def _delete_channel_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            response_status = nws.delete_channel("ce1d46fe-1cdf-4c5a-a316-20f6c99789b7")
            self.assertEquals(response_status, 204)
