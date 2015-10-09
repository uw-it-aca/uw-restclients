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
    def get_books_by_quarter_sln(self, quarter, sln):
        dao = Book_DAO()
        sln_string = self._get_sln_string(sln)
        url = "/myuw/myuw_mobile_beta.ubs?quarter=%s&%s" % (
            quarter,
            sln_string,
            )
        response = dao.getURL(url, {"Accept": "application/json"})
        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        books = []

        sln_data = data[str(sln)]

        if len(sln_data) > 0:
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

                    books.append(book)
        return books

    def get_books_for_schedule(self, schedule):
        """
        Returns a dictionary of data.  SLNs are the keys, an array of Book
        objects are the values.
        """
        slns = self._get_slns(schedule)

        books = {}

        for sln in slns:
            try:
                section_books = self.get_books_by_quarter_sln(
                    schedule.term.quarter, sln
                )
                books[sln] = section_books
            except DataFailureException:
                # do nothing if bookstore doesn't have sln
                pass
        return books

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

    def get_verba_url(self, schedule):
        sln_string = self._get_slns_string(schedule)
        url = "/myuw/myuw_mobile_v.ubs?quarter=%s&%s" % (
            schedule.term.quarter,
            sln_string,
            )

        return url

    def _get_sln_string(self, sln):
        return "sln1=%s" % sln

    def _get_slns(self, schedule):
        slns = []
        # Prevent dupes - mainly for mock data
        seen_slns = {}
        for section in schedule.sections:
            sln = section.sln
            if sln not in seen_slns:
                seen_slns[sln] = True
                slns.append(sln)

        return slns

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
