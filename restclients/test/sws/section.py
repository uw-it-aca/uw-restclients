from django.test import TestCase
from django.conf import settings
from restclients.models.sws import Term, Curriculum, Person
from restclients.exceptions import DataFailureException
from restclients.exceptions import InvalidSectionID, InvalidSectionURL
from restclients.exceptions import InvalidCanvasIndependentStudyCourse, InvalidCanvasSection
import restclients.sws.section as SectionSws
from restclients.sws import use_v5_resources

class SWSTestSectionData(TestCase):
    def test_final_exams(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = SectionSws.get_section_by_label('2013,summer,B BIO,180/A')
            self.assertEquals(section.final_exam, None, "No final exam for B BIO 180")

            section = SectionSws.get_section_by_label('2013,summer,MATH,125/G')
            final_exam = section.final_exam

            self.assertEquals(final_exam.is_confirmed, False, "Final exam for Math 125 isn't confirmed")
            self.assertEquals(final_exam.no_exam_or_nontraditional, False, "Final exam for Math 125 isn't non-traditional")
            section = SectionSws.get_section_by_label('2013,summer,TRAIN,101/A')
            final_exam = section.final_exam

            self.assertEquals(final_exam.is_confirmed, True, "Final exam for Train 101 is confirmed")
            self.assertEquals(final_exam.no_exam_or_nontraditional, False, "Final exam for Train 101 isn't non-traditional")
            self.assertEquals(final_exam.building, "KNE", "Has right final building")
            self.assertEquals(final_exam.room_number, "012", "Has right room #")

            start = final_exam.start_date
            end = final_exam.end_date

            self.assertEquals(start.year, 2013)
            self.assertEquals(start.month, 6)
            self.assertEquals(start.day, 2)
            self.assertEquals(start.hour, 13)
            self.assertEquals(start.minute, 30)

            self.assertEquals(end.year, 2013)
            self.assertEquals(end.month, 6)
            self.assertEquals(end.day, 2)
            self.assertEquals(end.hour, 16)
            self.assertEquals(end.minute, 20)



    def test_section_by_label(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            #Valid data, shouldn't throw any exceptions
            SectionSws.get_section_by_label('2013,summer,TRAIN,100/A')

            #Invalid data, should throw exceptions
            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              '')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              ' ')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              '2012')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              '2012,summer')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              '2012,summer,TRAIN')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              '2012, summer, TRAIN, 100')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              'summer, TRAIN, 100/A')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              '2012,fall,TRAIN,100/A')

            self.assertRaises(InvalidSectionID,
                              SectionSws.get_section_by_label,
                              '-2012,summer,TRAIN,100/A')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '9999,summer,TRAIN,100/A')

            #Valid section labels, no files for them
            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2012,summer,TRAIN,110/A')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2012,summer,TRAIN,100/B')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2012,summer,PHYS,121/B')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2012,summer,PHYS,121/BB')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2010,autumn,G H,201/A')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2010,autumn,CS&SS,221/A')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2010,autumn,KOREAN,101/A')

            self.assertRaises(DataFailureException,
                              SectionSws.get_section_by_label,
                              '2010,autumn,CM,101/A')

    def test_instructors_in_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = SectionSws.get_section_by_label('2013,winter,ASIAN,203/A')

            self.assertEquals(len(section.get_instructors()), 1, "Correct number of instructors")

            person1 = Person(uwregid="FBB38FE46A7C11D5A4AE0004AC494FFE")
            self.assertEquals(section.is_instructor(person1), False, "Person is not instructor")

            person2 = Person(uwregid="6DF0A9206A7D11D5A4AE0004AC494FFE")
            self.assertEquals(section.is_instructor(person2), True, "Person is instructor")

            section2 = SectionSws.get_section_by_label('2013,summer,TRAIN,101/A')
            self.assertEquals(len(section2.get_instructors()), 2, "Correct number of instructors")

            section3 = SectionSws.get_section_by_label('2013,spring,PHYS,121/A')
            self.assertEquals(len(section3.get_instructors()), 5,
                              "Correct number of all instructors")

            section3 = SectionSws.get_section_by_label('2013,spring,PHYS,121/A', False)
            self.assertEquals(len(section3.get_instructors()), 4,
                              "Correct number of TSPrinted instructors")

    def test_delegates_in_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = SectionSws.get_section_by_label('2013,winter,ASIAN,203/A')

            self.assertEquals(len(section.grade_submission_delegates), 3,
                "Correct number of delegates")

            person1 = Person(uwregid="6DF0A9206A7D11D5A4AE0004AC494FFE")
            self.assertEquals(section.is_grade_submission_delegate(person1), False, "Person is not delegate")

            person2 = Person(uwregid="FBB38FE46A7C11D5A4AE0004AC494FFE")
            self.assertEquals(section.is_grade_submission_delegate(person2), True, "Person is delegate")

    def test_joint_sections(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = SectionSws.get_section_by_label('2013,winter,ASIAN,203/A')
            joint_sections = SectionSws.get_joint_sections(section)

            self.assertEquals(len(joint_sections), 1)

            section = SectionSws.get_section_by_label('2013,winter,EMBA,503/A')
            joint_sections = SectionSws.get_joint_sections(section)

            self.assertEquals(len(joint_sections), 0)

    #Failing because linked section json files haven't been made (Train 100 AA/AB)
    def test_linked_sections(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            #Valid data, shouldn't throw any exceptions
            section = SectionSws.get_section_by_label('2013,summer,TRAIN,100/A')
            SectionSws.get_linked_sections(section)

            #Invalid data, should throw exceptions
            section.linked_section_urls = ['']
            self.assertRaises(InvalidSectionURL,
                              SectionSws.get_linked_sections, section)

            section.linked_section_urls = [' ']
            self.assertRaises(InvalidSectionURL,
                              SectionSws.get_linked_sections, section)

            section.linked_section_urls = ['2012,summer,TRAIN,100/A']
            self.assertRaises(InvalidSectionURL,
                              SectionSws.get_linked_sections, section)

            if use_v5_resources():
                section.linked_section_urls = ['/student/v5/course/2012,summer,PHYS,121/B.json']
            else:
                section.linked_section_urls = ['/student/v4/course/2012,summer,PHYS,121/B.json']
            self.assertRaises(DataFailureException,
                              SectionSws.get_linked_sections, section)

            if use_v5_resources():
                section.linked_section_urls = ['/student/v5/course/2010,autumn,CS&SS,221/A.json']
            else:
                section.linked_section_urls = ['/student/v4/course/2010,autumn,CS&SS,221/A.json']
            self.assertRaises(DataFailureException,
                              SectionSws.get_linked_sections, section)

            if use_v5_resources():
                section.linked_section_urls = ['/student/v5/course/2010,autumn,KOREAN,101/A.json']
            else:
                section.linked_section_urls = ['/student/v4/course/2010,autumn,KOREAN,101/A.json']
            self.assertRaises(DataFailureException,
                              SectionSws.get_linked_sections, section)

            if use_v5_resources():
                section.linked_section_urls = ['/student/v5/course/2010,autumn,G H,201/A.json']
            else:
                section.linked_section_urls = ['/student/v4/course/2010,autumn,G H,201/A.json']
            self.assertRaises(DataFailureException,
                              SectionSws.get_linked_sections, section)

            if use_v5_resources():
                section.linked_section_urls = ['/student/v5/course/2010,autumn,CM,101/A.json']
            else:
                section.linked_section_urls = ['/student/v4/course/2010,autumn,CM,101/A.json']
            self.assertRaises(DataFailureException,
                              SectionSws.get_linked_sections, section)

            if use_v5_resources():
                section.linked_section_urls = ['/student/v5/course/2012,autumn,PHYS,121/A.json',
                                           '/student/v5/course/2012,autumn,PHYS,121/AC.json',
                                           '/student/v5/course/2012,autumn,PHYS,121/BT.json']
            else:
                section.linked_section_urls = ['/student/v4/course/2012,autumn,PHYS,121/A.json',
                                           '/student/v4/course/2012,autumn,PHYS,121/AC.json',
                                           '/student/v4/course/2012,autumn,PHYS,121/BT.json']
            self.assertRaises(DataFailureException,
                              SectionSws.get_linked_sections, section)

            if use_v5_resources():
                section.linked_section_urls = ['/student/v5/course/2012,autumn,PHYS,121/A.json',
                                           '/student/v5/course/2012,autumn,PHYS,121/AC.json',
                                           '/student/v5/course/2012,autumn,PHYS,121/AAA.json']
            else:
                section.linked_section_urls = ['/student/v4/course/2012,autumn,PHYS,121/A.json',
                                           '/student/v4/course/2012,autumn,PHYS,121/AC.json',
                                           '/student/v4/course/2012,autumn,PHYS,121/AAA.json']
            self.assertRaises(DataFailureException,
                              SectionSws.get_linked_sections, section)


    def test_sections_by_instructor_and_term(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = Term(quarter="summer", year=2013)
            instructor = Person(uwregid="FBB38FE46A7C11D5A4AE0004AC494FFE")

            sections = SectionSws.get_sections_by_instructor_and_term(instructor, term)
            self.assertEquals(len(sections), 1)

    def test_sections_by_delegate_and_term(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = Term(quarter="summer", year=2013)
            delegate = Person(uwregid="FBB38FE46A7C11D5A4AE0004AC494FFE")

            sections = SectionSws.get_sections_by_delegate_and_term(delegate, term)
            self.assertEquals(len(sections), 2)

    def test_sections_by_curriculum_and_term(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = Term(quarter="winter", year=2013)
            curriculum = Curriculum(label="ENDO")
            sections = SectionSws.get_sections_by_curriculum_and_term(curriculum, term)

            self.assertEquals(len(sections), 2)

            # Valid curriculum, with no file
            self.assertRaises(DataFailureException,
                              SectionSws.get_sections_by_curriculum_and_term,
                              Curriculum(label="FINN"),
                              term)

    def test_instructor_published(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Published Instructors
            pi_section = SectionSws.get_section_by_label('2013,summer,B BIO,180/A')
            self.assertEquals(pi_section.meetings[0].instructors[0].TSPrint, True)

            # Unpublished Instructors
            upi_section = SectionSws.get_section_by_label('2013,summer,MATH,125/G')
            self.assertEquals(upi_section.meetings[0].instructors[0].TSPrint, False)

    def test_secondary_grading(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):


            section1 = SectionSws.get_section_by_label('2012,summer,PHYS,121/A')
            self.assertEquals(section1.allows_secondary_grading, True,
                              "Allows secondary grading")

            for linked in SectionSws.get_linked_sections(section1):
                self.assertEquals(linked.allows_secondary_grading, True,
                                  "Allows secondary grading")

            section2 = SectionSws.get_section_by_label('2013,winter,EMBA,503/A')
            self.assertEquals(section2.allows_secondary_grading, False,
                              "Does not allow secondary grading")

    def test_grading_period_open(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = SectionSws.get_section_by_label('2012,summer,PHYS,121/A')

            self.assertEquals(section.is_grading_period_open(), False, "Grading window is not open")

            # Spring 2013 is 'current' term
            section = SectionSws.get_section_by_label('2013,spring,MATH,125/G')

            self.assertEquals(section.is_grading_period_open(), True, "Grading window is open")

    def test_canvas_sis_ids(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Primary section containing linked secondary sections
            section = SectionSws.get_section_by_label('2012,summer,PHYS,121/A')
            self.assertEquals(section.canvas_course_sis_id(),
                '2012-summer-PHYS-121-A', 'Canvas course SIS ID')
            self.assertRaises(InvalidCanvasSection,
                              section.canvas_section_sis_id)

            # Primary section with no linked sections
            section = SectionSws.get_section_by_label('2013,autumn,REHAB,585/A')
            self.assertEquals(section.canvas_course_sis_id(),
                '2013-autumn-REHAB-585-A', 'Canvas course SIS ID')
            self.assertEquals(section.canvas_section_sis_id(),
                '2013-autumn-REHAB-585-A--', 'Canvas section SIS ID')

            # Secondary (linked) section
            section = SectionSws.get_section_by_label('2013,autumn,PHYS,121/AB')
            self.assertEquals(section.canvas_course_sis_id(),
                '2013-autumn-PHYS-121-A', 'Canvas course SIS ID')
            self.assertEquals(section.canvas_section_sis_id(),
                '2013-autumn-PHYS-121-AB', 'Canvas section SIS ID')

            # Independent study section
            section = SectionSws.get_section_by_label('2013,summer,PHIL,600/A')

            # ..missing instructor regid
            self.assertRaises(InvalidCanvasIndependentStudyCourse,
                              section.canvas_course_sis_id)

            section.independent_study_instructor_regid = 'A9D2DDFA6A7D11D5A4AE0004AC494FFE'
            self.assertEquals(section.canvas_course_sis_id(),
                '2013-summer-PHIL-600-A-A9D2DDFA6A7D11D5A4AE0004AC494FFE',
                'Canvas course SIS ID')
            self.assertEquals(section.canvas_section_sis_id(),
                '2013-summer-PHIL-600-A-A9D2DDFA6A7D11D5A4AE0004AC494FFE--',
                'Canvas section SIS ID')

