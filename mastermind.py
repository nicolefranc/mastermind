import libdw.sm as sm
import random
import subprocess
import time
import os
subprocess.call('', shell=True)

class Board:
	def __init__(self, rounds=8):
		self.palette = ["red", "green", "yellow", "blue", "pink", "cyan",  "violet", "white"]
		self.rounds = rounds
		self.secret_code = None
		self.generate_code()
		self.board = None
		
		
	def prRed(self,skk): 
		print("\033[91m {}\033[00m".format(skk)) 

	def generate_code(self):
		self.secret_code = random.choices(self.palette, k=4)
		# print("=== FOR TESTING PURPOSE ONLY ===\n", self.secret_code)

	def display_board(self, peg_data=None, key_data=None):
		peg_symbol = "[__]"
		peg = self.add_color("inactive", peg_symbol)
		key_symbol = "-"
		key = self.add_color("inactive", key_symbol)

		# make the peg changes here
		# board[0][0] = "c"
		if peg_data != None:
			color = peg_data[0]
			row_idx = peg_data[1]
			peg_idx = peg_data[2]
			# print("Peg to change: ", peg_data)
			self.board[row_idx][peg_idx] = self.add_color(color, peg_symbol)
		elif key_data != None:
			row_idx = self.rounds-1
			random.shuffle(key_data)
			for i, key in enumerate(key_data):
				if key == "black":
					# replace with x
					self.board[row_idx][i+5] = "x"
				elif key == "green":
					# replace with o
					self.board[row_idx][i+5] = "o"

		# display an empty board
		else:
			peg_row = [peg, peg, peg, peg]
			key_row = [key, key, key, key]

			row = peg_row + key_row
			row.insert(4, " | ")
			self.board = [row[:], row[:], row[:], row[:], row[:], row[:], row[:], row[:]]

		display_str = "\nM A S T E R M I N D\n\n"
		for row in self.board:
			display_str = display_str + "  ".join(row) + "\n\n"

		
		display_str += "\nYour choices:\n [ "
		for color in self.palette:
			display_str = display_str + self.add_color(color, color) + " " if color == self.palette[-1] else  display_str + self.add_color(color, color) + " / "
		display_str += "]\n"
		display_str += "\n\033[38;5;247mUnsure? Press\033[38;5;248m H \033[38;5;247mfor help. \nA quitter? Press \033[38;5;248mQ \033[38;5;247mto quit.\n"
		display_str += "In life, you can't undo. But here can. Press \033[38;5;248mB \033[38;5;247mto undo.\033[00m\n"
		return display_str
	
	def add_color(self, inp, str_to_color):
		colored_str = ""
		if inp == "red":
			colored_str = "\033[91m{}\033[00m"
		elif inp == "green":
			colored_str = "\033[92m{}\033[00m"
		elif inp == "yellow":
			colored_str = "\033[93m{}\033[00m"
		elif inp == "blue":
			colored_str = "\033[94m{}\033[00m"
		elif inp == "pink":
			colored_str = "\033[95m{}\033[00m"
		elif inp == "cyan":
			colored_str = "\033[96m{}\033[00m"
		elif inp == "violet":
			colored_str = "\033[35m{}\033[00m"
		elif inp == "white":
			colored_str = "\033[38;5;255m{}\033[00m"
		elif inp == "black":
			colored_str = "\033[90m{}\033[00m"
		elif inp == "inactive":
			colored_str = "\033[38;5;247m{}\033[00m"
		
		return colored_str.format(str_to_color)

	def show_code(self):
		reveal_str = "THE CODE:  "
		for color in self.secret_code:
			reveal_str += self.add_color(color, "[__]") + " "
		
		return reveal_str

class RowPegs(Board):
	def __init__(self, pegs, key_pegs, row_length):
		super().__init__()
		self.pegs = pegs
		self.key_pegs = key_pegs
		self.row_length = row_length

	def add_peg(self, peg):
		self.pegs.append(peg)

	def get_peg_length(self):
		return len(self.pegs)

	def undo(self):
		if len(self.pegs) != 0:
			self.pegs.pop()
			return True
		return False

	def validate_pegs(self):
		code = self.secret_code[:]
		pegs = self.pegs
		key_pegs = self.key_pegs
		for idx, peg in enumerate(pegs):
			if peg == code[idx]:
				key_pegs.append("black")
				code[idx] = 0
				pegs[idx] = 0

		for idx, peg in enumerate(pegs):
			if peg in code and peg != 0:
				key_pegs.append("green")
				code.remove(peg)
				
		is_decoded = all(key == "black" for key in key_pegs) if len(key_pegs) == 4 else False
		return is_decoded 

	def reset(self):
		self.pegs = list()
		self.key_pegs = list()
		# print(self.secret_code)


INIT = "initialised"
START = "start"
MOVE_WAIT = "wait for move"
CONFIRM_WAIT = "wait for confirmation"
CONFIRM = "confirm" # end row
# UNDO = "undo"
WIN = "win"
END = "end"


COLORS = ["red", "green", "yellow", "blue", "pink", "cyan",  "violet", "white"]

