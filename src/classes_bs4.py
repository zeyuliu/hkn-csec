from urllib2 import urlopen
from bs4 import BeautifulSoup

# Get current CS course ratings
cs_course_schedule_url = 'http://www.eecs.berkeley.edu/Scheduling/CS/schedule.html'

cs_request = urlopen(cs_course_schedule_url)

cs_courses = cs_request.read()

cs_soup = BeautifulSoup(cs_courses)

# Find the correct table
cs_course_table = cs_soup.find("div", {"id": "content"}).find("table")
