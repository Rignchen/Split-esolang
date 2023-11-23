"""
Split is an esoteric programming language that is based on the idea of splitting everything and annoying people.
The code is starts and ends with a numbers, everything between thoses are characters.
Before beeing interpreted, every character is converted to its ASCII value then the value is reduced by 25, new lines are removed (value bigger than 99 aren't allowed).
Every numbers are then grouped by 2 and converted to a character.

Once the code is converted, it splits the code in instructions
Instructions are separated by a : at 1/3 of the instruction.

There's 4 variables:
- Int: stores a chain of characters
- Str: stores a chain of numbers
- And: stores an index, it's used to get a part of int or str
- Help: stores the part of int or str that is currently used

Running the code starts at the end of the code and goes backward :)
"""

from sys import argv
if not "-k" in argv:
	from os import system, name
	system("cls" if name == "ntf" else "clear")

def error(message):
	"""Prints an error message in red and exits the program."""
	print("\033[91m" + message + "\033[0m")
	exit(1)

## Get the code
# Get the code from the file or from the user
if len(argv) >= 2:
	filename = argv[1]
	if filename.split(".")[-1] not in ["split", "fu", "fuckyou", "coddingsucks"]:
		error(f"Unknown extension: {filename.split('.')[-1]}")
	try:
		with open(filename, "r") as file:
			code = file.read()
	except FileNotFoundError:
		error(f"File not found: {filename}")
	except PermissionError:
		error(f"Permission denied: {filename}")
	except UnicodeEncodeError:
		error(f"Invalid character in file: {filename}")
else:
	code = []
	while True:
		try:
			code.append(input() + "\n")
		except KeyboardInterrupt:
			break
	code = "".join(code)[:-1]
# Compile the code to be readable
if "--Allready_Compiled" not in argv:
	# compile the code
	try: reduction = int(argv[argv.index("-r") + 1]) if "-r" in argv else 31
	except ValueError: error("Reduction should be a number")
	compiled = code[0]
	for char in code[1:-1]:
		compiled += str(ord(char) - reduction).zfill(2) if reduction <= ord(char) < (100 + reduction) else error(f"Invalid character: {char}")
	compiled += code[-1]

	# decript the compiled code
	code: list[str] = []
	for i in range(0,len(compiled),2):
		code.append(chr(int(compiled[i:i+2])))

	# Split the code
	compiled = []
	while ":" in code:
		index = code.index(":")
		if index*3-1 > len(code): error("Missing : potato")
		compiled.append("".join(code[:index*3]).replace(":", "", 1))
		if ":" in compiled[-1]: error("Too many :")
		code = code[index*3:]
	if len(code) > 0: error("Missing :")
	code = compiled
else: code = "".join(i.strip() for i in code.split("\n")).split(":")
