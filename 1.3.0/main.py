"""
ExpandScript
Eric Diskin
Version is at bottom
2018
"""
import sys
import os
import json
import time
#from threading import Thread

class thread (Thread):
   def __init__(self, ID, name, counter):
      super(thread, self).__init__()
      self.name = name

logged = []
PATH_R = './lib/canvas.expd'  # the path of file to EXEC

def typeInt(integer):
	try:
		integer = int(integer)
		return True
	except TypeError:
		return False

def getLines(path, MODE):
	if not MODE == 'FUNCTION':

		try:
			# try to find file
			with open(path, 'r') as file:
				lines = file.read().split('\n')

		except FileNotFoundError:
			# file not found
			error('File', 'File not found.', -1)

	else:
		lines = path.split('\n')

	return lines


#VARS
varz = {
	'0': '0',
	'1': '1',
	'2': '2',
	'3': '3',
	'4': '4',
	'5': '5',
	'6': '6',
	'7': '7',
	'8': '8',
	'9': '9'
}


class funs:
	"""a class for defining functions"""

	def __init__(self):
		self.funs = {}
		self.funs_args = {}

	def add(self, name, content, args):
		content = content.replace('%OP', '(').replace('%CP', ')')
		print('USER function\n~~~',content,'\n~~~')
		self.funs[name] = content
		self.funs_args[name] = args

	def defined(self, name):
		print(name, 'in funs:', name in self.funs)
		return name in self.funs

	def fun(self, name, args, line):
		done = self.funs[name]

		for x in range(len(self.funs_args[name])):
			done = done.replace(self.funs_args[name][x], args[x])

		if 'return' in done:
			for li in done.split('\n'):

				if 'return' in li:
					print('returning from function')
					retval = li[(li.index('return') + len('return')):]
					print('returnvalue:', retval)

					#namedex = line.index(name) + len(name)
					line = line.replace(name + '(' + ','.join(args) + ')', retval, 1)

		return (done, line)


funs = funs()


def join(arr, space=' '):
	return space.join(arr)


def error(etype='Unknown', content='An unknown error occured', linum=-1, path=''):
	#sys.exit('\n\n[:ERROR:]\n%sError:\n%s\nline:%s' % (etype,content,linum))
	pass


def speacialChars(strr):
	strr = strr.replace('%OP', '(').replace('%CP', ')').replace('%WS', '')
	return strr


def wordj(arr):
	return ' '.join(arr)


class bytec:
	"""creates bytecode"""

	def __init__(self, path='', content=''):
		self.path = path

	_bytecode = ''

	def add(self, *txts):
		self._bytecode += '\n'
		for i in txts:
			if type(i) != str:
				i = str(i)
			self._bytecode += i + ' '

	def finish(self):
		directory = os.path.dirname(self.path) + '/ExpandScript_Output_/'
		if not os.path.exists(directory):
			os.mkdir(directory)

		file = open(directory + os.path.split(self.path)
		            [1].split('.')[0] + '.expd-bytes', 'w')
		file.write(str(self._bytecode))
		file.close()

	def get(self):
		return self._bytecode

	def log(self, app):
		directory = os.path.dirname(PATH_R) + '/ExpandScript_Output_/'
		if not os.path.exists(directory):
			os.mkdir(directory)

		file = open(directory + os.path.split(PATH_R)
		            [1].split('.')[0] + '.expd-log', 'w')
		file.write('\n'.join(app))
		file.close()

	def FUN(self, name, args, line,itera,log):
		log('functioning')
		code = funs.fun(name, args, line)
		log('USER functio1n\n~~~', funs.fun(name, args, line)[0], '\n', '~~~')
		self._bytecode += EXEC(code[0], 'FUNCTION', itera + 1)
		return code[1]

	def finish_as_home(self):
		direct = (os.path.expanduser('$') +
		          '/ExpandScript_Output_/').replace('\\', '/')
		if not os.path.exists(direct):
			os.mkdir(direct)

		with open(direct + self.path.replace('\\', '/').split('/')[-1], 'w') as file:
			file.write(str(self._bytecode))

	def byte(self):
		self._bytecode = bytes(self._bytecode, 'utf8')


