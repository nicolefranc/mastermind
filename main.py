import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.label import Label
import random

class Mastermind(App):
# 	def build(self):
# 		return Label(text="Hello World")

	def __init__(self):
		self.palette = ["red", "orange", "yellow", "green", "blue", "pink",  "violet", "black"]
		self.code = self.generate_code()

	""" Generates a set of 'code' for player to break

		@type --
		@param none
		@rtype: list
		@returns: A list of strings representing the 'code' the player needs to break
	"""
	def generate_code(self):
		return random.choices(self.palette, k=4)

	""" Checks the given guess/input and returns the hint

		@type guess: list
		@param guess: The given input by the player
		@rtype: list
		@returns: The hints generated based on player's input
	"""		
	def validate_pegs(self, pegs):
		''' 
			A colored or black key peg is placed for each code peg from the guess which is correct in both color and position. 
			A white key peg indicates the existence of a correct color code peg placed in the wrong position.
			If there are duplicate colours in the guess, they cannot all be awarded a key peg unless they correspond to the same number of duplicate colours in the hidden code.
			For example, if the hidden code is white-white-black-black and the player guesses white-white-white-black, 
			the codemaker will award two colored key pegs for the two correct whites, nothing for the third white as there is not a third white in the code, and a colored key peg for the black.
		'''
		code = self.code[:]
		print("Code copy:", code)
		print(code[3])
		key_pegs = []
		for idx, peg in enumerate(pegs):
			print("Peg:", idx, peg)
			print("Code index, value:", idx, code[idx])
			if peg == code[idx]:
				key_pegs.append("black")
				code[idx] = 0
		# filter: retrieves the values that doesn't satisfy the given condition into a list
		code = list(filter(lambda matched_val: matched_val != 0, code)) 
		print("New code:", code)
		for idx, peg in enumerate(pegs):
			if peg in code:
				key_pegs.append("green")
		return key_pegs

	""" Reverts the colors to the previous state

		@type current_list: list (String)
		@param current_list: The list of 'code' that the player wants to revert
		@rtype: list (String)
		@returns: A list of the reverted 'code'
	"""		
	def undo(self):
		pass



if __name__ == '__main__':
# 	Mastermind().run()
	mm = Mastermind()
	print("Code:", mm.code)
	
	for row in range(8):
		''' Ask for player input '''
		code_pegs = []
		for i in range(4): 
			inp = input(f"Guess #{i+1}:")
			code_pegs.append(inp)
		print("Code pegs from input:", code_pegs)
		''' Check validity of guess '''
		hints = mm.validate_pegs(code_pegs)
		print("Hints:", hints)
		
		# Check if there are 4 items in the list
		# Assess if all are black
		if len(hints) == 4:
			result = all(hint == "black" for hint in hints)
			if result:
				print(f"YOU WON!\nIt only took you {row+1} tries.")
				break