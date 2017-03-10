import datetime
from restclients_core import models


def get_datetime_str(datetime_obj):
    if datetime_obj is None:
        return None
    return datetime_obj.isoformat()


class GradTerm(models.Model):
    SPRING = 'spring'
    SUMMER = 'summer'
    AUTUMN = 'autumn'
    WINTER = 'winter'

    QUARTERNAME_CHOICES = (
        (SPRING, 'Spring'),
        (SUMMER, 'Summer'),
        (AUTUMN, 'Autumn'),
        (WINTER, 'Winter'),
    )

    quarter = models.CharField(max_length=6,
                               choices=QUARTERNAME_CHOICES)
    year = models.PositiveSmallIntegerField()

    def __init__(self):
        self.terms = []

    def json_data(self):
        return {"year": self.year,
                "quarter": self.get_quarter_display(),
                }


class GradDegree(models.Model):
    AWAITING_STATUS_PREFIX = "Awaiting "
    CANDIDACY_STATUS = "candidacy granted"
    DEPT_RECOMMENDED_STATUS = "recommended by dept"
    GRADUATED_STATUS = "graduated by grad school"
    NOT_GRADUATE_STATUS = "did not graduate"

    req_type = models.CharField(max_length=100)
    submit_date = models.DateTimeField()
    degree_title = models.CharField(max_length=255)
    major_full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=64)
    decision_date = models.DateTimeField(null=True, default=None)
    exam_place = models.CharField(max_length=255, null=True, default=None)
    exam_date = models.DateTimeField(null=True, default=None)
    target_award_year = models.PositiveSmallIntegerField()
    target_award_quarter = models.CharField(
            max_length=6, choices=GradTerm.QUARTERNAME_CHOICES)

    def is_status_graduated(self):
        return self.status.lower() == self.GRADUATED_STATUS

    def is_status_candidacy(self):
        return self.status.lower() == self.CANDIDACY_STATUS

    def is_status_not_graduate(self):
        return self.status.lower() == self.NOT_GRADUATE_STATUS

    def is_status_await(self):
        """
        return true if status is:
        Awaiting Dept Action,
        Awaiting Dept Action (Final Exam),
        Awaiting Dept Action (General Exam)
        """
        return self.status.startswith(self.AWAITING_STATUS_PREFIX)

    def is_status_recommended(self):
        return self.status.lower() == self.DEPT_RECOMMENDED_STATUS

    def json_data(self):
        return {
            "req_type": self.req_type,
            "degree_title": self.degree_title,
            "exam_place": self.exam_place,
            "exam_date": get_datetime_str(self.exam_date)
            if self.exam_date is not None else None,
            "major_full_name": self.major_full_name,
            "status": self.status,
            'decision_date': get_datetime_str(self.decision_date)
            if self.decision_date is not None else None,
            "submit_date": get_datetime_str(self.submit_date),
            "target_award_year": self.target_award_year,
            "target_award_quarter": self.get_target_award_quarter_display()
            if self.target_award_quarter is not None else None,
            }


class GradCommitteeMember(models.Model):
    CHAIR = "chair"
    GSR = "gsr"
    MEMBER = "member"
    MEMBER_TYPE_CHOICES = (
        (CHAIR, "Chair"),
        (GSR, "GSR"),
        (MEMBER, None),
    )
    READING_TYPE_CHOICES = (
        (CHAIR, "Reading Committee Chair"),
        (MEMBER, "Reading Committee Member"),
    )

    first_name = models.CharField(max_length=96)
    last_name = models.CharField(max_length=96)
    member_type = models.CharField(max_length=64,
                                   choices=MEMBER_TYPE_CHOICES)
    reading_type = models.CharField(max_length=64,
                                    null=True,
                                    default=None,
                                    choices=READING_TYPE_CHOICES)
    dept = models.CharField(max_length=128,
                            null=True,
                            default=None)
    email = models.CharField(max_length=255,
                             null=True,
                             default=None)
    status = models.CharField(max_length=64)

    def __eq__(self, other):
        return self.member_type == other.member_type and\
            self.last_name == other.last_name and\
            self.first_name == other.first_name

    def __ne__(self, other):
        return self.member_type != other.member_type or\
            self.last_name != other.last_name or\
            self.first_name != other.first_name

    def __lt__(self, other):
        return self.member_type == other.member_type and\
            self.last_name < other.last_name or\
            self.member_type < other.member_type

    def is_type_chair(self):
        return self.member_type == self.CHAIR

    def is_type_gsr(self):
        return self.member_type == self.GSR

    def is_type_member(self):
        return self.member_type == self.MEMBER

    def is_reading_committee_member(self):
        return self.reading_type is not None and\
            self.reading_type == self.MEMBER

    def is_reading_committee_chair(self):
        return self.reading_type is not None and\
            self.reading_type == self.CHAIR

    def get_reading_display(self):
        if self.is_reading_committee_chair() or\
                self.is_reading_committee_member():
            return self.get_reading_type_display()
        return None

    def __str__(self):
        return "%s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s" %\
            (
             "member_type", self.member_type,
             "reading_type", self.reading_type,
             "last_name", self.last_name,
             "first_name", self.first_name,
             "dept", self.dept,
             "email", self.email,
             "status", self.status)

    def json_data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "member_type": self.get_member_type_display(),
            "reading_type": self.get_reading_display(),
            "dept": self.dept,
            "email": self.email,
            "status": self.status,
            }


