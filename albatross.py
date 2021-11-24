import csv
from os.path import isfile
from colorama import Fore, Style

class Round:

	def __init__(self, fairways_hit, fairways_possible, greens_in_regulation, up_and_downs, putts, score, round_number):
	
		self.fairways_hit = fairways_hit
		self.fairways_possible = fairways_possible
		self.fairways_hit_percentage = round((fairways_hit / fairways_possible) * 100, 2)
		self.greens_in_regulation = greens_in_regulation
		self.greens_in_regulation_percentage = round((greens_in_regulation / 18) * 100, 2)
		self.up_and_downs = up_and_downs
		self.scrambling_percentage = None if (greens_in_regulation == 18) else round(((up_and_downs / (18 - greens_in_regulation)) * 100), 2)
		self.putts = putts
		self.score = score
		self.round_number = round_number
		
	
	def print_stats_str(self):
	
		print("\nRound", self.round_number)
		
		if self.score < 72:
			print(f"Score: {Fore.GREEN}" + str(self.score) + f"{Style.RESET_ALL}")
		elif self.score > 72:
			print(f"Score: {Fore.RED}" + str(self.score) + f"{Style.RESET_ALL}")
		else:
			print(f"Score: {Fore.YELLOW}" + str(self.score) + f"{Style.RESET_ALL}")
		
		if round(self.fairways_hit / self.fairways_possible, 2) >= .58:
					print(f"Driving Accuracy: {Fore.GREEN}" + str(self.fairways_hit) + "/" + str(self.fairways_possible) + f"{Style.RESET_ALL} ({Fore.GREEN}" + str(self.fairways_hit_percentage) + f"%{Style.RESET_ALL})")
		else:
			print(f"Driving Accuracy: {Fore.RED}" + str(self.fairways_hit) + "/" + str(self.fairways_possible) + f"{Style.RESET_ALL} ({Fore.RED}" + str(self.fairways_hit_percentage) + f"%{Style.RESET_ALL})")
		
		if round(self.greens_in_regulation / 18, 2) >= .65:
			print(f"Greens In Regulation: {Fore.GREEN}" + str(self.greens_in_regulation) + f"/18 {Style.RESET_ALL}({Fore.GREEN}" + str(self.greens_in_regulation_percentage) + f"%{Style.RESET_ALL})")
		else:
			print(f"Greens In Regulation: {Fore.RED}" + str(self.greens_in_regulation) + f"/18 {Style.RESET_ALL}({Fore.RED}" + str(self.greens_in_regulation_percentage) + f"%{Style.RESET_ALL})")
		
		if round(self.up_and_downs / (18 - self.greens_in_regulation), 2) >= .57:
			print(f"Scrambling: {Fore.GREEN}" + str(self.up_and_downs) + "/" + str(18 - self.greens_in_regulation) + f"{Style.RESET_ALL} ({Fore.GREEN}" + str(self.scrambling_percentage) + f"%{Style.RESET_ALL})")
		else:
			print(f"Scrambling: {Fore.RED}" + str(self.up_and_downs) + "/" + str(18 - self.greens_in_regulation) + f"{Style.RESET_ALL} ({Fore.RED}" + str(self.scrambling_percentage) + f"%{Style.RESET_ALL})")
		
		if self.putts <= 29:
			print(f"Putts: {Fore.GREEN}" + str(self.putts) + f"{Style.RESET_ALL}")
		else:
			print(f"Putts: {Fore.RED}" + str(self.putts) + f"{Style.RESET_ALL}")	

class Model_Profile:

	def __init__(self, name, fairways_hit_percentage, greens_in_regulation_percentage, scrambling_percentage, putts_per_round, scoring_average):
		
		self.name = name
		self.fairways_hit_percentage = fairways_hit_percentage
		self.greens_in_regulation_percentage = greens_in_regulation_percentage
		self.scrambling_percentage = scrambling_percentage
		self.putts_per_round = putts_per_round
		self.scoring_average = scoring_average
	
	def print_stats_str(self):
		
		print("\n" + self.name)
		
		if self.scoring_average < 72:
			print(f"Scoring Average: {Fore.GREEN}" + str(self.scoring_average) + f"{Style.RESET_ALL}")
		elif self.scoring_average > 72:
			print(f"Scoring Average: {Fore.RED}" + str(self.scoring_average) + f"{Style.RESET_ALL}")
		else:
			print(f"Scoring Average: {Fore.YELLOW}" + str(self.scoring_average) + f"{Style.RESET_ALL}")
		
		if self.fairways_hit_percentage >= .58:
					print(f"Fairways: {Fore.GREEN}" + str(self.fairways_hit_percentage) + f"%{Style.RESET_ALL}")
		else:
					print(f"Fairways: {Fore.RED}" + str(self.fairways_hit_percentage) + f"%{Style.RESET_ALL}")
		
		if self.greens_in_regulation_percentage >= .65:
			print(f"Greens In Regulation: {Fore.GREEN}" + str(self.greens_in_regulation_percentage) + f"%{Style.RESET_ALL}")
		else:
			print(f"Greens In Regulation: {Fore.RED}" + str(self.greens_in_regulation_percentage) + f"%{Style.RESET_ALL}")
		
		if self.scrambling_percentage >= .57:
			print(f"Scrambling: {Fore.GREEN}" + str(self.scrambling_percentage) + f"%{Style.RESET_ALL}")
		else:
			print(f"Scrambling: {Fore.RED}" + str(self.scrambling_percentage) + f"%{Style.RESET_ALL}")
		
		if self.putts_per_round <= 29:
			print(f"Putting Average: {Fore.GREEN}"  + str(self.putts_per_round) + f"{Style.RESET_ALL} Putts Per Round")
		else:
			print(f"Putting Average: {Fore.RED}"  + str(self.putts_per_round) + f"{Style.RESET_ALL} Putts Per Round")


