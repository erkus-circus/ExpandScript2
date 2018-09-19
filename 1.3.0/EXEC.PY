"""
Lerk
Eric Diskin
2018
"""

import time, os, sys

def error(typeOfError,contentOfError, lineNum=0):
	sys.exit(typeOfError + 'Error:\n  ' + contentOfError + '\n  \tLine Number: ' + str(lineNum))

def run(path):

	for line in words:

		lineNum += 1
		wordNum = 0

		for w in line:
			oword = w
			def net(word):
				# returns and sets the next word
				word = line[line.index(word) + 1]
				return word

			wordNum += 1


	for mod in mods:
		# iterates through modules. the <main> modulehandles the main script
		with open(mod,'r') as m:
			#run module
			exec(m.read(),{
				'lines':lines,
			})
run('test.lerk2')