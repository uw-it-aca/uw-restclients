from django.test import TestCase
from django.conf import settings
from restclients.r25.events import get_event_by_id, get_events
from restclients.exceptions import DataFailureException

class R25TestEvents(TestCase):
    
    def test_event_by_id(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):
            
            event = get_event_by_id("100000")
            self.assertEquals(event.event_id, "100000", "event_id") 
            self.assertEquals(event.name, "BOTHELL WINTER 2013 CABINET", "name")
            self.assertEquals(event.title, "BOTHELL WINTER 2013 CABINET", "title")
            self.assertEquals(event.alien_uid, None, "alien_uid")
            self.assertEquals(event.start_date, "2013-01-01", "start_date")
            self.assertEquals(event.end_date, "2013-03-28", "end_date")
            self.assertEquals(event.state, "1", "state")
            self.assertEquals(event.parent_id, None, "parent_id")
            self.assertEquals(event.cabinet_id, "200000", "cabinet_id")
            self.assertEquals(event.cabinet_name, "BOTHELL WINTER 2013 CABINET", "cabinet_name")
            self.assertEquals(event.state_name(), "Tentative", "state_name")


    def test_all_events(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):

            events = get_events()
            self.assertEquals(len(events), 3, "event count")
