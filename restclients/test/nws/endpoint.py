from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException
from restclients.models import Endpoint
from unittest import skipIf

class NWSTestEndpoint(TestCase):
    #Expected values will have to change when the json files are updated
    def test_endpoint_endpoint_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            endpoint = nws.get_endpoint_by_endpoint_id("53ec7c26-19de-45ab-ba53-01b834c7fa81")
            self.assertEquals(endpoint.end_point_id, "53ec7c26-19de-45ab-ba53-01b834c7fa81")
            self.assertEquals(endpoint.end_point_uri, "/notification/v1/endpoint/53ec7c26-19de-45ab-ba53-01b834c7fa81")
            self.assertEquals(endpoint.end_point, "206-555-5555")
            self.assertEquals(endpoint.carrier, "ATT")
            self.assertEquals(endpoint.protocol, "SMS")
            self.assertEquals(endpoint.subscriber_id, "javerage")
            self.assertEquals(endpoint.owner_id, "javerage")
            self.assertEquals(endpoint.active, True)
            self.assertEquals(endpoint.default, False)

    def test_endpoint_subscriber_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            endpoints = nws.get_endpoints_by_subscriber_id("javerage")
            self.assertEquals(len(endpoints), 2)
   
    def test_create_endpoint(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            endpoint = Endpoint()
            endpoint.end_point = "206-555-5555"
            endpoint.carrier =  "ATT"
            endpoint.protocol = "SMS"
            endpoint.subscriber_id = "javerage"
            endpoint.owner_id = "javerage"
            endpoint.active = True
            endpoint.default = False

            nws = NWS()
            response_status = nws.create_new_endpoint(endpoint)
            self.assertEquals(response_status, 201)

    def test_update_endpoint(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            endpoint = Endpoint()
            endpoint.end_point_id = "53ec7c26-19de-45ab-ba53-01b834c7fa81"
            endpoint.end_point = "206-555-5555"
            endpoint.carrier =  "ATT"
            endpoint.protocol = "SMS"
            endpoint.subscriber_id = "javerage"
            endpoint.owner_id = "javerage"
            endpoint.active = True
            endpoint.default = False

            nws = NWS()
            response_status = nws.update_endpoint(endpoint)
            self.assertEquals(response_status, 204)

    def test_delete_endpoint(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            response_status = nws.delete_endpoint("53ec7c26-19de-45ab-ba53-01b834c7fa81")
            self.assertEquals(response_status, 204)
            
    @skipIf(True, "Used only for live testing")
    def test_endpoint_live(self):
        with self.settings(
                    RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            self._endpoint_subscriber_id_live()
            self._create_endpoint_live()
            self._update_endpoint_live()
            self._delete_endpoint_live()
            
    def _endpoint_subscriber_id_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            endpoints = nws.get_endpoints_by_subscriber_id("javerage")
            self.assertTrue(len(endpoints) > 0)

    def _create_endpoint_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            endpoint = Endpoint()
            endpoint.end_point_id = "cf659f2f-80e6-45fb-9b32-d77d89218107"
            endpoint.end_point = "206-555-5556"
            endpoint.carrier =  "ATT"
            endpoint.protocol = "SMS"
            endpoint.subscriber_id = "javerage"
            endpoint.owner_id = "javerage"
            endpoint.active = True
            endpoint.default = False

            nws = NWS()
            response_status = nws.create_new_endpoint(endpoint)
            self.assertEquals(response_status, 201)

    def _update_endpoint_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            endpoint = Endpoint()
            endpoint.end_point_id = "cf659f2f-80e6-45fb-9b32-d77d89218107"
            endpoint.end_point = "206-555-1111"
            endpoint.carrier =  "ATT"
            endpoint.protocol = "SMS"
            endpoint.subscriber_id = "javerage"
            endpoint.owner_id = "javerage"
            endpoint.active = True
            endpoint.default = False

            nws = NWS()
            response_status = nws.update_endpoint(endpoint)
            self.assertEquals(response_status, 204)
    
    def _delete_endpoint_live(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.Live'):
            nws = NWS()
            response_status = nws.delete_endpoint("cf659f2f-80e6-45fb-9b32-d77d89218107")
            self.assertEquals(response_status, 204)
