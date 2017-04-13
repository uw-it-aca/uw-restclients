from restclients_core import models
from restclients.models.sws import Section
from uw_catalyst.models import GradebookParticipant


class CourseGradeData(models.Model):
    section = models.ForeignKey(Section)
    name = models.CharField(max_length=250)
    class_grade = models.CharField(max_length=10)
    total_score = models.CharField(max_length=10)
    url = models.CharField(max_length=250)

    def json_data(self):
        data = {
            "name": self.name,
            "url": self.url,
            "class_grade": self.class_grade,
            "total_score": self.total_score,
            "assignments": []
        }

        for assignment in self.items:
            data["assignments"].append(assignment.json_data())

        return data


class CourseGradeItem(models.Model):
    name = models.CharField(max_length=250)
    score = models.CharField(max_length=200)
    url = models.CharField(max_length=250)
    max_points = models.CharField(max_length=50)

    def json_data(self):
        return {
            "name": self.name,
            "score": self.score,
            "url": self.url,
            "max_points": self.max_points,
        }
