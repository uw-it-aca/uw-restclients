"""
This is the interface for interacting with the UW Bookstore's book service.
"""

from restclients.dao import Book_DAO
from restclients.exceptions import DataFailureException
from restclients.models import Book, BookAuthor
import json
import re


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

        slns = []
        sln_count = 1
        for section in schedule.sections:
            slns.append("sln%s=%s" % (sln_count, section.sln))
            sln_count += 1

        sln_string = "&".join(slns)
        url = "/myuw/myuw_mobile_beta.ubs?quarter=%s&%s" % (
                                                        schedule.term.quarter,
                                                        sln_string,
                                                       )

        response = dao.getURL(url, {"Accept": "application/json"})
        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        response = {}

        for section in schedule.sections:
            response[section.sln] = []
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
                    book.authors.append(author);

                response[section.sln].append(book)

        return response
