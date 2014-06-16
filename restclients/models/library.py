from django.db import models
from restclients.util.formator import standard_date_str


class MyLibAccount(models.Model):
    holds_ready = models.IntegerField(max_length=8)
    fines = models.DecimalField(max_digits=8, decimal_places=2)
    items_loaned = models.IntegerField(max_length=8)
    next_due = models.DateField(null=True)

    
    def next_due_date_str(self):
        if self.next_due is None:
            return self.next_due
        else:
            return standard_date_str(self.next_due)


    def json_data(self, full_name_format=False):
        """
        The default format for next due date is the uncode of 
        the isoformat (yyyy-mm-dd). 
        If full_name_format is True, the format for 
        next due date will be:  "month-full-name dd, yyyy".
        """
        next_due = str(self.next_due)
        if full_name_format:
            next_due = self.next_due_date_str()
            
        return {
            'holds_ready': self.holds_ready,
            'fines': self.fines,
            'items_loaned': self.items_loaned,
            'next_due': unicode(next_due)
            }


    def __str__(self):
        return "{next_due: %s, holds_ready: %d, fines: %.2f, items_loaned: %d}" % (
            self.next_due, self.holds_ready, self.fines, self.items_loaned)
