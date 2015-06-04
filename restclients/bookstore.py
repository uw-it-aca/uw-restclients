"""
This is the interface for interacting with the UW Bookstore's book service.
"""

from restclients.dao import Book_DAO
from restclients.exceptions import DataFailureException
from restclients.models import Book, BookAuthor
import json
import re


BOOK_PREFIX = "http://uw-seattle.verbacompare.com/m?section_id="


class Bookstore(object):
    """
    Get book information for courses.
    """

    def get_books_for_schedule(self, schedule):
        """
        Returns a dictionary of data.  SLNs are the keys, an array of Book
        objects are the values.
        """
        dao = Book_DAO()

        url = self.get_books_url(schedule)

        response = dao.getURL(url, {"Accept": "application/json"})
        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        response = {}

        for section in schedule.sections:
            response[section.sln] = []
            try:
                sln_data = data[section.sln]
                for book_data in sln_data:
                    book = Book()
                    book.isbn = book_data["isbn"]
                    book.title = book_data["title"]
                    book.price = book_data["price"]
                    book.used_price = book_data["used_price"]
                    book.is_required = book_data["required"]
                    book.notes = book_data["notes"]
                    book.cover_image_url = book_data["cover_image"]
                    book.authors = []

                    for author_data in book_data["authors"]:
                        author = BookAuthor()
                        author.name = author_data["name"]
                        book.authors.append(author)

                    response[section.sln].append(book)
            except KeyError as err:
                # do nothing if bookstore has no record of book
                pass

        return response

    def get_verba_link_for_schedule(self, schedule):
        """
        Returns a link to verba.  The link varies by campus and schedule.
        Multiple calls to this with the same schedule may result in
        different urls.
        """
        dao = Book_DAO()

        url = self.get_verba_url(schedule)

        response = dao.getURL(url, {"Accept": "application/json"})
        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        for key in data:
            if re.match(r'^[A-Z]{2}[0-9]{5}$', key):
                return "%s%s&quarter=%s" % (BOOK_PREFIX,
                                            key,
                                            schedule.term.quarter)

    def get_books_url(self, schedule):
        sln_string = self._get_slns_string(schedule)
        url = "/myuw/myuw_mobile_beta.ubs?quarter=%s&%s" % (
            schedule.term.quarter,
            sln_string,
            )

        return url

    def get_verba_url(self, schedule):
        sln_string = self._get_slns_string(schedule)
        url = "/myuw/myuw_mobile_v.ubs?quarter=%s&%s" % (
            schedule.term.quarter,
            sln_string,
            )

        return url

    def _get_slns_string(self, schedule):
        slns = []
        # Prevent dupes - mainly for mock data
        seen_slns = {}
        sln_count = 1
        for section in schedule.sections:
            sln = section.sln
            if sln not in seen_slns:
                seen_slns[sln] = True
                slns.append("sln%s=%s" % (sln_count, section.sln))
                sln_count += 1

        sln_string = "&".join(slns)

        return sln_string