class Player_Profile:			
	
	def __init__(self):
		
		self.fairways_hit = 0
		self.fairways_possible = 0
		self.fairways_hit_percentage = None
		self.greens_in_regulation = 0
		self.greens_in_regulation_percentage = 0
		self.up_and_downs = 0
		self.scrambling_percentage = None
		self.putts = 0
		self.putts_per_round = 0
		self.putts_per_hole = 0
		self.scoring_average = 0
		self.total_rounds = 0
		self.rounds = []
		
		if isfile("test.csv"):
			with open("test.csv", "r+", newline="") as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=",")
				line_count = 0
				for row in csv_reader:
					if line_count > 0:
						new_round = Round(int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), line_count)
						self.update(new_round)
					line_count += 1

  
	def update(self, new_round):
		
		self.rounds.append(new_round)
		self.total_rounds += 1
		self.fairways_hit += new_round.fairways_hit
		self.fairways_possible += new_round.fairways_possible
		self.fairways_hit_percentage = round((self.fairways_hit / self.fairways_possible) * 100, 2)
		self.greens_in_regulation += new_round.greens_in_regulation
		self.greens_in_regulation_percentage = round((self.greens_in_regulation / (self.total_rounds * 18)) * 100, 2)
		self.up_and_downs += new_round.up_and_downs
		self.scrambling_percentage = round(self.scrambling_percentage if (new_round.greens_in_regulation == 18) else ((self.up_and_downs / ((self.total_rounds * 18) - self.greens_in_regulation)) * 100), 2)
		self.putts += new_round.putts
		self.putts_per_round = round(((self.putts_per_round * (self.total_rounds - 1)) + new_round.putts) / self.total_rounds , 2)
		self.putts_per_hole = round(self.putts_per_round / 18, 2)
		self.scoring_average = round(((self.scoring_average * (self.total_rounds - 1)) + new_round.score) / self.total_rounds, 2)

	
	def compare(self, model_profile):
		
		fairways_hit_percent_comp = round(self.fairways_hit_percentage - model_profile.fairways_hit_percentage, 2)
		fairways_hit_comp = round((fairways_hit_percent_comp / 100) * 18, 2)
		greens_in_regulation_percent_comp = round(self.greens_in_regulation_percentage - model_profile.greens_in_regulation_percentage, 2)
		greens_in_regulation_comp = round((greens_in_regulation_percent_comp / 100) * 18, 2)
		scrambling_percent_comp = round(self.scrambling_percentage - model_profile.scrambling_percentage, 2)
		scrambling_comp = round( (scrambling_percent_comp / 100) * (((self.greens_in_regulation_percentage - 100) / 100) * 18), 2)
		putts_comp = round(self.putts_per_round - model_profile.putts_per_round, 2)
		score_comp = round(self.scoring_average - model_profile.scoring_average, 2)
		
		return fairways_hit_percent_comp, fairways_hit_comp, greens_in_regulation_percent_comp, greens_in_regulation_comp, scrambling_percent_comp, scrambling_comp, putts_comp, score_comp
	
	def print_comp_str(self, model_profile):
		
		print("\nYou vs " + str(model_profile.name) + " (On Average)")
		fairways_hit_percent_comp, fairways_hit_comp, greens_in_regulation_percent_comp, greens_in_regulation_comp, scrambling_percent_comp, scrambling_comp, putts_comp, score_comp = self.compare(model_profile)
		
		if fairways_hit_comp >= 0:
			print(f"Fairways: You Hit {Fore.GREEN}" + str(abs(fairways_hit_comp)) + " (" + str(abs(fairways_hit_percent_comp)) + f"%){Style.RESET_ALL} More Fairways")
		else:
			print(f"Fairways: You Hit {Fore.RED}" + str(abs(fairways_hit_comp)) + " (" + str(abs(fairways_hit_percent_comp)) + f"%){Style.RESET_ALL} Less Fairways")
		
		if greens_in_regulation_comp >= 0:
			print(f"Greens In Regulation: You Hit {Fore.GREEN}" + str(abs(greens_in_regulation_comp)) + " (" + str(abs(greens_in_regulation_percent_comp)) + f"%){Style.RESET_ALL} More Greens")
		else:
			print(f"Greens In Regulation: You Hit {Fore.RED}" + str(abs(greens_in_regulation_comp)) + " (" + str(abs(greens_in_regulation_percent_comp)) + f"%){Style.RESET_ALL} Less Greens")
		
		if scrambling_comp <= 0:
			print(f"Scrambling: You Made {Fore.GREEN}" + str(abs(scrambling_comp)) + " (" + str(abs(scrambling_percent_comp)) + f"%){Style.RESET_ALL} More Up & Downs")
		else:
			print(f"Scrambling: You Made {Fore.RED}" + str(abs(scrambling_comp)) + " (" + str(abs(scrambling_percent_comp)) + f"%){Style.RESET_ALL} Less Up & Downs")
		
		if putts_comp <= 0:
			print(f"Putts: You Made {Fore.GREEN}" + str(abs(putts_comp)) + f"{Style.RESET_ALL} More Putts Per Round")
		else:
			print(f"Putts: You Made {Fore.RED}" + str(abs(putts_comp)) + f"{Style.RESET_ALL} Less Putts Per Round")
		
		if score_comp <= 0:
			print(f"Scoring Average: You Had {Fore.GREEN}" + str(abs(score_comp)) + f"{Style.RESET_ALL} Less Strokes Per Round")
		else:
			print(f"Scoring Average: You Had {Fore.RED}" + str(abs(score_comp)) + f"{Style.RESET_ALL} More Strokes Per Round")
	
	
	def print_stats_str(self):
		
		print("\nYour Stats")
		print("Rounds Played:", self.total_rounds)
		
		if self.scoring_average < 72:
			print(f"Scoring Average: {Fore.GREEN}" + str(self.scoring_average) + f"{Style.RESET_ALL}")
		elif self.scoring_average > 72:
			print(f"Scoring Average: {Fore.RED}" + str(self.scoring_average) + f"{Style.RESET_ALL}")
		else:
			print(f"Scoring Average: {Fore.YELLOW}" + str(self.scoring_average) + f"{Style.RESET_ALL}")
		
		if round(self.fairways_hit / self.fairways_possible, 2) >= .58:
					print(f"Fairways: {Fore.GREEN}" + str(self.fairways_hit) + "/" + str(self.fairways_possible) + f"{Style.RESET_ALL} ({Fore.GREEN}" + str(self.fairways_hit_percentage) + f"%{Style.RESET_ALL})")
		else:
			print(f"Fairways: {Fore.RED}" + str(self.fairways_hit) + "/" + str(self.fairways_possible) + f"{Style.RESET_ALL} ({Fore.RED}" + str(self.fairways_hit_percentage) + f"%{Style.RESET_ALL})")
		
		if round(self.greens_in_regulation / (18 * self.total_rounds), 2) >= .65:
			print(f"Greens In Regulation: {Fore.GREEN}" + str(self.greens_in_regulation) + "/" + str(18 *self.total_rounds) + f"{Style.RESET_ALL} ({Fore.GREEN}" + str(self.greens_in_regulation_percentage) + f"%{Style.RESET_ALL})")
		else:
			print(f"Greens In Regulation: {Fore.RED}" + str(self.greens_in_regulation) + "/" + str(18 *self.total_rounds) + f"{Style.RESET_ALL} ({Fore.RED}" + str(self.greens_in_regulation_percentage) + f"%{Style.RESET_ALL})")
		
		if round(self.up_and_downs / ((18 * self.total_rounds) - self.greens_in_regulation), 2) >= .57:
			print(f"Scrambling: {Fore.GREEN}" + str(self.up_and_downs) + "/" + str((18 * self.total_rounds)- self.greens_in_regulation) + f"{Style.RESET_ALL} ({Fore.GREEN}" + str(self.scrambling_percentage) + f"%{Style.RESET_ALL})")
		else:
			print(f"Scrambling: {Fore.RED}" + str(self.up_and_downs) + "/" + str((18 * self.total_rounds) - self.greens_in_regulation) + f"{Style.RESET_ALL} ({Fore.RED}" + str(self.scrambling_percentage) + f"%{Style.RESET_ALL})")
		
		if self.putts <= 29:
			print(f"Putting Average: {Fore.GREEN}"  + str(self.putts_per_round) + "{Style.RESET_ALL} Putts Per Round ({Fore.GREEN}" + str(self.putts_per_hole) + f"{Style.RESET_ALL} Putts Per Hole)")
		else:
			print(f"Putting Average: {Fore.RED}"  + str(self.putts_per_round) + f"{Style.RESET_ALL} Putts Per Round ({Fore.RED}" + str(self.putts_per_hole) + f"{Style.RESET_ALL} Putts Per Hole)")

	def write_to_csv(self):
		
		HEADER=["Fairways Hit", "Fairways Possible", "Greens In Regulation", "Up & Downs", "Putts", "Score"]
		
		with open("test.csv", "w", newline="") as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(HEADER)
			
			for new_round in self.rounds:
				data = [new_round.fairways_hit, new_round.fairways_possible, new_round.greens_in_regulation, new_round.up_and_downs, new_round.putts, new_round.score]
				writer.writerow(data)		

 
