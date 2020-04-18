import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.label import Label
import libdw.sm as sm
import random

class Board:
	def __init__(self, rounds=8):
		self.palette = ["red", "orange", "yellow", "green", "blue", "pink",  "violet", "black"]
		self.secret_code = None
		self.rounds = rounds
		self.generate_code()
		
	def generate_code(self):
		self.secret_code = random.choices(self.palette, k=4)
		print("=== FOR TESTING PURPOSE ONLY ===\n", self.secret_code)

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

class Mastermind(sm.SM, App):
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
		
		COLORS = row.palette
		
		if inp in COLORS and current_state == INIT:
			row.add_peg(inp)
			next_state = [MOVE_WAIT, row]
			output = f"Peg #{row.get_peg_length() + 1}"
			return next_state, output
		
		elif inp in COLORS and current_state == MOVE_WAIT:
			row.add_peg(inp)
			peg_length = row.get_peg_length()

			# if last peg, wait for confirmation
			# else, wait for next move
			if peg_length == row.row_length:
				output = "Your code is"
				for color in row.pegs:
					output = output + " " + color 
				output += "\nConfirm?"
				next_state = [CONFIRM_WAIT, row]
				return next_state, output

			output = f"Peg #{peg_length + 1}"
			next_state = [MOVE_WAIT, row]
			return next_state, output

		elif inp == "Y" and current_state == CONFIRM_WAIT:
			# evaluate guess, get and display key pegs
			# round ends, round--
			# if not decoded, next state is init
			# else win
			is_decoded = row.validate_pegs()
			output = row.key_pegs
			if is_decoded:
				output = f"{row.key_pegs}\nIt is indeed you, Mr Holmes. Sherlock Holmes."
				next_state = [END, row]
			elif row.rounds == 1:
				output = f"{row.key_pegs}\nSeems like your luck ran out. Don't buy 4D."
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

		print("Code generated.\nYour turn, Sherlock.")
		while(True):
			if (not self.done(self.state)):
					inp = input(">>>\t")
					output = self.step(inp)
					print(output)
			else:
				break
		print("Bye.")

Mastermind().run()
# if __name__ == '__main__':
# # 	Mastermind().run()
# 	mm = Mastermind()
	
# 	for row in range(8):
# 		code_pegs = []
# 		print(f"Row {row+1}:")
# 		for i in range(4): 
# 			inp = input(f"Guess #{i+1}:")
# 			if inp == "exit":
# 				break
# 			code_pegs.append(inp)
			
# 		hints = mm.validate_pegs(code_pegs)
# 		print("Results:", *hints)
# 		# Check if there are 4 items in the list
# 		# Assess if all are black
# 		if len(hints) == 4:
# 			result = all(hint == "black" for hint in hints)
# 			if result:
# 				print(f"YOU WON!\nIt only took you {row+1} tries.")
# 				break
