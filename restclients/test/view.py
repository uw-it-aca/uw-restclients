from django.test import TestCase
from restclients.views import clean_self_closing_divs

class ViewTest(TestCase):
    def test_simple(self):
        self_closed = "<div/>"
        valid = "<!-- <div/> --><div></div>"

        self.assertEquals(valid, clean_self_closing_divs(self_closed))

    def test_2_simple(self):
        self_closed = "<div/><div/>"
        valid = "<!-- <div/> --><div></div><!-- <div/> --><div></div>"

        self.assertEquals(valid, clean_self_closing_divs(self_closed))

    def test_valid_div(self):
        valid = "<div id='test id'></div>"
        self.assertEquals(valid, clean_self_closing_divs(valid))

    def test_div_then_valid_self_closing(self):
        valid = "<div id='test id'></div><br/>"
        self.assertEquals(valid, clean_self_closing_divs(valid))
