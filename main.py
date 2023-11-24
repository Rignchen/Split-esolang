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
	global is_running
	if is_running:
		print("\033[91m" + message + "\033[0m")
		is_running = False
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

## Initialize the memory
Int: str = "" # chain of characters
Str: str = "" # chain of numbers
And: tuple[int, int] = (0, 0) # index, length  index and length of the part of Int or Str that you want to use
Help: tuple[str,str] = ("","") # value, type   part of Int or Str that you want to use

## Initialize other variables
is_running: bool = True
index = 0

## Make the functions
def get(memory: str) -> None:
	"""Returns the part of Int or Str that is currently used."""
	global Int, Str, And, Help
	match memory.title():
		case "Int":
			Help = (Int[And[0]:And[0]+And[1]],"Int")
		case "Str":
			Help = (Str[And[0]:And[0]+And[1]],"Str")
		case _:
			error(f"Invalid memory: {memory}")
def add_to_memory(memory: str) -> None:
	"""Adds Help to Int or Str."""
	global Int, Str, Help
	match memory.title():
		case "Str":
			if Help[0].startswith("-"):
				Str += Help[0].removeprefix("-")
				if Str.startswith("-"): Str = Str.removeprefix("-")
				else: Str = "-" + Str
			else:
				Str += Help[0]
		case "Int":
			Int += Help[0]
		case _:
			error(f"Invalid memory: {memory}")
def set_help(value: str, type: str) -> None:
	"""Sets Help to value and type to type."""
	global Help
	match type.title():
		case "Int":
			Help = (str(value), "Int")
		case "Str":
			Help = (str(int(value,7)),"Str")
		case _:
			error(f"Invalid type: {type}")
def set_and_length(length: int) -> None:
	"""Sets the length of and to length."""
	global And
	And = (And[0], length)
def set_and_index(index: int) -> None:
	"""Sets the index of and to index."""
	global And
	And = (index, And[1])

## Remove unnecessary variables
del argv, filename
try: del compiled, char
except NameError: pass

## Interpret the code
def interpret(command: str, arguments: list[str]) -> None:
	global is_running, Int, Str, And, Help
	match command.title():
		case "Split":
			"""Store the part of int/str given by And in Help."""
			get(arguments[0])
		case "Put":
			"""Adds a value at the end of Int or Str\n
			if help is an int and the value is < 0, the whole int is multiplied by -1"""
			add_to_memory(arguments[0])
		case "Ilen":
			"""Sets the Index of And"""
			set_and_index(int(arguments[0]))
		case "Ipset":
			"""Sets the length of And"""
			set_and_length(int(arguments[0]))
		case "Help":
			"""set the value and type of Help"""
			set_help(" ".join(arguments[0:-1]), arguments[-1])

## Run the code
while is_running and len(code) > index >= 0:
	index += 1
	instructions = code[-index].split(" ")
	try: interpret(instructions[0], instructions[1:])
	except: error("An error happend")

	# TODO Debug
	print("Help:", Help)
	print("And:", And)
	print("Str:", Str)
	print("Int:", Int)
