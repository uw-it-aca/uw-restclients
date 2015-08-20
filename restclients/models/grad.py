import datetime
from django.db import models


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
    req_type = models.CharField(max_length=100)
    submit_date = models.DateTimeField()
    degree_title = models.CharField(max_length=255)
    major_full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=64)
    decision_date = models.DateTimeField(null=True)
    exam_place = models.CharField(max_length=255, null=True)
    exam_date = models.DateTimeField(null=True)
    target_award_year = models.PositiveSmallIntegerField()
    target_award_quarter = models.CharField(
            max_length=6, choices=GradTerm.QUARTERNAME_CHOICES)

    def is_status_graduated(self):
        return self.status.lower() == "graduated by grad school"

    def is_status_candidacy(self):
        return self.status.lower() == "candidacy granted"

    def is_status_not_graduate(self):
        return self.status.lower() == "did not graduate"

    def is_status_await(self):
        """
        return true if status is:
        Awaiting Dept Action,
        Awaiting Dept Action (Final Exam),
        Awaiting Dept Action (General Exam)
        """
        return self.status.startswith("Awaiting ")

    def is_status_recommended(self):
        return self.status.lower() == "recommended by dept"

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
    first_name = models.CharField(max_length=96)
    last_name = models.CharField(max_length=96)
    member_type = models.CharField(max_length=64)
    reading_type = models.CharField(max_length=64)
    dept = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=64)

    def is_reading_committee_member(self):
        return self.reading_type.lower() == "member"

    def is_reading_committee_chair(self):
        return self.reading_type.lower() == "chair"

    def get_reading_type_display(self):
        if self.is_reading_committee_chair():
            return "reading committee chair"
        if self.is_reading_committee_member():
            return "reading committee member"
        return None

    def json_data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "member_type": self.member_type,
            "reading_type": self.get_reading_type_display(),
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
        for member in self.members:
            data["members"].append(member.json_data())
        return data


class GradLeave(models.Model):
    reason = models.CharField(max_length=100,
                              db_index=True)
    submit_date = models.DateTimeField()
    status = models.CharField(max_length=50,
                              blank=True)

    def __init__(self):
        self.terms = []

    def is_status_approved(self):
        return self.status.lower() == "approved"

    def is_status_denied(self):
        return self.status.lower() == "denied"

    def is_status_paid(self):
        return self.status.lower() == "paid"

    def is_status_requested(self):
        return self.status.lower() == "requested"

    def is_status_withdrawn(self):
        return self.status.lower() == "withdrawn"

    def json_data(self):
        data = {
            'reason': self.reason,
            'submit_date': get_datetime_str(self.submit_date)
            if self.submit_date is not None else None,
            'status': self.status,
            'terms': [],
        }
        for term in self.terms:
            data["terms"].append(term.json_data())
        return data


class GradPetition(models.Model):
    description = models.CharField(max_length=100,
                                   db_index=True)
    submit_date = models.DateTimeField()
    dept_recommend = models.CharField(max_length=50)
    gradschool_decision = models.CharField(max_length=50,
                                           null=True,
                                           blank=True)
    decision_date = models.DateTimeField(null=True)
    # gradschool decision date

    def is_dept_approve(self):
        return self.dept_recommend.lower() == "approve"

    def is_dept_deny(self):
        return self.dept_recommend.lower() == "deny"

    def is_dept_pending(self):
        return self.dept_recommend.lower() == "pending"

    def is_dept_withdraw(self):
        return self.dept_recommend.lower() == "withdraw"

    def is_gs_pending(self):
        return self.gradschool_decision.lower() == "pending"

    def json_data(self):
        data = {
            'description': self.description,
            'submit_date': get_datetime_str(self.submit_date),
            'decision_date': get_datetime_str(self.decision_date)
            if self.decision_date is not None else None,
            'dept_recommend': self.dept_recommend,
            'gradschool_decision': self.gradschool_decision,
            }
        return data
