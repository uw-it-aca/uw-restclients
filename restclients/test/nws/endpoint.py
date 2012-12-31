from django.test import TestCase
from django.conf import settings
from restclients.nws import NWS
from restclients.exceptions import DataFailureException
from vm.v1.viewmodels import Endpoint

class NWSTestEndpoint(TestCase):
    
    def _assert_endpoint_matches(self, endpoint):
        self.assertEquals('780f2a49-2118-4969-9bef-bbd38c26970a', endpoint.endpoint_id)
        self.assertEquals('/notification/v1/endpoint/780f2a49-2118-4969-9bef-bbd38c26970a', endpoint.endpoint_uri)
        self.assertEquals('222-222-3333', endpoint.endpoint_address)
        self.assertEquals('AT&T', endpoint.carrier)
        self.assertEquals('sms', endpoint.protocol)
        self.assertEquals('javerage', endpoint.subscriber_id)
        self.assertEquals('sdf', endpoint.owner_id)
        self.assertEquals(False, endpoint.active)
        self.assertEquals(False, endpoint.default)
        
    
    def test_endpoint_endpoint_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            endpoint = nws.get_endpoint_by_endpoint_id("780f2a49-2118-4969-9bef-bbd38c26970a")
            self._assert_endpoint_matches(endpoint)
    
    def test_endpoint_search_by_subscriber_id(self):
        with self.settings(
                RESTCLIENTS_NWS_DAO_CLASS='restclients.dao_implementation.nws.File'):
            nws = NWS()
            endpoints = nws.get_endpoints_by_subscriber_id("javerage")
            self.assertEquals(len(endpoints), 2)
            
            endpoint = endpoints[0]
            self._assert_endpoint_matches(endpoint)
            