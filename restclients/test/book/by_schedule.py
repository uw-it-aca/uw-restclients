from django.test import TestCase
from django.conf import settings
from restclients.bookstore import Bookstore
from restclients.sws import SWS
from unittest2 import skipIf
from restclients.sws.term import get_current_term
from restclients.sws.registration import get_schedule_by_regid_and_term
from restclients.exceptions import DataFailureException
from restclients.test import fdao_bookstore_override, fdao_pws_override,\
    fdao_sws_override


@fdao_bookstore_override
@fdao_pws_override
@fdao_sws_override
class BookstoreScheduleTest(TestCase):
    def test_get_book(self):
        books = Bookstore()

        result = books.get_books_by_quarter_sln('autumn', 19187)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].isbn, '9780878935970')

        with self.assertRaises(DataFailureException):
            books.get_books_by_quarter_sln('autumn', 00000)

    def test_get_books_by_schedule(self):
        books = Bookstore()
        term = get_current_term()
        schedule = get_schedule_by_regid_and_term(
            'AA36CCB8F66711D5BE060004AC494FFE', term)
        schedule_books = books.get_books_for_schedule(schedule)

        self.assertEquals(len(schedule_books), 2)
        self.assertEqual(len(schedule_books['13833']), 0)
        self.assertEqual(len(schedule_books['13830']), 2)

    def test_verba_link(self):
        books = Bookstore()

        term = get_current_term()
        schedule = get_schedule_by_regid_and_term(
            'AA36CCB8F66711D5BE060004AC494FFE', term)

        verba_link = books.get_verba_link_for_schedule(schedule)

        self.assertEquals(
            ("http://uw-seattle.verbacompare.com/m?" +
             "section_id=AB12345&quarter=spring"), verba_link,
            "Seattle student has seattle link")

    def test_dupe_slns(self):
        books = Bookstore()
        term = get_current_term()
        schedule = get_schedule_by_regid_and_term(
            'AA36CCB8F66711D5BE060004AC494FFE', term)

        schedule.sections.append(schedule.sections[0])
        schedule.sections.append(schedule.sections[0])
        schedule.sections.append(schedule.sections[0])
        schedule.sections.append(schedule.sections[0])
        schedule.sections.append(schedule.sections[0])

        verba_link = books.get_verba_url(schedule)

        self.assertEquals(
            verba_link,
            '/myuw/myuw_mobile_v.ubs?quarter=spring&sln1=13830&sln2=13833')

        schedule_books = books.get_books_for_schedule(schedule)
        self.assertEquals(len(schedule_books), 2)
