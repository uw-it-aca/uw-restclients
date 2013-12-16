from django.test import TestCase
from restclients.catalyst.gradebook import GradeBook

class CatalystGradebookGrades(TestCase):

   def test_student_grades(self):
         with self.settings(
                RESTCLIENTS_CATALYST_DAO_CLASS='restclients.dao_implementation.catalyst.File'):

                catalyst = GradeBook()
                data = catalyst.get_grades_for_student_and_term('javerage', 2013, 'Autumn')

                train = data['2013,autumn,TRAIN,100/A']

                self.assertEquals(train[0].class_grade, "3.6")
                self.assertEquals(train[0].url, "https://catalyst.uw.edu/gradebook/notreal/999")

                self.assertEquals(len(train[0].items), 6)
                self.assertEquals(train[0].items[0].name, "Homework 1")
                self.assertEquals(train[0].items[0].score, "80")

