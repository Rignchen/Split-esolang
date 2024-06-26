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

def dd(*args):
	"""Prints the arguments and exits the program."""
	print(*args,end="")
	if input().lower().strip() in ["y","yes","yeah","yep","yup","yee","yeehaw","yeehaw!"]:
		exit(0)

from sys import argv
if not "-k" in argv:
	from os import system, name
	system("cls" if name == "ntf" else "clear")

## Custom chr & ord functions, used for the compilation part
custom_table = ['', "'", ',', 'C', 'J', '&', 'G', '÷', '"', '6', '4', 'i', 'A', 'p', 'K', 'y', 'T', 'P', '}', ';', 'q', '#', 'd', 'F', '1', 's', 'M', 'v', 'V', 'Z', '@', '2', '-', 'w', '!', '.', 'I', '<', 'B', '~', '7', 'e', '3', 'Q', '|', 'x', 't', 'f', 'ç', '0', 'L', 'a', 'g', '=', '5', '€', 'r', '_', 'l', ':', 'm', 'D', 'S', '\\', 'U', '+', ']', 'N', ')', '^', 'n', 'R', '$', 'X', '%', 'b', '?', '[', 'h', '9', 'O', 'µ', 'o', '/', ' ', 'Y', '8', '*', 'W', 'j', 'H', 'c', '>', '(', 'k', 'z', '{', '`', 'E', 'u']
def _ord(char: str) -> int:
	"""Returns the value of the character."""
	if char not in custom_table:
		raise ValueError(f"Invalid character: {char}")
	return custom_table.index(char)
def _chr(value: int) -> str:
	"""Returns the character of the value."""
	return custom_table[value % len(custom_table)]

## Initialize main variables
is_running: bool = True
index = 0

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
	if filename.split(".")[-1] not in ["split", "fu", "", "coddingsucks"]:
		error(f"Unknown extension: {filename.split('.')[-1]}")
	try:
		with open(filename, "r", encoding="utf-8") as file:
			code = file.read().replace("\n","").replace("\t","")
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

if len(code) <= 3: error("Not enougth character in the file")

# Compile the code to be readable
if "--Allready_Compiled" in argv:
	code = code.split(":")
else:
	# read the code and transform it into numbers
	compiled = code[0]
	for char in code[1:-1]:
		if char in custom_table:
			compiled += str(_ord(char)).zfill(2) 
		else:
			error(f"Invalid character: {char}")
	compiled += code[-1]

	# split the code in instructions
	# instructions are separated by a : at 1/3 of the instruction
	# every character are 2 numbers long
	# the ascii value of ":" is 58
	code = []
	num = 2
	while len(compiled) > 0:
		if len(compiled) < num*3:
			dd(code, compiled, num)
			error("Missing ':'")
		if compiled[num:num+2] == str(_ord(":")):
			code.append(compiled[:num] + compiled[num+2:num*3])
			compiled = compiled[num*3:]
			num = 2
		else:
			num += 2
	
	# turn the numbers back to characters
	code = ["".join([_chr(int(i[j:j+2])) for j in range(0,len(i),2)]) for i in code]

	# Remove unnecessary variables
	del compiled, char, num

## Remove unnecessary variables
del argv, filename

## Initialize the memory
Int: str = "" # chain of characters
Str: str = "" # chain of numbers
And: tuple[int, int] = (0, 0) # index, length  index and length of the part of Int or Str that you want to use
Help: tuple[str,str] = ("","") # value, type   part of Int or Str that you want to use

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
			if int(Help[0]) < 0:
				Str += Help[0].removeprefix("-")
				if Str.startswith("-"): Str = Str.removeprefix("-")
				else: Str = "-" + Str
			else:
				Str += Help[0]
		case "Int":
			Int += Help[0]
		case _:
			error(f"Invalid memory: {memory}")