def EXEC(path, MODE='MAIN', itera=0):
	TIME_START = time.time()

	# var types:
	def log(*args, **kwargs):
		fargs = [''] * (len(args))
		sept = ' '
		endl = '\n'
		if 'sept' in kwargs:
			sept = kwargs['sept']

		if 'endl' in kwargs:
			endl = kwargs['endl']

		for i in range(len(args)):
			if type(i) != str:
				fargs[i] = str(args[i])
			else:
				fargs[i] = args[i]

		logged.append('\t' * itera + sept.join(fargs) + endl)
		byte.log(logged)
		print('\t' * itera, *fargs, sep=sept, end=endl)

	VAR_TYPES = [
            'int',
            'str',
            'bool',
	]

	#lines to skip in a block:
	skipLines = -1
	byte = bytec(path)

	lines = getLines(path, MODE)

	linum = 0  # line number

	def hasChar(arr, word):
		for i in arr:
			for x in word:
				if i == x:
					return True
		return False

	inComment = False

	for line in lines:
		linum += 1
		if skipLines > -1:
			skipLines -= 1
			continue

		log('reading line %s: %s' % (linum, line))
		line = line.strip()

		if line == '' or line == '\n' or line[0] == '^':
			continue

		if '::' in line:
			log('skipping comment')
			inComment = (inComment == False)
			if inComment:
				line = line.split('::')[1]

			else:
				line = line.split('::')[0]

		elif inComment:
			continue

		if hasChar(line, '^'):
			log('skipping comment')
			line = line.split('^')[0].strip()

		words = line.split(' ')

		for i in range(len(words)):

			words[i] = words[i].strip()

		for i in varz:
			line = line.replace('$' + i, varz[i])

		if hasChar(line, '(') and hasChar(line, ')'):
			# if line is a function
			_name = line.split('(')[0].strip().split()[-1]
			_args = line.split('(')[1].split(')')[len(
				line.split('(')[1].split(')')) - 2].split(',')
			log('function name:', _name)

			log('stripping args')
			for i in range(len(_args)):
				_args[i] = _args[i].strip()

			log('args stripped')

			line = line.replace(', ', ',').replace(' ,', ',').strip()
			if funs.defined(_name):
				line = byte.FUN(_name, _args, line,itera,log)
				words = line.split()
				log('line returned from function:', line)

			elif _name == 'rawjs':
				log('adding raw js')
				byte.add('js', line.split('(\'')[1].split('\')')[
				         len(line.split('(\'')[1].split('\')')) - 2])

			elif _name == 'rawhtml':
				log('adding raw html to body')
				byte.add('html', line.split('(\'')[1].split('\')')[
				         len(line.split('(\'')[1].split('\')')) - 2])

			elif _name == 'rawcss':
				log('adding raw css')
				byte.add('css', line.split('(\'')[1].split('\')')[
				         len(line.split('(\'')[1].split('\')')) - 2])

			elif _name == 'log':
				log('adding console statement')
				byte.add('log', join(_args))

			elif _name == 'do':
				if funs.defined(_args[0]) and typeInt(_args[1]):
					for timesDoneFun in range(int(_args[1])):
						log('done func',_args[0],timesDoneFun,'times.')
						line = byte.FUN(_args[0], _args[2:], line,itera,log)
						words = line.split()
				else:
					error('BultininFunc','Incorrect arguments for this function.')
					

			else:
				error('Define', 'An item on this line is not defined in file: %s, in word: %s' % (
					path, _name), linum)

		if words[0] in VAR_TYPES:
			log('Getting variable')
			_type = words[0]
			_val = 'undefined'
			if not '$' in words[1]:
				error('Name', 'Invalid variable name', linum)

			_name = words[1].split('$')[1]
			if not _type in VAR_TYPES:
				error('Type', 'Not a valid variable type', linum, time)
			elif words[2] != '=':
				error('Syntax', 'Invalid syntax. (mssing =)', linum)

			elif _type == 'int':
				log('type is int')
				try:
					_val = words[3]

				except ValueError:
					error('Type', 'Not of type: int', linum, time)

			elif _type == "str":
				log('type str')
				if hasChar(line, "'"):
					word = words[3]
					strStart = word.index("'")
					_val = ' '.join(words[(words.index(word) + strStart):])

				else:
					error('String', 'Invalid str.', linum)

			elif _type == 'bool':
				bool_types = ['true', 'false']
				if not words[3] in bool_types:
					error('Bool', 'invalid bool', linum)

			log('setting variable')
			log('variable data:', 'ANONY')
			varz[_name] = _val

		elif hasChar(line, '$') and line[0] == '$' and '[' in line and ']' in line:
			log('Creating function')
			lini = linum + 1

			_name = line.split('[')[0][1:]
			_args = line.split('[')[1].split(']')[0].split(',')

			for x in _args:
				if len(x) > 0:
					if x[0] != '$':
						error('Syntax', 'Invalid variable', linum)

			content = []
			while True:
				log('\t\tvar lini is now', lini)
				cline = lines[lini]

				if len(cline) < 1:
					log('skipping...')

				elif cline[0] == '}':
					skipLines = lini - linum
					break

				else:
					log('<<LINE NOT RECG. ADDING>>')

				content.append(cline)
				lini += 1

			fin = '\n'.join(content)
			funs.add(_name, fin, _args)
			log('function created')

		if words[0] == '#inc':
			log('importing')
			if len(words) > 2:
				if not words[2] == 'from':
					error('Syntax', 'Invalid syntax.', linum, time)
				else:
					_path = words[3] + line.split('<')[1].split('>')[0] + '.expd'

			else:
				_path = './Lib/' + line.split('<')[1].split('>')[0] + '.expd'

			byte.add(EXEC(_path, 'MODULE', itera + 1))

	if MODE == 'MAIN':
		#byte.byte()

		byte.finish()  # finish_as_home for non-dev purposes

		compileHTML(byte.get(), path)
	elif MODE == 'MODULE' or MODE == 'FUNCTION':
		print('returned script')
		return byte.get()

	else:
		error('Compile', 'Unable to compile at this time.')

	log('COMPILE_TIME[0]:', round(time.time() - TIME_START, 3), 'S')
	return 0


