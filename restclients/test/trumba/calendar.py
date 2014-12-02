from django.test import TestCase
from django.conf import settings
from restclients.trumba import get_calendar_by_name


class TestCalendarParse(TestCase):
    def test_ical_parsing(self):
        with self.settings(RESTCLIENTS_CALENDAR_DAO_CLASS='restclients.dao_implementation.trumba.CalendarFile'):
            calendar = get_calendar_by_name('sea_acad-comm')
            self.assertEquals(len(calendar.walk('vevent')), 4)
