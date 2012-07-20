#!/usr/bin/python

#test_config = {'cert':'/usr/local/canvas_sis/canvas/certs/canvas.cac.washington.edu.cert', 'key':'/usr/local/canvas_sis/canvas/certs/canvas.cac.washington.edu.key', 'log':'/usr/local/canvas_sis/logs/prod/sws_client.log'}
test_base = '/home/jlaney/apps/restclients/'

import yaml
import sys
sys.path.append(test_base + 'lib')

from sws_client import SWSClient

f = open(test_base + 'config/sws_client.yml')
config = yaml.load(f)['production']
f.close()

#config.update(test_config)

client = SWSClient(config)

print client.get_section_by_id("2012,summer,A A,260/A")
print client.get_course_by_id("2012,summer,A A,260")

data = client.get_term('2012', 'summer')

#data = client.get_colleges({'campus_short_name':'SEATTLE'})

#data = client.get_curricula({'college_abbreviation':'NURS'})

#data = client.get_courses({'year':'2012','quarter':'summer','curriculum_abbreviation':'CSE'})

#data = client.get_section('2012,spring,A A,260/A')

#data = client.get_sections({'year':'2012','quarter':'summer','curriculum_abbreviation':'A A'})

#data = client.get_full_registrations({'curriculum_abbreviation':'A A', 'course_number':'260', 'section_id':'A'})

print len(data)

