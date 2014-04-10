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
    if type(sections) == type(dict()):
        instructors = get_name_from_section(sections)
        return course_number, instructors, set()
    lec = sections[0]
    # We need to handle the X94s separately
    instructors = get_name_from_section(lec)
    if not instructors:
        import pdb; pdb.set_trace()
        print("something bad happened. could not get instructor name")
    # iterate through sections to obtain GSI names
    for section in sections[1:]:
        GSI_names = parse_section(section, set())
    return course_number, instructors, GSI_names

def parse_section(section, names):
    gsi_name = get_name_from_section(section)
    if gsi_name:
        try:
            if type(gsi_name) == type(list()):
                for name in gsi_name:
                    names.add(name)
            elif type(gsi_name) == str:
                names.add(gsi_name)
        except Exception:
            import pdb; pdb.set_trace()
    return names
    

def get_name_from_section(section):
    # might be list, might be dict
    try:
        meeting = section['sectionMeetings']
        if type(meeting) == type(list()):
            gsi_name = meeting[0]['instructorNames']
        elif type(meeting) == type(dict()):
            gsi_name = meeting['instructorNames']
        else:
            gsi_name = None
    except Exception:
        # maybe we can implement some kind of logging
        gsi_name = None
    return gsi_name

def parse_course_offerings(courses):
    class_info = []
    for course in courses:
        class_info.append(tuple(parse_class(course)))
    import pdb; pdb.set_trace()

r = parse_course_offerings(response_json['ClassOffering'])
