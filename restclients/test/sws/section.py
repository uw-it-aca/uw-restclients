from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.exceptions import DataFailureException, InvalidSectionID

class SWSTestSectionData(TestCase):
    def test_section_by_label(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
        
            #Valid data, shouldn't throw any exceptions
            sws.get_section_by_label('2012,summer,TRAIN,100/A')
            sws.get_section_by_label('2012,summer,TRAIN,101/A')
            sws.get_section_by_label('2012,summer,TRAIN,102/A')
            sws.get_section_by_label('2012,summer,TRAIN,103/A')
            sws.get_section_by_label('2012,summer,TRAIN,104/A')
            sws.get_section_by_label('2012,summer,PHYS,121/A')
            sws.get_section_by_label('2012,summer,PHYS,121/AC')
            sws.get_section_by_label('2012,summer,PHYS,121/AQ')
            sws.get_section_by_label('2012,summer,TEST,098/T')
            sws.get_section_by_label('2012,summer,B BIO,180/A')
            sws.get_section_by_label('2012,summer,B BIO,180/AA')
            sws.get_section_by_label('2012,summer,EDC&I,461/A')
            sws.get_section_by_label('2012,summer,CSS,161/A')
            sws.get_section_by_label('2012,summer,T BUS,310/A')
            sws.get_section_by_label('2012,summer,MATH,125/G')
            sws.get_section_by_label('2012,summer,MATH,125/GA')
            sws.get_section_by_label('2012,summer,TEDADM,572/A')
            sws.get_section_by_label('2012,summer,TMATH,110/A')
            sws.get_section_by_label('2012,summer,ELCBUS,451/A')

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
            section = sws.get_section_by_label('2012,summer,TRAIN,100/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TRAIN,101/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TRAIN,102/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TRAIN,103/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TRAIN,104/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,PHYS,121/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,PHYS,121/AC')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,PHYS,121/AQ')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,B BIO,180/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,B BIO,180/AA')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,CSS,161/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,T BUS,310/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TEST,098/T')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TRAIN,101/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,MATH,125/G')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,MATH,125/GA')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,EDC&I,461/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TEDADM,572/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,TMATH,110/A')
            sws.get_linked_sections(section)
            section = sws.get_section_by_label('2012,summer,ELCBUS,451/A')
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


