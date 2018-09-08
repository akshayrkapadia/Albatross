import math
import pickle
import argparse
import datetime
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from termcolor import colored

__author__ = "Akshay R. Kapadia"
__copyright__ = "Copyright 2018, Akshay R. Kapadia"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Akshay R. Kapadia"
__email__ = "akshayrkapadia@tutamail.com"
__status__ = "Development"


class NotEnoughRoundsError(Exception):
    pass


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


class Round:

    def __init__(self, date, course, score):
        self.date = datetime.datetime.strptime(date, "%m-%d-%Y").date()
        self.course = course
        self.score = score
        handicap_diff = (self.score - self.course.course_rating) * \
            (113.0 / self.course.slope_rating)
        self.handicap_diff = math.ceil(handicap_diff * 100) / 100.0


class Data:

    def __init__(self):
        try:
            with open(r'Golf_Stats.txt', 'rb') as f:
                data = pickle.load(f)
                self.rounds = data.rounds
                self.handicap_indexes = data.handicap_indexes
                self.scoring_averages = data.scoring_averages
                self.handicap_index = data.handicap_index
                self.scoring_average = data.scoring_average
                self.lowest_score = data.lowest_score
                self.handicap_index_change = data.handicap_index_change
                self.scoring_average_change = data.scoring_average_change
                self.courses = data.courses
        except IOError:
            self.rounds = []
            self.handicap_indexes = []
            self.scoring_averages = []
            self.handicap_index = None
            self.scoring_average = None
            self.lowest_score = None
            self.handicap_index_change = None
            self.scoring_average_change = None
            self.courses = []

    # Serializes the data to a file named "Golf_Stats.txt"
    def save(self):
        with open(r'Golf_Stats.txt', 'wb') as f:
            pickle.dump(self, f)

    # Adds a new round to the data
    def add_round(self, round):
        self.rounds.append(round)
        if round.course not in self.courses:
            self.courses.append(round.course)
        self.update()

    # Creates a pandas table for 20 of the most recent rounds
    def show_table(self):
        rounds = self.rounds
        if len(rounds) >= 20:
            rounds = rounds[len(rounds) - 20:]
        elif len(rounds) == 0:
            raise NotEnoughRoundsError
        table = []
        for i in range(0, len(rounds)):
            table.insert(0, [rounds[i].date, rounds[i].course.name,
                             rounds[i].score, rounds[i].handicap_diff])
        df = pd.DataFrame(data=table, columns=[
            "Date", "Course", "Score", "Handicap Differential"])
        print(df)

    # Shows handicap index, scoring average, lowest score, number of rounds, and a table of the most recent rounds
    def show_data(self):
        if len(self.rounds) > 5:
            if self.handicap_index >= 0:
                handicap_index = "+" + str(self.handicap_index)
            if self.handicap_index_change >= 0:
                print("Handicap: " + colored(handicap_index, "blue") +
                      colored(" (+" + str(self.handicap_index_change) + ")", "red"))
            else:
                print("Handicap: " + colored(handicap_index, "blue") +
                      colored(" (" + str(self.handicap_index_change) + ")", "green"))
            if self.scoring_average_change >= 0:
                print("Scoring Average: " + colored(self.scoring_average, "blue") +
                      colored(" (+" + str(self.scoring_average_change) + ")", "red"))
            else:
                print("Scoring Average: " + colored(self.scoring_average, "blue") +
                      colored(" (" + str(self.scoring_average_change) + ")", "green"))
        else:
            print("Handicap: " + colored(self.handicap_index, "blue"))
            print("Scoring Average: " + colored(self.handicap_index, "blue"))
        print("Lowest Round: " + colored(self.lowest_score, "green"))
        print("Number Of Rounds: " + colored(len(self.rounds), "blue"))
        self.show_table()

    # Updates the values for the handicap_index, scoring_average, and lowest_score
    def update(self):
        differentials = []
        for round in self.rounds:
            differentials.append(round.handicap_diff)
        differentials = np.array(differentials)
        if len(differentials) < 5:
            self.handicap_index = None
        else:
            if len(differentials) >= 20:
                differentials = differentials[len(differentials) - 20:]
            handicap_index = float(np.sum(differentials)) / len(differentials)
            self.handicap_index = math.ceil(handicap_index * 100) / 100.0
            self.handicap_indexes.append(self.handicap_index)
            if len(self.rounds) > 5:
                change = self.handicap_indexes[-1] - self.handicap_indexes[-2]
                self.handicap_index_change = math.ceil(change * 100) / 100.0
        scores = []
        for round in self.rounds:
            scores.append(round.score)
        scores = np.array(scores)
        self.lowest_score = np.min(scores)
        if len(scores) < 5:
            self.scoring_average = None
        else:
            if len(scores) >= 20:
                scores = scores[len(scores) - 20:]
            scoring_average = float(np.sum(scores)) / len(scores)
            self.scoring_average = math.ceil(scoring_average * 100) / 100.0
            self.scoring_averages.append(self.scoring_average)
            if len(self.rounds) > 5:
                change = self.scoring_averages[-1] - self.scoring_averages[-2]
                self.scoring_average_change = math.ceil(change * 100) / 100.0


