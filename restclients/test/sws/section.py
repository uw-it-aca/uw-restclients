from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.exceptions import DataFailureException, InvalidSectionID

class SWSTestSectionData(TestCase):
    def test_final_exams(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()

            section = sws.get_section_by_label('2013,summer,B BIO,180/A')
            self.assertEquals(section.final_exam, None, "No final exame for B BIO 180")

            section = sws.get_section_by_label('2013,summer,MATH,125/G')
            final_exam = section.final_exam

            self.assertEquals(final_exam.is_confirmed, False, "Final exame for Math 125 isn't confirmed")
            self.assertEquals(final_exam.no_exam_or_nontraditional, False, "Final exame for Math 125 isn't non-traditional")
            section = sws.get_section_by_label('2013,summer,TRAIN,101/A')
            final_exam = section.final_exam

            self.assertEquals(final_exam.is_confirmed, True, "Final exame for Train 101 is confirmed")
            self.assertEquals(final_exam.no_exam_or_nontraditional, False, "Final exame for Train 101 isn't non-traditional")
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
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
        
            #Valid data, shouldn't throw any exceptions
            sws.get_section_by_label('2013,summer,TRAIN,100/A')

            #Invalid data, should throw exceptions
            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              '')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              ' ')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              '2012')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              '2012,summer')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              '2012,summer,TRAIN')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              '2012, summer, TRAIN, 100')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              'summer, TRAIN, 100/A')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              '2012,fall,TRAIN,100/A')

            self.assertRaises(InvalidSectionID, 
                              sws.get_section_by_label, 
                              '-2012,summer,TRAIN,100/A')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '9999,summer,TRAIN,100/A')

            #Valid section labels, no files for them
            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2012,summer,TRAIN,110/A')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2012,summer,TRAIN,100/B')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2012,summer,PHYS,121/B')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2012,summer,PHYS,121/BB')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2010,autumn,G H,201/A')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2010,autumn,CS&SS,221/A')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2010,autumn,KOREAN,101/A')

            self.assertRaises(DataFailureException, 
                              sws.get_section_by_label, 
                              '2010,autumn,CM,101/A')

            
 
    #Failing because linked section json files haven't been made (Train 100 AA/AB)
    def test_linked_sections(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
            #Valid data, shouldn't throw any exceptions
            section = sws.get_section_by_label('2013,summer,TRAIN,100/A')
            sws.get_linked_sections(section)

            #Invalid data, should throw exceptions
            section.linked_section_urls = ['']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = [' ']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2012,summer,TRAIN,100/A']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['-2012,summer,TRAIN,100/A.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['9999,summer,TRAIN,100/A.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2012,summer,PHYS,121/B.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2010,autumn,CS&SS,221/A.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2010,autumn,KOREAN,101/A.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2010,autumn,G H,201/A.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2010,autumn,CM,101/A.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2012,autumn,PHYS,121/A.json', 
                                           '2012,autumn,PHYS,121/AC.json', 
                                           '2012,autumn,PHYS,121/BT.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)

            section.linked_section_urls = ['2012,autumn,PHYS,121/A.json', 
                                           '2012,autumn,PHYS,121/AC.json', 
                                           '2012,autumn,PHYS,121/AAA.json']
            self.assertRaises(DataFailureException, 
                              sws.get_linked_sections, section)


