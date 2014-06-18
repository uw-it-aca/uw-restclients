from django.db import models
from restclients.util.date_formator import month_full_name_date_str


class MyLibAccount(models.Model):
    holds_ready = models.IntegerField(max_length=8)
    fines = models.DecimalField(max_digits=8, decimal_places=2)
    items_loaned = models.IntegerField(max_length=8)
    next_due = models.DateField(null=True)

    
    def get_next_due_date_str(self, full_name_format):
        """
        If full_name_format is False, return next due date in 
        the ISO format (yyyy-mm-dd). 
        If full_name_format is True, return the format of: 
        "month-full-name dd, yyyy".
        If the next_due is None, return None.
        """
        if self.next_due is not None:
            if full_name_format:
                return month_full_name_date_str(self.next_due)
            else:
                return str(self.next_due)

        return None


    def json_data(self, full_name_format=False):
        return {
            'holds_ready': self.holds_ready,
            'fines': self.fines,
            'items_loaned': self.items_loaned,
            'next_due': self.get_next_due_date_str(full_name_format)
            }


    def __str__(self):
        return "{next_due: %s, holds_ready: %d, fines: %.2f, items_loaned: %d}" % (
            self.next_due, self.holds_ready, self.fines, self.items_loaned)
