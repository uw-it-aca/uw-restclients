from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.exceptions import DataFailureException, InvalidSectionID

class SWSTestSectionData(TestCase):
    def test_section_by_label(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()
        
            #Valid data, shouldn't throw any exceptions
            sws.get_section_by_label('2012,summer,TRAIN,100/A')
            sws.get_section_by_label('2012,summer,PHYS,121/A')
            sws.get_section_by_label('2012,summer,PHYS,121/AC')
            sws.get_section_by_label('2012,summer,PHYS,121/AQ')

            #Invalid data, should throw exceptions
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, '')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, ' ')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, '2012')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, '2012,summer')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, '2012,summer,TRAIN')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, '2012, summer, TRAIN, 100')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, 'summer, TRAIN, 100/A')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, '2012,fall,TRAIN,100/A')
            self.assertRaises(InvalidSectionID, sws.get_section_by_label, '-2012,summer,TRAIN,100/A')
            self.assertRaises(DataFailureException, sws.get_section_by_label, '2012,summer,TRAIN,102/A')
            self.assertRaises(DataFailureException, sws.get_section_by_label, '2012,summer,TRAIN,100/B')
            self.assertRaises(DataFailureException, sws.get_section_by_label, '9999,summer,TRAIN,100/A')
            self.assertRaises(DataFailureException, sws.get_section_by_label, '2012,summer,PHYS,121/AB')
