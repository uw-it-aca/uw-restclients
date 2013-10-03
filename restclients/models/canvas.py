from django.db import models


class Course(models.Model):
    course_url = models.CharField(max_length=2000)
    sis_id = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)

    def sws_course_id(self):
        parts = self.sis_id.split("-")
        if len(parts) != 5:
            return None

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                     parts[4])

        return sws_id


class Enrollment(models.Model):
    course_url = models.CharField(max_length=2000)
    sis_id = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)

    def sws_course_id(self):
        parts = self.sis_id.split("-")

        if len(parts) != 5:
            return None

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                     parts[4])

        return sws_id


class Account(models.Model):
    account_id = models.CharField(max_length=30)
    name = models.CharField(max_length=500)
    parent_account_id = models.CharField(max_length=30)
    root_account_id = models.CharField(max_length=30)


class Report(models.Model):
    report_id = models.CharField(max_length=30)
    type = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    progress = models.SmallIntegerField(max_length=3, default=0)


class ReportType(models.Model):
    name = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
