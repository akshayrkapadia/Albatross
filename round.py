import math
import datetime


class Round:

    def __init__(self, date, course, score):
        self.date = datetime.datetime.strptime(date, "%m-%d-%Y").date()
        self.course = course
        self.score = score
        handicap_diff = (self.score - self.course.course_rating) * \
            (113.0 / self.course.slope_rating)
        self.handicap_diff = math.ceil(handicap_diff * 100) / 100.0
