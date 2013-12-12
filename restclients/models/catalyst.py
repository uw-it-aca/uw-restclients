from django.db import models
from restclients.models.sws import Section

class CourseGradeData(models.Model):
    section = models.ForeignKey(Section)
    name = models.CharField(max_length=250)
    class_grade = models.CharField(max_length=10)
    total_score = models.CharField(max_length=10)
    url = models.CharField(max_length=250)


class CourseGradeItem(models.Model):
    name = models.CharField(max_length=250)
    score = models.CharField(max_length=200)
    url = models.CharField(max_length=250)