def banner():
    print(colored("______________________________________________________________________________________", "green"))
    print(colored("""
       d8888 888 888               888
      d88888 888 888               888
     d88P888 888 888               888
    d88P 888 888 88888b.   8888b.  888888 888d888 .d88b.  .d8888b  .d8888b
   d88P  888 888 888 "88b     "88b 888    888P"  d88""88b 88K      88K
  d88P   888 888 888  888 .d888888 888    888    888  888 "Y8888b. "Y8888b.
 d8888888888 888 888 d88P 888  888 Y88b.  888    Y88..88P      X88      X88
d88P     888 888 88888P"  "Y888888  "Y888 888     "Y88P"   88888P'  88888P'
                                                                            """, "blue"))
    print(colored("                   -</Golf Statistical Analyzer/>-", "red"))
    print(colored("______________________________________________________________________________________", "green"))


def main():
    parser = argparse.ArgumentParser(
        prog="Albatross", description="Golf Stat Tracker For Linux", epilog="Albatross Copyright (C) 2018 Akshay R. Kapadia")
    subparsers = parser.add_subparsers(dest="command")  # Primary command
    a_subparser = subparsers.add_parser("add")
    s_subparser = subparsers.add_parser("show")

    # Add round parser
    a_subparser.add_argument("score", help="The 18 hole score", type=int)

    args = vars(parser.parse_args())

    data = Data()

    try:
        if args["command"] is None:
            banner()
            data.show_data()
        elif args["command"] == "add":
            date = str(input("Date (mm-dd-yyyy): "))
            course_name = input("Course Name: ").lower().title()
            course = None
            while course is None:
                for course, i in zip(data.courses, range(len(data.courses))):
                    if fuzz.partial_ratio(course_name, data.courses[i].name) > 75:
                        print(str(i) + ") " + colored(data.courses[i].name, "red") + "\n  Slope Rating: " +
                              colored(data.courses[i].slope_rating, "blue") + "\n  Course Rating: " + colored(data.courses[i].course_rating, "blue"))
                print(str(len(data.courses)) + ") Manuel Entry")
                print(str(len(data.courses) + 1) + ") Edit Course Name")
                while True:
                    course_index = int(input("Select A Course Number: "))
                    if course_index not in range(len(data.courses) + 2):
                        raise ValueError
                    elif course_index == len(data.courses):
                        course = Course(course_name, float(input("Slope Rating: ")),
                                        float(input("Course Rating: ")))
                        break
                    elif course_index == (len(data.courses) + 1):
                        course_name = str(input("Course Name: "))
                        break
                    else:
                        course = data.courses[course_index]
                        break
            data.add_round(Round(date, course, args["score"]))
            data.show_data()
        elif args["command"] == "show":
            data.show_data()
    except NotEnoughRoundsError:
        print(colored("Not Enough Rounds", "red"))
    # except ValueError:
    #     print(colored("Invalid Input", "red"))
    finally:
        data.save()


if __name__ == "__main__":
    main()
