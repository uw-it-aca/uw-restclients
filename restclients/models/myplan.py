from django.db import models


class MyPlan(models.Model):
    def __init__(self):
        self.terms = []

    def json_data(self):
        data = {
            "terms": []
            }
        for term in self.terms:
            data["terms"].append(term.json_data())

        return data


class MyPlanTerm(models.Model):
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

    def __init__(self):
        self.courses = []

    quarter = models.CharField(max_length=6,
                               choices=QUARTERNAME_CHOICES)
    year = models.PositiveSmallIntegerField()

    def json_data(self):
        data = {
            "year": self.year,
            "quarter": self.quarter,
            "courses": [],
        }

        for course in self.courses:
            data["courses"].append(course.json_data())

        return data


class MyPlanCourse(models.Model):
    def __init__(self):
        self.sections = []

    curriculum_abbr = models.CharField(max_length=6,
                                       db_index=True)
    course_number = models.PositiveSmallIntegerField(db_index=True)
    registrations_available = models.BooleanField()

    def json_data(self):
        data = {
            'curriculum_abbr': self.curriculum_abbr,
            'course_number': self.course_number,
            'registrations_available': self.registrations_available,
            'sections': [],
        }

        for section in self.sections:
            data["sections"].append(section.json_data())

        return data


class MyPlanCourseSection(models.Model):
    section_id = models.CharField(max_length=2,
                                  db_index=True)

    def json_data(self):
        return {
            "section_id": self.section_id
            }
