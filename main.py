import libdw.sm as sm
import random
import subprocess
subprocess.call('', shell=True)

class Board:
	def __init__(self, rounds=8):
		self.palette = ["red", "green", "yellow", "blue", "pink", "cyan",  "violet", "white"]
		self.rounds = rounds
		self.secret_code = None
		self.generate_code()
		self.board = None
		print(self.display_board())
		
		
	def prRed(self,skk): 
		print("\033[91m {}\033[00m".format(skk)) 

	def generate_code(self):
		self.secret_code = random.choices(self.palette, k=4)
		print("=== FOR TESTING PURPOSE ONLY ===\n", self.secret_code)

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
			print("Peg to change: ", peg_data)

			self.board[row_idx][peg_idx] = self.add_color(color, peg_symbol)
		elif key_data != None:
			row_idx = self.rounds-1
			for i, key in enumerate(key_data):
				if key == "black":
					# replace with x
					self.board[row_idx][i+4] = "x"
				elif key == "green":
					# replace with o
					self.board[row_idx][i+4] = "o"

		# display an empty board
		else:
			peg_row = [peg, peg, peg, peg]
			key_row = [key, key, key, key]

			row = peg_row + key_row
			self.board = [row[:], row[:], row[:], row[:], row[:], row[:], row[:], row[:]]

		for row in self.board:
			row.insert(4, " | ")
		display_str = "M A S T E R M I N D\t\ttimer s\n\n"
		for row in self.board:
			display_str = display_str + "  ".join(row) + "\n\n"

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
		self.pegs.pop()

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
		print(self.secret_code)


INIT = "initialised"
MOVE_WAIT = "wait for move"
CONFIRM_WAIT = "wait for confirmation"
CONFIRM = "confirm" # end row
# UNDO = "undo"
WIN = "win"
END = "end"


COLORS = ["red", "green", "yellow", "blue", "pink", "cyan",  "violet", "white"]
class Mastermind(sm.SM):
	def __init__(self):
		# game initialised, code generated
		pegs = list()
		key_pegs = list()
		row_length = 4
		self.start_state = [INIT, RowPegs(pegs, key_pegs, row_length)]
		print("Game initialised.")

	def get_next_values(self, state, inp):
		current_state = state[0]
		row = state[1]
		
		if inp in COLORS and current_state == INIT:
			row.add_peg(inp)

			peg_length = row.get_peg_length()
			peg_data = (inp, row.rounds-1, peg_length-1)

			next_state = [MOVE_WAIT, row]
			output = row.display_board(peg_data)
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
				output += "\nConfirm?"
				next_state = [CONFIRM_WAIT, row]
				return next_state, output

			output = row.display_board(peg_data=peg_data)
			next_state = [MOVE_WAIT, row]
			return next_state, output

		elif inp == "Y" and current_state == CONFIRM_WAIT:
			# evaluate guess, get and display key pegs
			# round ends, round--
			# if not decoded, next state is init
			# else win
			is_decoded = row.validate_pegs()
			output = row.display_board(key_data=row.key_pegs)
			print("KEYS: ", row.key_pegs)
			if is_decoded:
				output += "\nIt is indeed you, Mr Holmes. Sherlock Holmes."
				next_state = [END, row]
			elif row.rounds == 1:
				output += "\nSeems like your luck ran out. Don't buy 4D."
				next_state = [END, row]
			else:
				row.reset()
				row.rounds -= 1
				print("NEXT ROUND:", row.rounds)
				next_state = [MOVE_WAIT, row]
			return next_state, output

		elif inp == "Q":
			output = "I DID NOT RAISE A QUITTER!\n\t\t-Your Mom"
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
		print("Code generated.\nYour turn, Sherlock.")

		# print(self.display_board())
		# palette = "Here are your choices:\n"
		# for color in COLORS:
		# 	palette += self.add_color(color, color) +  " "
		# print(palette)

		while(True):
			if (not self.done(self.state)):
					inp = input(">>>\t")
					output = self.step(inp)
					print(output)
			else:
				break
		print("Bye.")


Mastermind().run()