tiger_woods_2000 = Model_Profile("Tiger Woods 2000", 71.22, 75.15, 67.08, 28.76, 67.79)
tiger_woods_2006 = Model_Profile("Tiger Woods 2006", 60.71, 74.15, 62.81, 29.38, 68.12)
jordan_spieth_2015 = Model_Profile("Jordan Spieth 2015", 62.91, 67.87, 65.03, 27.82, 68.93)
vijay_singh_2004 = Model_Profile("Vijay Singh 2004", 60.36, 73.03, 62.36, 29.24, 68.84)
rory_mcilroy_2014 = Model_Profile("Rory McIlroy 2014", 59.93, 69.44, 58.52, 28.59, 68.83)
brooks_koepka_2018 = Model_Profile("Brooks Koepka 2018", 56.85, 68.28, 63.28, 28.76, 69.44)

player = Player_Profile()
	
while True:
	
	option = input("\n(a)dd new round, (r)ound history, (s)tats, (c)ompare to the pros, (q)uit: ")
	
	if option in ["a", "A"]:
		while True:
			try:
				fairways_hit = int(input("\nFairways Hit: "))
				fairways_possible = int(input("Fairways Possible: "))
				greens_in_regulation = int(input("Greens In Regulation: "))
				up_and_downs = int(input("Successful Up & Downs: "))
				putts = int(input("Putts: "))
				score = int(input("Score: "))
				
				new_round = Round(fairways_hit, fairways_possible, greens_in_regulation, up_and_downs, putts, score, len(player.rounds) + 1)
				player.update(new_round)
				player.write_to_csv()
				
				player.rounds[-1].print_stats_str()
				player.print_stats_str()
				
				break
			
			except ValueError:
				print(f"\n{Fore.RED}Please input a valid value{Style.RESET_ALL}")
	elif option in ["r", "R"]:
		for new_round in player.rounds:
			new_round.print_stats_str()
	elif option in ["s", "S"]:
		player.print_stats_str()
	elif option in ["c", "C"]:
		while True:
			print("\n(1) Tiger Woods 2000, (2) Tiger Woods 2006, (3) Jordan Spieth 2015, (4) Vijay Singh 2004, (5) Rory McIlroy 2014, (6) Brooks Koepka 2018 (7) Average (8) Best Of")
			model_option = input("\nSelect a player/season: ")
			if model_option == "1":
				player.print_stats_str()
				tiger_woods_2000.print_stats_str()
				player.print_comp_str(tiger_woods_2000)
				break
			elif model_option == "2":
				player.print_stats_str()
				tiger_woods_2006.print_stats_str()
				player.print_comp_str(tiger_woods_2006)
				break
			elif model_option == "3":
				player.print_stats_str()
				jordan_spieth_2015.print_stats_str()
				player.print_comp_str(jordan_spieth_2015)
				break
			elif model_option == "4":
				player.print_stats_str()
				vijay_singh_2004.print_stats_str()
				player.print_comp_str(vijay_singh_2004)
				break
			elif model_option == "5":
				player.print_stats_str()
				rory_mcilroy_2014.print_stats_str()
				player.print_comp_str(rory_mcilroy_2014)
				break
			elif model_option == "6":
				player.print_stats_str()
				brooks_koepka_2018.print_stats_str()
				player.print_comp_str(brooks_koepka_2018)
				break
			else:
				print(f"\n{Fore.RED}Please input a valid option{Style.RESET_ALL}")
	elif option in ["q", "Q"]:
		break
	else:
		print(f"\n{Fore.RED}Please input a valid option{Style.RESET_ALL}")
	





