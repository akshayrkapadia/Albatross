#!/usr/bin/env python

import argparse
from fuzzywuzzy import fuzz
from termcolor import colored
from course import *
from round import *
from data import *

__author__ = "Akshay R. Kapadia"
__copyright__ = "Copyright 2018, Akshay R. Kapadia"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Akshay R. Kapadia"
__email__ = "akshayrkapadia@tutamail.com"
__status__ = "Development"


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
