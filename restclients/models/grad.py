from django.db import models


def get_datetime_str(datetime_obj):
    if datetime_obj is None:
        return None
    return datetime_obj.strftime("%Y-%m-%d %H:%M")


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
                "quarter": self.quarter,
                }


class GradDegree(models.Model):
    req_type = models.CharField(max_length=100)
    submit_date = models.DateTimeField()
    degree_title = models.CharField(max_length=255)
    major_full_name = models.CharField(max_length=255)
    status = models.CharField(max_length=64)
    exam_place = models.CharField(max_length=255, null=True)
    exam_date = models.DateTimeField(null=True)
    target_award_year = models.PositiveSmallIntegerField()
    target_award_quarter = models.CharField(
            max_length=6, choices=GradTerm.QUARTERNAME_CHOICES)

    def json_data(self):
        return {
            "req_type": self.req_type,
            "degree_title": self.degree_title,
            "exam_place": self.exam_place,
            "exam_date": get_datetime_str(self.exam_date),
            "major_full_name": self.major_full_name,
            "status": self.status,
            "submit_date": get_datetime_str(self.submit_date),
            "target_award_year": self.target_award_year,
            "target_award_quarter": self.target_award_quarter,
            }


class GradCommitteeMember(models.Model):
    first_name = models.CharField(max_length=96)
    last_name = models.CharField(max_length=96)
    member_type = models.CharField(max_length=64)
    dept = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=64)

    def json_data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "member_type": self.member_type,
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
            "start_date": get_datetime_str(self.start_date),
            "end_date": get_datetime_str(self.end_date),
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

    def json_data(self):
        data = {
            'reason': self.reason,
            'submit_date': self.submit_date,
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

    def json_data(self):
        data = {
            'description': self.description,
            'submit_date': get_datetime_str(self.submit_date),
            'dept_recommend': self.dept_recommend,
            'gradschool_decision': self.gradschool_decision,
            }
        return data
