from django.test import TestCase
from datetime import date, datetime, timedelta
from restclients.util.date_formator import full_month_date_str
from restclients.util.date_formator import abbr_month_date_time_str
from restclients.util.date_formator import abbr_week_month_day_str
from restclients.util.date_formator import last_midnight, time_str, is_today
from restclients.util.date_formator import is_days_ago, is_over_weeks_ago
from restclients.util.date_formator import is_over_years_ago, is_over_months_ago
from restclients.util.date_formator import past_datetime_str


class formatorTest(TestCase):


    def test_full_month_date_str(self):
        
        self.assertEquals(full_month_date_str(date(2014, 7, 4)),
                          'July 4, 2014')
        
        self.assertEquals(full_month_date_str(date(2014, 6, 12)),
                          'June 12, 2014')
                                            

    def test_time_str(self):
        self.assertEquals(time_str(datetime(2014, 7, 4, 0, 0)), '12:00 AM')
        self.assertEquals(time_str(datetime(2014, 7, 4, 3, 3)), '3:03 AM')
        self.assertEquals(time_str(datetime(2014, 7, 4, 12, 0)), '12:00 PM')
        self.assertEquals(time_str(datetime(2014, 7, 4, 13, 3)), '1:03 PM')
        self.assertEquals(time_str(datetime(2014, 7, 4, 23, 59)), '11:59 PM')


    def test_abbr_month_date_time_str(self):
        self.assertEquals(abbr_month_date_time_str(datetime(2014, 7, 4, 3, 3)),
                          'Jul 4, 2014 at 3:03 AM')
        
        self.assertEquals(abbr_month_date_time_str(datetime(2014, 6, 12, 17, 55)),
                          'Jun 12, 2014 at 5:55 PM')
                                            

    def test_abbr_week_month_day_str(self):
        self.assertEquals(abbr_week_month_day_str(datetime(2014, 7, 4)),
                          'Fri, Jul 4')
        self.assertEquals(abbr_week_month_day_str(datetime(2014, 6, 12)),
                          'Thu, Jun 12')
        self.assertEquals(abbr_week_month_day_str(datetime(2014, 6, 14)),
                          'Sat, Jun 14')
        self.assertEquals(abbr_week_month_day_str(datetime(2014, 6, 15)),
                          'Sun, Jun 15')
        self.assertEquals(abbr_week_month_day_str(datetime(2014, 6, 16)),
                          'Mon, Jun 16')
        self.assertEquals(abbr_week_month_day_str(datetime(2014, 6, 17)),
                          'Tue, Jun 17')
        self.assertEquals(abbr_week_month_day_str(datetime(2014, 6, 18)),
                          'Wed, Jun 18')
                                            

    def test_last_midnight(self):
        now = datetime.now()
        self.assertEquals(last_midnight(),
                          datetime(now.year, now.month, now.day, 0, 0, 0, 0))


    def test_is_today(self):
        now = datetime.now() 
        self.assertTrue(is_today(now))
        self.assertTrue(is_today(last_midnight()))
        self.assertTrue(is_today(last_midnight()+timedelta(seconds=1)))
        self.assertFalse(is_today(last_midnight()-timedelta(seconds=1)))
        self.assertFalse(is_today(now-timedelta(days=1)))


    def test_is_yesterday(self):
        now = datetime.now() 
        self.assertFalse(is_days_ago(last_midnight()+timedelta(seconds=1), 1))
        self.assertTrue(is_days_ago(last_midnight(), 1))
        self.assertTrue(is_days_ago(now-timedelta(days=1), 1))
        self.assertTrue(
            is_days_ago(last_midnight()-timedelta(days=1)+timedelta(seconds=1), 1))
        self.assertTrue(is_days_ago(last_midnight()-timedelta(days=1), 1))
        self.assertFalse(
            is_days_ago(last_midnight()-timedelta(days=1)-timedelta(seconds=1), 1))
        self.assertFalse(is_days_ago(now-timedelta(days=2), 1))


    def test_is_days_ago(self):
        now = datetime.now() 
        self.assertTrue(is_days_ago(last_midnight()-timedelta(days=1), 2))
        self.assertTrue(
            is_days_ago(last_midnight()-timedelta(days=1)-timedelta(seconds=1), 2))
        self.assertTrue(is_days_ago(now-timedelta(days=2), 2))
        self.assertTrue(is_days_ago(last_midnight()-timedelta(days=2), 2))
        self.assertFalse(
            is_days_ago(last_midnight()-timedelta(days=2)-timedelta(seconds=1), 2))

        self.assertTrue(is_days_ago(now-timedelta(days=3), 3))
        self.assertTrue(is_days_ago(now-timedelta(days=4), 4))
        self.assertTrue(is_days_ago(now-timedelta(days=5), 5))
        self.assertTrue(is_days_ago(now-timedelta(days=6), 6))


    def test_is_a_week_ago(self):
        now = datetime.now() 
        self.assertFalse(
            is_days_ago(last_midnight()-timedelta(days=6)+timedelta(seconds=1),7))
        self.assertTrue(is_days_ago(last_midnight()-timedelta(days=6),7))
        self.assertTrue(
            is_days_ago(last_midnight()-timedelta(days=7)+timedelta(seconds=1),7))
        self.assertTrue(is_days_ago(now-timedelta(weeks=1),7))
        self.assertTrue(is_days_ago(now-timedelta(days=7),7))
        self.assertFalse(
            is_days_ago(last_midnight()-timedelta(days=7)-timedelta(seconds=1),7))
        self.assertFalse(is_days_ago(now-timedelta(days=8),7))


    def test_is_over_1_week_ago(self):
        now = datetime.now() 
        self.assertFalse(
            is_over_weeks_ago(now-timedelta(days=7), 1))
        self.assertFalse(
            is_over_weeks_ago(last_midnight()-timedelta(days=7)+timedelta(seconds=1), 1))
        self.assertTrue(
            is_over_weeks_ago(last_midnight()-timedelta(days=7), 1))
        self.assertTrue(is_over_weeks_ago(now-timedelta(days=8), 1))
        self.assertTrue(is_over_weeks_ago(now-timedelta(days=14), 1))
        self.assertTrue(
            is_over_weeks_ago(last_midnight()-timedelta(days=14), 1))
        self.assertFalse(
            is_over_weeks_ago(last_midnight()-timedelta(days=14)-timedelta(seconds=1), 1))
        self.assertFalse(is_over_weeks_ago(now-timedelta(days=15), 1))


    def test_is_over_2_weeks_ago(self):
        now = datetime.now() 
        self.assertFalse(is_over_weeks_ago(now-timedelta(days=14), 2))
        self.assertTrue(is_over_weeks_ago(last_midnight()-timedelta(days=14), 2))
        self.assertTrue(is_over_weeks_ago(now-timedelta(days=15), 2))
        self.assertTrue(
            is_over_weeks_ago(last_midnight()-timedelta(days=21)+timedelta(seconds=1), 2))
        self.assertTrue(is_over_weeks_ago(now-timedelta(days=21), 2))
        self.assertTrue(is_over_weeks_ago(last_midnight()-timedelta(days=21), 2))
        self.assertFalse(
            is_over_weeks_ago(last_midnight()-timedelta(days=21)-timedelta(seconds=1), 2))
        self.assertFalse(is_over_weeks_ago(now-timedelta(days=22), 2))

    def test_is_over_3_weeks_ago(self):
        now = datetime.now() 
        self.assertFalse(is_over_weeks_ago(now-timedelta(days=21), 3))
        self.assertTrue(is_over_weeks_ago(last_midnight()-timedelta(days=21), 3))
        self.assertTrue(is_over_weeks_ago(now-timedelta(days=22), 3))
        self.assertTrue(is_over_weeks_ago(now-timedelta(days=27), 3))
        self.assertTrue(is_over_weeks_ago(now-timedelta(days=28), 3))
        self.assertTrue(is_over_weeks_ago(last_midnight()-timedelta(days=28), 3))
        self.assertFalse(
            is_over_weeks_ago(last_midnight()-timedelta(days=28)-timedelta(seconds=1), 3))
        self.assertFalse(is_over_weeks_ago(now-timedelta(days=29), 3))


    def test_is_over_1_month_ago(self):
        now = datetime.now()
        self.assertFalse(is_over_weeks_ago(now-timedelta(days=28), 1))
        self.assertFalse(
            is_over_months_ago(last_midnight()-timedelta(days=28)+timedelta(seconds=1), 1))
        self.assertTrue(is_over_months_ago(last_midnight()-timedelta(days=28), 1))
        self.assertTrue(is_over_months_ago(now-timedelta(days=29), 1))
        self.assertTrue(is_over_months_ago(now-timedelta(days=56), 1))
        self.assertTrue(is_over_months_ago(last_midnight()-timedelta(days=56), 1))
        self.assertFalse(
            is_over_months_ago(last_midnight()-timedelta(days=56)-timedelta(seconds=1), 1))
        self.assertFalse(is_over_months_ago(now-timedelta(days=57), 1))

    def test_is_over_2_months_ago(self):
        now = datetime.now()
        self.assertFalse(is_over_weeks_ago(now-timedelta(days=56), 2))
        self.assertFalse(
            is_over_months_ago(last_midnight()-timedelta(days=56)+timedelta(seconds=1), 2))
        self.assertTrue(
            is_over_months_ago(last_midnight()-timedelta(days=56), 2))
        self.assertTrue(is_over_months_ago(now-timedelta(days=57), 2))
        self.assertTrue(is_over_months_ago(now-timedelta(days=84), 2))
        self.assertTrue(is_over_months_ago(last_midnight()-timedelta(weeks=12), 2))
        self.assertFalse(
            is_over_months_ago(last_midnight()-timedelta(days=84)-timedelta(seconds=1), 2))
        self.assertFalse(is_over_months_ago(now-timedelta(days=85), 2))

    def test_is_over_3_months_ago(self):
        now = datetime.now()
        self.assertFalse(is_over_months_ago(now-timedelta(days=84), 3))
        self.assertFalse(
            is_over_months_ago(last_midnight()-timedelta(days=84)+timedelta(seconds=1), 3))
        self.assertTrue(is_over_months_ago(last_midnight()-timedelta(days=84), 3))
        self.assertTrue(is_over_months_ago(now-timedelta(days=85), 3))
        self.assertTrue(is_over_months_ago(now-timedelta(days=112), 3))
        self.assertTrue(is_over_months_ago(last_midnight()-timedelta(days=112), 3))
        self.assertFalse(
            is_over_months_ago(last_midnight()-timedelta(days=112)-timedelta(seconds=1), 3))
        self.assertFalse(is_over_months_ago(now-timedelta(days=113), 3))


    def test_is_over_1_year_ago(self):
        now = datetime.now()
        self.assertFalse(is_over_years_ago(now-timedelta(days=365), 1))
        self.assertTrue(is_over_years_ago(last_midnight()-timedelta(days=365), 1))
        self.assertTrue(is_over_years_ago(now-timedelta(days=366), 1))
        self.assertTrue(is_over_years_ago(now-timedelta(days=365*2), 1))
        self.assertTrue(is_over_years_ago(last_midnight()-timedelta(days=365*2), 2))
        self.assertFalse(is_over_years_ago(now-timedelta(days=731), 1))

    def test_is_over_2_years_ago(self):
        now = datetime.now()
        self.assertFalse(is_over_years_ago(now-timedelta(days=365*2), 2))
        self.assertTrue(is_over_years_ago(last_midnight()-timedelta(days=365*2), 2))
        self.assertTrue(is_over_years_ago(now-timedelta(days=731), 2))
        self.assertTrue(is_over_years_ago(now-timedelta(days=1095), 2))
        self.assertTrue(is_over_years_ago(last_midnight()-timedelta(days=365*3), 2))
        self.assertFalse(is_over_years_ago(now-timedelta(days=1096), 2))

            
    def test_past_datetime_str_today(self):
        now = datetime.now()
        t1 = datetime(now.year, now.month, now.day, 0, 0, 0)
        self.assertEquals(past_datetime_str(t1), 'today at 12:00 AM')
        t1 = datetime(now.year, now.month, now.day, 1)
        self.assertEquals(past_datetime_str(t1), 'today at 1:00 AM')
        t1 = datetime(now.year, now.month, now.day, 11)
        self.assertEquals(past_datetime_str(t1), 'today at 11:00 AM')
        t1 = datetime(now.year, now.month, now.day, 12)
        self.assertEquals(past_datetime_str(t1), 'today at 12:00 PM')
        t1 = datetime(now.year, now.month, now.day, 13)
        self.assertEquals(past_datetime_str(t1), 'today at 1:00 PM')


    def test_past_datetime_str_yesterday(self):
        day = datetime.now() - timedelta(days=1)
        t2 = datetime(day.year, day.month, day.day, 0, 0, 0)
        self.assertEquals(past_datetime_str(t2), 'yesterday at 12:00 AM')
        t2 = datetime(day.year, day.month, day.day, 1,)
        self.assertEquals(past_datetime_str(t2), 'yesterday at 1:00 AM') 


    def test_past_datetime_str_days_ago(self):
        day = datetime.now() - timedelta(days=2)
        self.assertEquals(past_datetime_str(day), '2 days ago') 

        day = datetime.now() - timedelta(days=3)
        self.assertEquals(past_datetime_str(day), '3 days ago') 

        day = datetime.now() - timedelta(days=4)
        self.assertEquals(past_datetime_str(day), '4 days ago') 

        day = datetime.now() - timedelta(days=5)
        self.assertEquals(past_datetime_str(day), '5 days ago') 

        day = datetime.now() - timedelta(days=6)
        self.assertEquals(past_datetime_str(day), '6 days ago') 


    def test_past_datetime_str_a_week_ago(self):
        day = datetime.now() - timedelta(days=7)
        self.assertEquals(past_datetime_str(day), '1 week ago') 

    def test_past_datetime_str_over_weeks_ago(self):
        day = datetime.now() - timedelta(days=8)
        self.assertEquals(past_datetime_str(day), 'over 1 week ago') 
        day = datetime.now() - timedelta(days=14) 
        self.assertEquals(past_datetime_str(day), 'over 1 week ago') 
        day = last_midnight() - timedelta(days=14) 
        self.assertEquals(past_datetime_str(day), 'over 1 week ago') 

        day = datetime.now() - timedelta(days=15) 
        self.assertEquals(past_datetime_str(day), 'over 2 weeks ago') 
        day = datetime.now() - timedelta(days=21) 
        self.assertEquals(past_datetime_str(day), 'over 2 weeks ago') 
        day = last_midnight() - timedelta(days=21)
        self.assertEquals(past_datetime_str(day), 'over 2 weeks ago') 

        day = datetime.now() - timedelta(days=22)
        self.assertEquals(past_datetime_str(day), 'over 3 weeks ago') 
        day = datetime.now() - timedelta(days=28)
        self.assertEquals(past_datetime_str(day), 'over 3 weeks ago') 

    def test_past_datetime_str_over_months_ago(self):
        day = datetime.now() - timedelta(days=29)
        self.assertEquals(past_datetime_str(day), 'over 1 month ago') 
        day = datetime.now() - timedelta(days=56)
        self.assertEquals(past_datetime_str(day), 'over 1 month ago') 

        day = datetime.now() - timedelta(days=57)
        self.assertEquals(past_datetime_str(day), 'over 2 months ago') 
        day = datetime.now() - timedelta(days=84)
        self.assertEquals(past_datetime_str(day), 'over 2 months ago') 

        day = datetime.now() - timedelta(days=85)
        self.assertEquals(past_datetime_str(day), 'over 3 months ago') 
        day = datetime.now() - timedelta(days=112)
        self.assertEquals(past_datetime_str(day), 'over 3 months ago') 
        
    def test_past_datetime_str_over_years_ago(self):
        day = datetime.now() - timedelta(days=366)
        self.assertEquals(past_datetime_str(day), 'over 1 year ago') 
        day = datetime.now() - timedelta(days=730)
        self.assertEquals(past_datetime_str(day), 'over 1 year ago') 

        day = datetime.now() - timedelta(days=731)
        self.assertEquals(past_datetime_str(day), 'over 2 years ago') 
        day = datetime.now() - timedelta(days=1095)
        self.assertEquals(past_datetime_str(day), 'over 2 years ago') 
