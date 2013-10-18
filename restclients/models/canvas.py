from django.db import models


class Account(models.Model):
    account_id = models.IntegerField(max_length=20)
    sis_account_id = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=500)
    parent_account_id = models.CharField(max_length=30)
    root_account_id = models.CharField(max_length=30)


class Course(models.Model):
    course_id = models.IntegerField(max_length=20)
    course_url = models.CharField(max_length=2000)
    sis_course_id = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)

    def sws_course_id(self):
        parts = self.sis_course_id.split("-")
        if len(parts) != 5:
            return None

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                     parts[4])

        return sws_id


class Enrollment(models.Model):
    STUDENT = "StudentEnrollment"
    TEACHER = "TeacherEnrollment"
    TA = "TaEnrollment"
    OBSERVER = "ObserverEnrollment"
    DESIGNER = "DesignerEnrollment"

    ROLE_CHOICES = (
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (TA, "TA"),
        (OBSERVER, "Observer"),
        (DESIGNER, "Designer")
    )

    user_id = models.IntegerField(max_length=20)
    course_id = models.IntegerField(max_length=20)
    section_id = models.IntegerField(max_length=20)
    login_id = models.CharField(max_length=80)
    role = models.CharField(max_length=80, choices=ROLE_CHOICES)
    status = models.CharField(max_length=100)
    html_url = models.CharField(max_length=1000)
    sis_course_id = models.CharField(max_length=100, null=True)
    course_url = models.CharField(max_length=2000, null=True)
    course_name = models.CharField(max_length=100, null=True)

    def sws_course_id(self):
        if self.sis_course_id is None:
            return None

        parts = self.sis_course_id.split("-")

        if len(parts) != 5:
            return None

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                     parts[4])

        return sws_id


class Report(models.Model):
    report_id = models.CharField(max_length=30)
    type = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    progress = models.SmallIntegerField(max_length=3, default=0)


class ReportType(models.Model):
    name = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
