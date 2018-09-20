import math
import pickle
import numpy as np
import pandas as pd
from termcolor import colored


class NotEnoughRoundsError(Exception):
    pass


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
