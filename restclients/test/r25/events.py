from django.test import TestCase
from django.conf import settings
from restclients.r25.events import get_event_by_id, get_events
from restclients.exceptions import DataFailureException
from unittest2 import skipIf

class R25TestEvents(TestCase):

    @skipIf(True, "Shouldn't be skipped")
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
            self.assertEquals(event.cabinet_id, event.event_id, "cabinet_id")
            self.assertEquals(event.cabinet_name, event.name, "cabinet_name")
            self.assertEquals(event.state_name(), "Tentative", "state_name")
            self.assertEquals(len(event.reservations), 1, "reservations")
            self.assertEquals(len(event.binding_reservations), 1, "binding_reservations")

    @skipIf(True, "Shouldn't be skipped")
    def test_parent_event(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):

            event = get_event_by_id("100002")
            parent = event.parent()
            self.assertEquals(parent.event_id, event.parent_id, "parent_id")

            # No parent event
            parent2 = parent.parent()
            self.assertEquals(parent2, None, "parent_id")

    @skipIf(True, "Shouldn't be skipped")
    def test_child_events(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):

            event = get_event_by_id("100000")
            children = event.children()
            self.assertEquals(len(children), 1, "child event count")

            # No child events
            child = children[0]
            children = child.children()
            self.assertEquals(len(children), 0, "child event count")

    @skipIf(True, "Shouldn't be skipped")
    def test_cabinet_event(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):

            event = get_event_by_id("100002")
            cabinet = event.cabinet()
            self.assertEquals(cabinet.event_id, event.cabinet_id, "cabinet_id")

            # cabinet is self
            cabinet2 = cabinet.cabinet()
            self.assertEquals(cabinet2.event_id, cabinet.event_id, "cabinet_id")

    @skipIf(True, "Shouldn't be skipped")
    def test_all_events(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):

            events = get_events()
            self.assertEquals(len(events), 3, "event count")
