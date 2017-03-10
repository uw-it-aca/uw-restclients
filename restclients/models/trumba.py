from restclients_core import models
from datetime import datetime


def is_bot(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.BOT_CAMPUS_CODE


def is_sea(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.SEA_CAMPUS_CODE


def is_tac(campus_code):
    return campus_code is not None and\
        campus_code == TrumbaCalendar.TAC_CAMPUS_CODE


def is_valid_campus_code(campus_code):
    return is_bot(campus_code) or is_sea(campus_code) or is_tac(campus_code)


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
                              default=SEA_CAMPUS_CODE
                              )
    name = models.CharField(max_length=500)

    def is_bot(self):
        return is_bot(self.campus)

    def is_sea(self):
        return is_sea(self.campus)

    def is_tac(self):
        return is_tac(self.campus)

    def __eq__(self, other):
        return self.calendarid == other.calendarid

    def __lt__(self, other):
        return self.campus == other.campus and\
            self.name < other.name

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


editor_group_desc =\
    "Specifying the editors who can add/edit/delete events on this calendar"
showon_group_desc =\
    "Specifying the editor groups whose members have the showon permissions" +\
    " on this calendar"


def make_group_desc(gtype):
    if is_editor_group(gtype):
        return editor_group_desc
    else:
        return showon_group_desc


class UwcalGroup(models.Model):
    GTYEP_EDITOR = 'editor'
    GTYEP_SHOWON = 'showon'
    ADMIN_GROUP_NAME = 'u_eventcal_support'
    calendar = models.ForeignKey(TrumbaCalendar)
    gtype = models.CharField(max_length=6)
    uwregid = models.CharField(max_length=32, db_index=True, unique=True)
    name = models.CharField(max_length=64, db_index=True, unique=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=500, null=True)
    lastverified = models.DateTimeField(null=True)

    def __init__(self, *args, **kwargs):
        super(UwcalGroup, self).__init__(*args, **kwargs)

        if self.name is None or len(self.name) == 0:
            self.name = make_group_name(self.calendar.campus,
                                        self.calendar.calendarid,
                                        self.gtype)

        if self.title is None or len(self.title) == 0:
            self.title = make_group_title(self.calendar.name,
                                          self.gtype)

        if self.description is None or len(self.description) == 0:
            self.description = make_group_desc(self.gtype)

    def get_calendarid(self):
        return self.calendar.calendarid

    def get_campus_code(self):
        return self.calendar.campus

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
            self.uwregid, self.name, self.title, self.description)

    def __unicode__(self):
        return u'{uwregid: %s, name: %s, title: %s, description: %s}' % (
            self.uwregid, self.name, self.title, self.description)


def is_edit_permission(level):
    return level is not None and level == Permission.EDIT


def is_showon_permission(level):
    return level is not None and level == Permission.SHOWON


def is_publish_permission(level):
    return level is not None and level == Permission.PUBLISH


def is_republish_permission(level):
    return level is not None and level == Permission.REPUBLISH


def is_view_permission(level):
    return level is not None and level == Permission.VIEW


def is_higher_permission(level1, level2):
    """
    Return True if the level1 is higher than level2
    """
    return (is_publish_permission(level1) and
            not is_publish_permission(level2) or
            (is_edit_permission(level1) and
             not is_publish_permission(level2) and
             not is_edit_permission(level2)) or
            (is_showon_permission(level1) and
             is_view_permission(level2)))


class Permission(models.Model):
    PUBLISH = 'PUBLISH'
    EDIT = 'EDIT'
    REPUBLISH = 'REPUBLISH'
    SHOWON = 'SHOWON'
    VIEW = 'VIEW'
    NONE = 'NONE'
    LEVEL_CHOICES = ((EDIT, 'Can add, delete and change content'),
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
        return "%s@washington.edu" % self.uwnetid

    def is_publish(self):
        return is_publish_permission(self.level)

    def is_edit(self):
        return is_edit_permission(self.level) or self.is_publish()

    def is_showon(self):
        return is_showon_permission(self.level) or\
            is_republish_permission(self.level)

    def is_gt_level(self, perm_level):
        return is_higher_permission(self.level, perm_level)

    def is_bot(self):
        return is_bot(self.campus)

    def is_sea(self):
        return is_sea(self.campus)

    def is_tac(self):
        return is_tac(self.campus)

    def __eq__(self, other):
        return self.calendarid == other.calendarid and\
            self.uwnetid == other.uwnetid and\
            self.name == other.name and self.level == other.level

    def __lt__(self, other):
        return self.calendarid == other.calendarid and\
            (is_higher_permission(self.level, other.level) or
             self.level == other.level and
             self.uwnetid < other.uwnetid)

    def __str__(self):
        return "{calendarid: %s, campus: %s, uwnetid: %s, level: %s}" % (
            self.calendarid, self.campus, self.uwnetid, self.level)

    def __unicode__(self):
        return u'{calendarid: %s, campus: %s, uwnetid: %s, level: %s}' % (
            self.calendarid, self.campus, self.uwnetid, self.level)
