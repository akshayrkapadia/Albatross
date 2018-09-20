from termcolor import colored


class Course:

    def __init__(self, course_name, slope_rating, course_rating):
        self.name = course_name
        self.slope_rating = slope_rating
        self.course_rating = course_rating

    # Checks if the course name is equal to the given name
    def equals(self, other_course):
        if [self.name, self.slope_rating, self.course_rating] == [other_course.name, other_course.slope_rating, other_course.course_rating]:
            return True
        else:
            return False

    # Shows the course name, slope rating, and course rating
    def show_course(self):
        print("Course Name: " + colored(self.name, "blue"))
        print("Slope Rating: " + colored(self.slope_rating, "blue"))
        print("Course Rating: " + colored(self.course_rating, "blue"))
