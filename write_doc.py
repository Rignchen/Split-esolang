import re
from sys import argv
from os import path, getcwd, popen, listdir
from datetime import date

# get filename
if len(argv) > 1:
	file = argv[1]
else:
	file = input("Filename: ")

# basic io functions
def read_file(filename: str):
	with open(filename,encoding="utf-8") as f:
		return f.read()
def write_file(filename: str, content: str):
	with open(filename, "w",encoding="utf-8") as f:
		f.write(content)

# global variables
REGEX = {
	"tableau":"^\|(.+\|)+$",
	"list":"^- ",
	"line": "^-+$",
	"title": "^#+ .+$",
	"code": "^```$",
	"comment": "^\[[^\]\[]+\]: <> \(.+\)$\n", # this is markdown comment syntax
}
CONST_TEXT = {
	"line_break": "<br>"
}
file_content = re.sub(REGEX["comment"],"",read_file(file).replace("\\n", CONST_TEXT["line_break"])).split("\n")
out = []
index = 0

# parse document
def tableau():
	global index, out
	out += ['{| class="wikitable"']
	for i in file_content[index][1:-1].split("|"):
		out += [f"!{i.strip()}"]
	index += 1
	if re.match("^\|(-+\|)+$", file_content[index]): index += 1
	while index < len(file_content):
		line = file_content[index]
		if not re.match(REGEX["tableau"], line): 
			index -= 1
			break
		out += ["|-"]
		index += 1
		for i in line[1:-1].split("|"):
			if i.startswith("§"):
				text = f"<code>{i[1:].strip()}</code>"
			else:
				text = i.strip()
			out += [f"|{text}"]
	out += ["|}",""]
def code():
	global index, out
	index += 1
	while index < len(file_content):
		line = file_content[index]
		if re.match(REGEX["code"], line):
			break
		out += [f" {line}"]
		index += 1
	out += [""]

# get wifi page credentials
if not file_content[0].startswith(r"{{infobox proglang"):
	dir_name = path.basename(getcwd())
	current_year = date.today().year
	if git := ".git" in listdir():
		created_by = popen("git config --global --get user.name").read().strip()
		url = popen("git remote get-url origin").read().strip()

	out += [
		r"{{infobox proglang",
		f"|name={dir_name}",
		f"|author=[[User:{created_by}|{created_by}]]" if git else "|author=",
		f"|year=[[:Category:{current_year}|{current_year}]]",
		"|memsys=",
		"|dimensions=",
		"|class=[[:Category:Turing complete|Turing complete]]",
		f"|refimpl=[{url} {dir_name}]" if git else "|refimpl=",
		f"|files=<code>.{dir_name.lower()}</code>",
		r"}}",""
	]
else:
	while index < len(file_content) and not file_content[index].startswith(r"}}"):
		out += [file_content[index]]
		index += 1

# read doc file
while index < len(file_content):
	line = file_content[index]
	if re.match(REGEX["tableau"], line):
		tableau()
	elif re.match(REGEX["code"], line):
		code()
	elif re.match(REGEX["list"], line):
		out += [f"* {line[2:]}"]
	elif re.match(REGEX["line"], line):
		out += ["----"]
	elif re.match(REGEX["title"], line):
		# get the number of # at the beginning of the line
		n = len(re.match("^#+", line).group())
		out += [f"{'='*(n+1)}{line[n+1:].title()}{'='*(n+1)}"]
	else:
		line = line.strip()
		if len(line) > 0 and index + 1 < len(file_content) and len(file_content[index+1].strip()) > 0:
			has_next = True
			for i in REGEX.values():
				if re.match(i, file_content[index+1]):
					has_next = False
					break
			if has_next:
				line += CONST_TEXT["line_break"]
		if len(line) > 0 and index > 0 and line[0].islower():
			has_no_previous = False
			for i in REGEX.values():
				if re.match(i, file_content[index-1]):
					has_no_previous = True
					break
			if has_no_previous or len(file_content[index-1].strip()) == 0:
				line = line[0].upper() + line[1:]
		out += [line]
	index += 1

# Categoies
out += [
	"",
	"[[Category:Languages]]",
	f"[[Category:{date.today().year}]]",
	"[[Category:Turing complete]]",
	"[[Category:Implemented]]"
]

write_file(file + ".mediawiki", "\n".join(out))
print("Done.")

"""
This script is used to convert a custom formated but readable file to a mediawiki file.
This script is not perfect and isn't meant to replace every manual work, but it can help to save time.

In some cases, some characters needs to be changed:
| -> &vert;
' ' -> &nbsp;
& -> &amp;
"""
