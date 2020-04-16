import random

class Mastermind():
	def __init__(self):
		self.palette = ["red", "orange", "yellow", "green", "blue", "pink",  "violet", "black"]
		self.code = self.generate_code()

	def generate_code(self):
		return random.choices(self.palette, k=4)

	def validate_pegs(self, pegs):
		code = self.code[:]
		key_pegs = []
		for idx, peg in enumerate(pegs):
			if peg == code[idx]:
				key_pegs.append("black")
				code[idx] = 0

		for idx, peg in enumerate(pegs):
			if peg in code:
				key_pegs.append("green")
				code = [0 if value == peg else value for value in code]
		
		return key_pegs

	def undo(self):
		pass



if __name__ == '__main__':
	mm = Mastermind()
	
	for row in range(8):
		code_pegs = []
		print(f"Row {row+1}:")
		for i in range(4): 
			inp = input(f"Guess #{i+1}:")
			if inp == "exit":
				break
			code_pegs.append(inp)

		hints = mm.validate_pegs(code_pegs)
		print("Results:", *hints)
		
		# Check if there are 4 items in the list
		# Assess if all are black
		if len(hints) == 4:
			result = all(hint == "black" for hint in hints)
			if result:
				print(f"YOU WON!\nIt only took you {row+1} tries.")
				break