def convert_time(elapsed_time):
	hours, rem = divmod(elapsed_time, 3600)
	minutes, seconds = divmod(rem, 60)
	return "{:>2}m {:.0f}s".format(int(minutes),seconds) if int(minutes) > 0 else "{:.0f}s".format(seconds)

def clear_terminal():
	os.system('cls')

class Mastermind(sm.SM):
	def __init__(self):
		# game initialised, code generated
		pegs = list()
		key_pegs = list()
		row_length = 4
		self.start_state = [INIT, RowPegs(pegs, key_pegs, row_length)]
		self.start_time = time.time()
		# print(self.start_time)

	def get_next_values(self, state, inp):
		current_state = state[0]
		row = state[1]
		
		if inp == "" and current_state == INIT:
			next_state = [START, row]
			output = row.display_board()
			clear_terminal()
			return next_state, output

		elif inp in COLORS and current_state == START:
			row.add_peg(inp)

			peg_length = row.get_peg_length()
			peg_data = (inp, row.rounds-1, peg_length-1)

			next_state = [MOVE_WAIT, row]
			output = row.display_board(peg_data)
			clear_terminal()
			return next_state, output
		
		elif inp in COLORS and current_state == MOVE_WAIT:
			row.add_peg(inp)
			peg_length = row.get_peg_length()
			peg_data = (inp, row.rounds-1, peg_length-1)
			output = row.display_board(peg_data)

			# if last peg, wait for confirmation
			# else, wait for next move
			if peg_length == row.row_length:
				output += "\nYour code is"
				for color in row.pegs:
					output = output + " " + color 
				output += "\nPress Y to confirm."
				clear_terminal()
				next_state = [CONFIRM_WAIT, row]
				return next_state, output

			output = row.display_board(peg_data=peg_data)
			clear_terminal()
			next_state = [MOVE_WAIT, row]
			return next_state, output

		elif inp == "Y" and current_state == CONFIRM_WAIT:
			# evaluate guess, get and display key pegs
			# round ends, round--
			# if not decoded, next state is init
			# else win
			is_decoded = row.validate_pegs()
			output = row.display_board(key_data=row.key_pegs)
			# print("KEYS: ", row.key_pegs)
			end_time = time.time()
			elapsed_time = convert_time(end_time-self.start_time)
			if is_decoded:
				output += f"\n\n\n---\n\nYou solved it in {elapsed_time}!\n"
				output += row.show_code()
				output += "\n\nWeird flex but ok."
				clear_terminal()
				next_state = [END, row]
			elif row.rounds == 1:
				output += f"\n\n\n---\n\nSeems like you ran out of luck after {elapsed_time}.\n"
				output += row.show_code()
				output += "\n\nTook you long enough. Don't gamble."
				clear_terminal()
				next_state = [END, row]
			else:
				row.reset()
				row.rounds -= 1
				# print("NEXT ROUND:", row.rounds)
				clear_terminal()
				next_state = [MOVE_WAIT, row]
			return next_state, output

		elif inp == "B":
			peg_length = row.get_peg_length()
			success = row.undo()
			next_state = [MOVE_WAIT, row]
			peg_data = ("inactive", row.rounds-1, peg_length-1)
			output = row.display_board(peg_data) if success else "\nNothing to undo. Choose a color.\n"
			clear_terminal()
			return next_state, output

		elif inp == "H":
			output = "---\n\n Guess the code that I'm keeping secret.\n"
			output += " You will be given the following clues after every row:\n"
			output += "   x  -  you guessed the \033[92mright\033[00m color in the \033[92mcorrect\033[00m position\n"
			output += "   o  -  you guessed the \033[92mright\033[00m color but in the \033[91mwrong\033[00m position\n"
			output += " May you uncover your inner Sherlock Holmes. Good Luck!\n\n---"
			return state, output

		elif inp == "Q":
			end_time = time.time()
			elapsed_time = convert_time(end_time-self.start_time)
			output = "---\n\n  I DID NOT RAISE A QUITTER!\n\t - No longer your Mom\n\n  You are hereby disowned."
			output += f"\n  Although it only took you {elapsed_time} to quit. Well done."
			next_state = [END, None]
			return next_state, output

		elif current_state != INIT or current_state != END:
			output = "Not recognised. Try again."
			return state, output

	def done(self, state):
		current_state = state[0]
		# if current_state is at rounds = 0, return True
		# 	or all key_pegs are black, return True
		# else, return False
		return True if current_state == END else False
			

	def run(self):
		self.start()
		peg_count = 4

		# subprocess.call("", shell=True)
		print("Welcome welcome.")
		print("---\n\n Guess the code that I'm keeping secret.\n")
		print(" You will be given the following clues after every row:\n")
		print("   x  -  you guessed the \033[92mright\033[00m color in the \033[92mcorrect\033[00m position\n")
		print("   o  -  you guessed the \033[92mright\033[00m color but in the \033[91mwrong\033[00m position\n")
		print(" May you uncover your inner Sherlock Holmes. Good Luck!\n")
		print("Press ENTER to begin.\n\n---")

		while(True):
			if (not self.done(self.state)):
					inp = input(">>>  ")
					output = self.step(inp)
					print(output)
			else:
				break
		print("\n---\nFarewell.")


Mastermind().run()