class GradCommittee(models.Model):
    committee_type = models.CharField(max_length=64)
    dept = models.CharField(max_length=255, null=True)
    degree_title = models.CharField(max_length=255, null=True)
    degree_type = models.CharField(max_length=255)
    major_full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=64, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __init__(self):
        self.members = []   # GradCommitteeMember

    def json_data(self):
        data = {
            "committee_type": self.committee_type,
            "dept": self.dept,
            "degree_title": self.degree_title,
            "degree_type": self.degree_type,
            "major_full_name": self.major_full_name,
            "status": self.status,
            "start_date": get_datetime_str(self.start_date)
            if self.start_date is not None else None,
            "end_date": get_datetime_str(self.end_date)
            if self.end_date is not None else None,
            "members": [],
            }
        for member in sorted(self.members):
            data["members"].append(member.json_data())
        return data


class GradLeave(models.Model):
    APPROVED = "approved"
    DENIED = "denied"
    PAID = "paid"
    REQUESTED = "requested"
    WITHDRAWN = "withdrawn"

    STATUS_CHOICES = (
        ("", None),
        (APPROVED, "Approved"),
        (DENIED, "Denied"),
        (PAID, "Paid"),
        (REQUESTED, "Requested"),
        (WITHDRAWN, "Withdrawn"),
    )
    reason = models.CharField(max_length=100,
                              db_index=True)
    submit_date = models.DateTimeField()
    status = models.CharField(max_length=50,
                              blank=True,
                              default="",
                              choices=STATUS_CHOICES)

    def __init__(self):
        self.terms = []

    def is_status_approved(self):
        return self.status == self.APPROVED

    def is_status_denied(self):
        return self.status == self.DENIED

    def is_status_paid(self):
        return self.status == self.PAID

    def is_status_requested(self):
        return self.status == self.REQUESTED

    def is_status_withdrawn(self):
        return self.status == self.WITHDRAWN

    def json_data(self):
        data = {
            'reason': self.reason,
            'submit_date': get_datetime_str(self.submit_date)
            if self.submit_date is not None else None,
            'status': self.get_status_display(),
            'terms': [],
        }
        for term in self.terms:
            data["terms"].append(term.json_data())
        return data


class GradPetition(models.Model):
    APPROVE = "approve"
    APPROVED = "approved"
    DENY = "deny"
    NOT_APPROVED = "not approved"
    PENDING = "pending"
    WITHDRAW = "withdraw"
    WITHDRAWN = "withdrawn"

    RECOMMEND_CHOICES = (
        ("", None),
        (APPROVE, "Approve"),
        (DENY, "Deny"),
        (PENDING, "Pending"),
        (WITHDRAW, "Withdraw"),
    )

    DECISION_CHOICES = (
        ("", None),
        (APPROVED, "Approved"),
        (NOT_APPROVED, "Not approved"),
        (PENDING, "Pending"),
        (WITHDRAW, "Withdraw"),
        (WITHDRAWN, "Withdrawn"),
    )

    description = models.CharField(max_length=100,
                                   db_index=True)
    submit_date = models.DateTimeField()
    dept_recommend = models.CharField(max_length=50,
                                      choices=RECOMMEND_CHOICES)
    gradschool_decision = models.CharField(max_length=50,
                                           null=True,
                                           blank=True,
                                           default="",
                                           choices=DECISION_CHOICES)
    decision_date = models.DateTimeField(null=True)
    # gradschool decision date

    def is_dept_approve(self):
        return self.dept_recommend == self.APPROVE

    def is_dept_deny(self):
        return self.dept_recommend == self.DENY

    def is_dept_pending(self):
        return self.dept_recommend == self.PENDING

    def is_dept_withdraw(self):
        return self.dept_recommend == self.WITHDRAW

    def is_gs_pending(self):
        return self.gradschool_decision == self.PENDING

    def json_data(self):
        data = {
            'description': self.description,
            'submit_date': get_datetime_str(self.submit_date),
            'decision_date': get_datetime_str(self.decision_date)
            if self.decision_date is not None else None,
            'dept_recommend': self.get_dept_recommend_display(),
            'gradschool_decision': self.get_gradschool_decision_display(),
            }
        return data
