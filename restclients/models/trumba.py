from django.db import models
from datetime import datetime

def is_bot(campus_code):
    return campus_code is not None and campus_code == TrumbaCalendar.BOT_CAMPUS_CODE

def is_sea(campus_code):
    return campus_code is not None and campus_code == TrumbaCalendar.SEA_CAMPUS_CODE

def is_tac(campus_code):
    return campus_code is not None and campus_code == TrumbaCalendar.TAC_CAMPUS_CODE


class TrumbaCalendar(models.Model):
    SEA_CAMPUS_CODE = 'sea'
    BOT_CAMPUS_CODE = 'bot'
    TAC_CAMPUS_CODE = 'tac'
    CAMPUS_CHOICES = (
        (SEA_CAMPUS_CODE, 'Seattle'),
        (BOT_CAMPUS_CODE, 'Bothell'),
        (TAC_CAMPUS_CODE, 'Tacoma')
        )
    calendarid = models.PositiveIntegerField(primary_key=True)
    campus = models.CharField(max_length=3,
                              choices=CAMPUS_CHOICES,
                              default=SEA_CAMPUS_CODE)
    name = models.CharField(max_length=500)

    def is_bot(self):
        return is_bot(self.campus)

    def is_sea(self):
        return is_sea(self.campus)

    def is_tac(self):
        return is_tac(self.campus)

    def __eq__(self, other):
        return self.calendarid == other.calendarid 

    def __str__(self):
        return "{name: %s, campus: %s, calendarid: %s}" % (
            self.name, self.campus, self.calendarid)

    def __unicode__(self):
        return u'{name: %s, campus: %s, calendarid: %s}' % (
            self.name, self.campus, self.calendarid)

def is_editor_group(gtype):
    return gtype is not None and gtype == UwcalGroup.GTYEP_EDITOR

def is_showon_group(gtype):
    return gtype is not None and gtype == UwcalGroup.GTYEP_SHOWON

def make_group_name(campus, calendarid, gtype):
    return "u_eventcal_%s_%s-%s" % (campus, calendarid, gtype)

def make_group_title(calendar_name, gtype):
    return "%s calendar %s group" % (calendar_name, gtype)

def make_group_desc(gtype):
    if is_editor_group(gtype):
        return "Specifying the editors who are able to add/edit/delete any event on the corresponding Trumba calendar"
    else:
        return "Specifying the users with view and showon permission of the corresponding Trumba calendar"

class UwcalGroup(models.Model):
    GTYEP_EDITOR = 'editor'
    GTYEP_SHOWON = 'showon'
    calendar = models.ForeignKey(TrumbaCalendar)
    gtype = models.CharField(max_length=6)
    uwregid = models.CharField(max_length=32, null=True, default=None)
    name = models.CharField(max_length=500, null=True, default=None)
    title = models.CharField(max_length=500, null=True, default=None)
    description = models.CharField(max_length=500, null=True, blank=True, default=None)
    lastverified = models.DateTimeField(null=True, default=datetime.now())

    def get_calendarid(self):
        return self.calendar.calendarid

    def get_campus_code(self):
        return self.calendar.campus

    def get_name(self):
        if self.name is not None and len(self.name) > 0:
            return self.name
        return make_group_name(self.calendar.campus,
                               self.calendar.calendarid,
                               self.gtype)

    def get_title(self):
        if self.title is not None and len(self.title) > 0:
            return self.title
        return make_group_title(self.calendar.name,
                                self.gtype)

    def get_desc(self):
        if self.description is not None and len(self.description) > 0:
            return self.description
        return make_group_desc(self.gtype)

    def has_regid(self):
        return self.uwregid is not None and len(self.uwregid) == 32

    def is_editor_group(self):
        return is_editor_group(self.gtype)
    
    def is_showon_group(self):
        return is_showon_group(self.gtype)

    def set_lastverified(self):
        self.lastverified = datetime.now()

    def __eq__(self, other):
        return self.calendar == other.calendar and self.gtype == other.gtype

    def __str__(self):
        return "{uwregid: %s, name: %s, title: %s, description: %s}" % (
            self.uwregid, self.get_name(), self.get_title(), self.get_desc())

    def __unicode__(self):
        return u'{uwregid: %s, name: %s, title: %s, description: %s}' % (
            self.uwregid, self.get_name(), self.get_title(), self.get_desc())

def is_edit_permission(level):
    return level is not None and level == Permission.EDIT
    
def is_showon_permission(level):
    return level is not None and level == Permission.SHOWON
    
def is_publish_permission(level):
    return level is not None and level == Permission.PUBLISH

def is_republish_permission(level):
    return level is not None and level == Permission.REPUBLISH

class Permission(models.Model):
    EDIT = 'EDIT'
    NONE = 'NONE'
    PUBLISH = 'PUBLISH'
    REPUBLISH = 'REPUBLISH'
    SHOWON = 'SHOWON'
    VIEW = 'VIEW'
    LEVEL_CHOICES = (
        (EDIT, 'Can add, delete and change content'),
        (PUBLISH, 'Can view, edit and publish'),
        (REPUBLISH, 'Can view, edit and republish'),
        (SHOWON, 'Can view and show on'),
        (VIEW, 'Can view content'),
        (NONE, 'None')
        )
    calendarid = models.PositiveIntegerField()
    campus = models.CharField(max_length=3)
    uwnetid = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    level = models.CharField(max_length=6,
                             choices=LEVEL_CHOICES,
                             default=VIEW)

    def get_trumba_userid(self):
        return "%s@washington.edu" % uwnetid

    def is_edit(self):
        return is_edit_permission(self.level)
    
    def is_publish(self):
        return is_publish_permission(self.level)
    
    def is_republish(self):
        return is_republish_permission(self.level)
    
    def is_showon(self):
        return is_showon_permission(self.level)
    
    def is_bot(self):
        return is_bot(self.campus)

    def is_sea(self):
        return is_sea(self.campus)

    def is_tac(self):
        return is_tac(self.campus)

    def __eq__(self, other):
        return self.calendarid == other.calendarid and self.uwnetid == other.uwnetid and self.name == other.name and self.level == other.level

    def __str__(self):
        return "{calendarid: %s, campus: %s, uwnetid: %s, level: %s}" % (
                self.calendarid, self.campus, self.uwnetid, self.level)
    
    def __unicode__(self):
        return u'{calendarid: %s, campus: %s, uwnetid: %s, name: %s, level: %s}' % (
                self.calendarid, self.campus, self.uwnetid, self.name, self.level)
    


    
