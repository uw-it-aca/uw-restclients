from django.db import models
from datetime import datetime

class CalendarGroup(models.Model):
    SEATTLE = 'sea'
    BOTHELL = 'bot'
    TACOMA = 'tac'
    CAMPUS_CHOICES = (
        (SEATTLE, 'Seattle'),
        (BOTHELL, 'Bothell'),
        (TACOMA, 'Tacoma')
        )
    calendarid = models.PositiveIntegerField(primary_key=True)
    campus = models.CharField(max_length=3,
                              choices=CAMPUS_CHOICES,
                              default=SEATTLE)
    name = models.CharField(max_length=100)

    def is_bot(self):
        return self.campus in (self.BOTHELL)

    def is_sea(self):
        return self.campus in (self.SEATTLE)

    def is_tac(self):
        return self.campus in (self.TACOMA)

    def get_uw_editor_groupid(self):
        return "u_eventcal_%s_%s-editor" % (self.campus,
                                            self.calendarid)

    def get_uw_showon_groupid(self):
        return "u_eventcal_%s_%s-showon" % (self.campus,
                                            self.calendarid)

    def __str__(self):
        return "{name: %s, campus: %s, calendarid: %s}" % (
            self.name, self.campus, self.calendarid)
    

class Permission(models.Model):
    EDIT = 'EDIT'
    NONE = 'NONE'
    SHOWON = 'SHOWON'
    VIEW = 'VIEW'
    LEVEL_CHOICES = (
        (EDIT, 'Can add, delete and change content'),
        (SHOWON, 'Can view and show on'),
        (VIEW, 'Can view content'),
        (NONE, 'None')
        )
    calendarid = models.PositiveIntegerField()
    campus = models.CharField(max_length=3)
    name = models.CharField(max_length=64)
    uwnetid = models.CharField(max_length=16)
    level = models.CharField(max_length=6,
                             choices=LEVEL_CHOICES,
                             default=VIEW)

    def is_edit(self):
        return self.level in (self.EDIT)
    
    def is_showon(self):
        return self.level in (self.SHOWON)
    
    def is_bot(self):
        return self.campus in (CalendarGroup.BOTHELL)

    def is_sea(self):
        return self.campus in (CalendarGroup.SEATTLE)

    def is_tac(self):
        return self.campus in (CalendarGroup.TACOMA)

    def __str__(self):
        return "{calendarid: %s, campus: %s, name: %s, uwnetid: %s, level: %s}" % (
            self.calendarid, self.campus, self.name, self.uwnetid, self.level)
    


    