def set_help(value: str, type: str, str_base: int = 10) -> None:
	"""Sets Help to value and type to type."""
	global Help
	match type.title():
		case "Int":
			Help = (str(value), "Int")
		case "Str":
			Help = (str(int(value,str_base)),"Str")
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
def calculate(operation: str) -> None:
	"""Calculates Help with operation, store the result in Help"""
	global Help
	length: int = len(Help[0])
	match Help[1]:
		case "Int":
			value = (
				"".join(str(ord(char)) for char in Help[0][:length//2]),
				"".join(str(ord(char)) for char in Help[0][length//2:])
			)
			match operation:
				case "+":
					Help = (
						chr(
							int(value[0]) +
							int(value[1])),
						"Int")
				case "-":
					Help = (
						chr(
							int(value[1]) -
							int(value[0])),
						"Int")
				case "*":
					Help = (
						chr(
							int(value[0]) *
							int(value[1])),
						"Int")
				case "%":
					Help = (
						chr(
							int(value[0]) %
							int(value[1])),
						"Int")
		case "Str":
			value = (
				int(Help[0][:length//2]),
				int(Help[0][length//2:])
			)
			match operation:
				case "+":
					Help = (
						str(
							value[0] +
							value[1]),
						"Str")
				case "-":
					Help = (
						str(
							value[0] -
							value[1]),
						"Str")
				case "*":
					Help = (
						str(
							value[0] *
							value[1]),
						"Str")
				case "%":
					Help = (
						str(
							value[0] %
							value[1]),
						"Str")
def numberToBase(number: int, base: int) -> str:
	if number == 0:
		return "0"
	if number < 0:
		return "-" + numberToBase(-number, base)
	digits = []
	while number:
		digits.append(int(number % base))
		number //= base
	return "".join([
		str(digit) if digit < 10 else chr(digit + ord("A") - 10)
		for digit in digits[::-1]
		])
def get_sum_value(string: list[str]) -> int:
	value = 0
	for i in string: value += ord(i)
	return value
def move(direction: int):
	global index
	while direction != index:
		if direction > index: index += 1
		else: index -= 1

		values = [i.title() for i in code[-index].split(" ")]
		if "Move" in values:
			value = int(values[values.index("Move") + 1])
			print(code[-index])
			print(f"{value} / {index} / {direction}")
			input(f"{value - index} * {direction - index}")
			if (value - index) * (direction - index) > 0:
				direction = value
	index -= 1

## Interpret the code
def interpret(command: str, arguments: list[str]) -> None:
	global is_running, Int, Str, And, Help
	match command.title():
		case "Run":
			"""Runs the Help as code."""
			temp = Help[0].title().split(" ")
			interpret(temp[0], temp[1:])
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
		case "Add":
			"""Adds the value to Help"""
			calculate("+")
		case "Reduce":
			"""Substracts the value to Help"""
			calculate("-")
		case "Multiply":
			"""Multiplies the value to Help"""
			calculate("*")
		case "Mod":
			"""Modulos the value to Help"""
			calculate("%")
		case "Help":
			"""set the value and type of Help"""
			set_help(" ".join(arguments[0:-1]), arguments[-1], 7)
		case "In":
			"""set the value and type of Help from the user's input"""
			set_help(input(), arguments[0])
		case "Reverse":
			"""Reverses Help"""
			match Help[1]:
				case "Str":
					Help = (str(-int(Help[0])), "Str")
				case "Int":
					Help = (
						"".join([
							char.lower() if char.isupper() 
							else char.upper()
							for char in Help[0]]),
						"Int")
		case "Display":
			"""Displays Help"""
			match Help[1]:
				case "Int":
					print(Help[0])
				case "Str":
					print(numberToBase(int(Help[0]), 11))
		case "If":
			"""If Str and Help is < 0, it runs the instruction after it\n
			If Int and sum(chr(Help)) < sum(char(argument[0])) run next value"""
			match Help[1]:
				case "Int":
					if get_sum_value(Help[0]) < get_sum_value(arguments[0]):
						interpret(arguments[1], arguments[2:])
				case "Str":
					if Help[0].startswith("-"):
						interpret(arguments[0], arguments[1:])
		case "Move":
			"""Move the code to the value in Help, if help is Int, it will move according to the sum of the arguments\n
			but it will also trigger every Move it finds"""
			global index
			match Help[1]:
				case "Int":
					move(int(arguments[0]))
				case "Str":
					index = int(Help[0])

## Run the code
while is_running and len(code) > index >= 0:
	index += 1

	# TODO Debug
	# print("Help:", Help)
	# print("And:", And)
	# print("Str:", Str)
	# print("Int:", Int)
	# print("Index:", index)

	instructions = code[-index].split(" ")
	try: interpret(instructions[0], instructions[1:])
	except: error("An error happend")


"""
commands:

Help| 		set the value and type of Help to the value and type you want| STR values are given in base 7| 																								Help 14 Str (put 11 in Help)
Put| 		Adds a value at the end of Int or Str|| 																																					Put Str (put the value of Help in Str)
Ilen| 		Sets the Index of And to the value you want|| 																																				Ilen 5 (put 5 as index of And)
Ipset| 		Sets the length of And to the value you want|| 																																				Ipset 8 (put 8 as length of And)
Split| 		Store the part of int/str given by And in Help|| 																																			Split Int (overide Help with the characters of Int selected by And)
Display| 	Display content of Help| STR: content is display as base 11| 																																Display
In| 		Set the value and type of Help from the user's input| STR: content is input as base 10| 																									In Str (put the user's input in Help)
Add| 		Split the content of Help and make the sum of the 2 parts| INT, convert the content to ascii and back| 																						Add
Reduce| 	Split the content of Help and make the substraction of the 2 parts| INT, convert the content to ascii and back| 																			Reduce
Multiply| 	Split the content of Help and make the multiplication of the 2 parts| INT, convert the content to ascii and back| 																			Multiply
Mod| 		Split the content of Help and make the modulo of the 2 parts| INT, convert the content to ascii and back| 																					Mod
Reverse| 	STR: multiply by -1 INT: upper case to lower case and lower case to upper case|| 																											Reverse
If| 		Check if Help is < 0| STR: use the sum of the ascii value of the characters| 																												If Display (Print Help if Help < 0)
Move| 		Move the currently executed instruction to the value in Help| STR: use the number written next to the instruction\nfollow every Move it finds on the way if it goes in the same direction| 	Move 1 (move to the first instruction)
Run|		Execute the code from the Help variables||																																					Run
"""
