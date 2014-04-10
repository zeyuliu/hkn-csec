import json
import urllib
import urllib2
from berkeley_api import BERKELEY_ID
from berkeley_api import BERKELEY_KEY

API_BASE_URL = 'https://apis-dev.berkeley.edu/cxf/asws/classoffering'

term = raw_input('Which term? (Spring/Fall)')
termYear = raw_input('Which year? (2014)')

cs_values = {
    'departmentCode': 'compsci',
    'term': term,
    'termYear': termYear,
    '_type': 'json',
    'app_id': BERKELEY_ID,
    'app_key': BERKELEY_KEY
    }

cs_data = urllib.urlencode(cs_values)
#cs_req = urllib2.Request(API_BASE_URL, cs_data)
response = urllib2.urlopen(API_BASE_URL+'?'+cs_data).read()

response_json = json.loads(response)

# Parses one class offering
def parse_class(class_offering):
    """
    Returns a 3 element tuple
        - course number
        - instructor name
        - TA names
    """
    title = class_offering['courseTitle']
    course_number = class_offering['courseNumber']
    sections = class_offering['sections']
    lec = sections[0]
    instructors = lec['sectionMeetings']['instructorNames']
    # iterate through sections to obtain GSI names
    GSI_names = set()
    for section in sections[1:]:
        GSI_names.add(section['sectionMeetings'][0]['instructorNames'])
    return course_number, instructors, GSI_names

def parse_course_offerings(courses):
    import pdb; pdb.set_trace()

class_info = parse_class(response_json['ClassOffering'][0])