def err(line):
	if line.strip() == '' or line.strip() == '\n':
		return True

	return False


def strip(line):
	fin = line.strip()
	fin = fin.replace('${VERSION}$', VERSION)
	return fin


def replaceSP(line):
	return line.replace('${TABS}$', '\t\t')


def wordsLen(words, num):
	if len(words) < num:
		error('Argument', 'Insufficint arguments', -1)


def compileHTML(code, path):

	#code = bytes.decode(code,'utf8')

	class compiled:
		"""this class is for making """

		def __init__(self):
			html = open('./html_compile/start_html.txt', 'r')
			self.html = html.read()
			html.close()

		js = """"""

		css = """"""

		htmlPlus = """"""

		def addHtml(self, *html):
			html = replaceSP(' '.join(html))
			self.htmlPlus += '\n\t' + html

		def addJs(self, *js):
			js = replaceSP(' '.join(js))
			self.js += '\n\t\t' + js

		def addCss(self, *css):
			css = replaceSP(' '.join(css))
			self.css += '\n\t\t' + css

		def bind(self):
			binded = self.html.replace('${HTML}$', self.htmlPlus).replace(
				'${JS}$', self.js, 1).replace('${CSS}$', self.css, 1).replace('${VERSION}$', VERSION, 1)
			return binded

	html = compiled()

	lines = code.split('\n')
	linum = 0

	for line in lines:
		linum += 1

		line = strip(line)
		words = line.split(' ')

		if err(line):
			continue

		if words[0] == 'log':
			# logs to the console
			wordsLen(words, 2)
			html.addJs('console.log(' + ', '.join(words[1:]) + ');')

		elif words[0] == 'js':
			wordsLen(words, 2)
			html.addJs(join(words[1:]))

		elif words[0] == 'html':
			wordsLen(words, 2)
			html.addHtml(join(words[1:]))

		elif words[0] == 'css':
			wordsLen(words, 2)
			html.addCss(join(words[1:]))

	with open(os.path.dirname(path) + '/ExpandScript_Output_/' + os.path.basename(path) + '.html', 'w') as output:
		output.write(html.bind())


VERSION = '0.1.6.0'

try:
	EXEC(PATH_R)
	#valid exeptions:
	execptions = [
		IndexError,
		FileExistsError,
		FileNotFoundError,
		FloatingPointError
	]
except Exception as e:  # set to the type of error getting
	bytec(PATH_R).log(logged)
	raise e

"""
name (current release {b:beta,a:alpha}) planned release version
Features to be added:
	do-loop (a1) 0.1.6.4
	random number generator () 0.1.7.0
	for-loop () 0.1.9.0
	while-loop () 0.1.9.0
	if/else statement () 0.1.8.0
	use threads to compile faster () 0.2.0.0

bug (status {0:active,1:in progress,2:mostly patched}).patch_version::(extra known information)::
bugs:
	functions inside calling function as argument (0)
	the error system outputs incorrect line number (1.2)	
	cn not call other functions from inside a function (2)
	if the length of a function is greater than 3 lines, it causes IndexError (2)
"""
