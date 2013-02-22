from django.db import models


class GroupReference(models.Model):
    uwregid = models.CharField(max_length=32)
    name = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    url = models.CharField(max_length=200)


class Group(models.Model):
    CLASSIFICATION_NONE = "u"
    CLASSIFICATION_PUBLIC = "p"
    CLASSIFICATION_RESTRICTED = "r"
    CLASSIFICATION_CONFIDENTIAL = "c"

    CLASSIFICATION_TYPES = (
        (CLASSIFICATION_NONE, "Unclassified"),
        (CLASSIFICATION_PUBLIC, "Public"),
        (CLASSIFICATION_RESTRICTED, "Restricted"),
        (CLASSIFICATION_CONFIDENTIAL, "Confidential")
    )

    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)

    name = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    contact = models.CharField(max_length=120)
    authnfactor = models.PositiveSmallIntegerField(max_length=1,
                                                   choices=((1, ""), (2, "")),
                                                   default=1)
    classification = models.CharField(max_length=1,
                                      choices=CLASSIFICATION_TYPES,
                                      default=CLASSIFICATION_NONE)
    emailenabled = models.CharField(max_length=10,
                                    choices=(("UWExchange", "UWExchange"),
                                             ("disabled", "disabled")),
                                    default="disabled")
    dependson = models.CharField(max_length=500)
    publishemail = models.CharField(max_length=120)
    reporttoorig = models.SmallIntegerField(max_length=1,
                                            choices=((1, "Yes"), (0, "No")),
                                            default=0)


class CourseGroup(Group):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"

    QUARTERNAME_CHOICES = (
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
        (AUTUMN, "Autumn"),
        (WINTER, "Winter"),
    )

    curriculum_abbr = models.CharField(max_length=8)
    course_number = models.CharField(max_length=3)
    year = models.PositiveSmallIntegerField()
    quarter = models.CharField(max_length=6,
                               choices=QUARTERNAME_CHOICES)
    section_id = models.CharField(max_length=2,
                                  db_index=True)

    sln = models.PositiveIntegerField()


class GroupUser(models.Model):
    UWNETID_TYPE = "uwnetid"
    EPPN_TYPE = "eppn"
    GROUP_TYPE = "group"
    DNS_TYPE = "dns"

    TYPE_CHOICES = (
        (UWNETID_TYPE, "UWNetID"),
        (EPPN_TYPE, "ePPN"),
        (GROUP_TYPE, "Group ID"),
        (DNS_TYPE, "Hostname"),
    )

    name = models.CharField(max_length=40)
    user_type = models.SlugField(max_length=8,
                                 choices=TYPE_CHOICES)

    def is_uwnetid(self):
        return self.user_type == UWNETID_TYPE

    def is_eppn(self):
        return self.user_type == EPPN_TYPE

    def is_group(self):
        return self.user_type == GROUP_TYPE

    def __eq__(self, other):
        return self.name == other.name and self.user_type == other.user_type


class GroupMember(models.Model):
    UWNETID_TYPE = "uwnetid"
    EPPN_TYPE = "eppn"
    GROUP_TYPE = "group"
    DNS_TYPE = "dns"

    TYPE_CHOICES = (
        (UWNETID_TYPE, "UWNetID"),
        (EPPN_TYPE, "ePPN"),
        (GROUP_TYPE, "Group ID"),
        (DNS_TYPE, "Hostname"),
    )

    name = models.CharField(max_length=40)
    member_type = models.SlugField(max_length=8,
                                   choices=TYPE_CHOICES)

    def is_uwnetid(self):
        return self.member_type == UWNETID_TYPE

    def is_eppn(self):
        return self.member_type == EPPN_TYPE

    def is_group(self):
        return self.member_type == GROUP_TYPE

    def __eq__(self, other):
        return self.name == other.name and self.member_type == other.member_type
