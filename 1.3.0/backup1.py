"""
ExpandScript
Eric Diskin
Version is at bottom
2018
"""
import sys, os, json, time, re 

logged = 0


def getLines(path,MODE):
	if not MODE == 'FUNCTION':

		try:
			# try to find file 
			with open(path,'r') as file:
				lines = file.read().split('\n')

		except FileNotFoundError:
			# file not found
			error('File','File not found.',-1)

	else:
		lines = path.split('\n')

	return lines


#VARS
varz = {
	'0':'0',
	'1':'1',
	'2':'2',
	'3':'3',
	'4':'4',
	'5':'5',
	'6':'6',
	'7':'7',
	'8':'8',
	'9':'9'
}


class funs:
	"""a class for defining functions"""
	def __init__(self):
		self.funs = {}
		self.funs_args = {}

	def add(self,name,content,args):
		content = content.replace('%OP','(').replace('%CP',')')
		#log('USER function\n~~~',content,'\n~~~')
		self.funs[name] = content
		self.funs_args[name] = args
		
	def defined(self,name):
		return name in self.funs

	def fun(self,name,args,line):
		done = self.funs[name]

		for x in range(len(self.funs_args[name])):
			done = done.replace(self.funs_args[name][x],args[x])

		if 'return' in done:
			for li in done.split('\n'):

				if 'return' in li:
					print('returning from function')
					retval = li[(li.index('return') + len('return')):]
					print('returnvalue:',retval)

					#namedex = line.index(name) + len(name) 
					line = line.replace(name + '(' + ','.join(args) + ')' ,retval,1)
					log('newline:',line)

		return (done,line)

funs = funs()

def join(arr,space=' '):
	return space.join(arr)

def error(etype='Unknown',content='An unknown error occured',linum=-1,path=''):
	sys.exit('\n\n[:ERROR:]\n%sError:\n%s\nline:%s' % (etype,content,linum))

def speacialChars(strr):
	strr = strr.replace('%OP','(').replace('%CP',')').replace('%WS','')
	return strr

def wordj(arr):
	return ' '.join(arr)

def EXEC(path,MODE='MAIN',funs=funs,varz=varz,itera=0):

	def log(*args):
		print('\t' * itera + ' '.join(args))

	class bytec:
		"""creates bytecode"""
		def __init__(self,path='',content=''):
			self.path = path

		_bytecode = ''

		def add(self,*txts):
			self._bytecode += '\n'
			for i in txts:
				if type(i) != str:
					i = str(i)
				self._bytecode += i + ' '

		def finish(self):
			directory = os.path.dirname(self.path) + '/ExpandScript_Output_/'
			if not os.path.exists(directory):
				os.mkdir(directory)

			file = open(directory + os.path.split(self.path)[1].split('.')[0] + '.exs_bytes','w')
			file.write(str(self._bytecode))
			file.close()

		def get(self):
			return self._bytecode

		def FUN(self,name,args,line):
			log('functioning')
			code = funs.fun(name,args,line)
			log('USER functio1n\n~~~',funs.fun(name,args,line)[0],'\n','~~~')
			self._bytecode += EXEC(code[0],'FUNCTION',funs,varz,itera + 1)
			return code[1]

		def finish_as_home(self):
			direct = (os.path.expanduser('$') + '/ExpandScript_Output_/').replace('\\','/')
			if not os.path.exists(direct):
				os.mkdir(direct)


			with open(direct + self.path.replace('\\','/').split('/')[-1],'w') as file:
				file.write(str(self._bytecode))

		def byte(self):
			self._bytecode = bytes(self._bytecode,'utf8')

	# var types:
	VAR_TYPES = [
	'int',
	'str',
	'bool',
	'arr',
	'obj',
	'void',
	'fun'
	]

	#lines to skip in a block:
	skipLines = -1
	byte = bytec(path)

	lines = getLines(path,MODE)

	linum = 0 # line number
	


	def hasChar(arr, word):
		for i in arr:
			for x in word:
				if i == x:
					return True
		return False

	inComment = False
	
	for line in lines:
		linum += 1
		
		log('reading line %s: %s' % (linum,line))
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


		if skipLines > -1:
			skipLines -= 1
			continue


		if hasChar(line,'^'):
			log('skipping comment')
			line = line.split('^')[0].strip()

		words = line.split(' ')

		for i in range(len(words)):

			words[i] = words[i].strip()

		for i in varz:
			line = line.replace('$' + i,varz[i])

		if hasChar(line,'(') and hasChar(line,')'):
			# if line is a function
			_name = line.split('(')[0].strip().split()[-1]
			_args = line.split('(')[1].split(')')[len(line.split('(')[1].split(')')) - 2].split(',')
			log('function name:',_name)

			log('stripping args')
			for i in range(len(_args)):
				_args[i] = _args[i].strip()

			log('args stripped')

			line = line.replace(', ',',')
			if funs.defined(_name):
				line = byte.FUN(_name,_args,line)
				words = line.split()
				print('line returned from function:',line)

			elif _name == 'rawjs':
				log('adding raw js')
				byte.add('js',line.split('(\'')[1].split('\')')[len(line.split('(\'')[1].split('\')')) - 2])

			elif _name == 'rawhtml':
				log('adding raw html to body')
				byte.add('html',line.split('(\'')[1].split('\')')[len(line.split('(\'')[1].split('\')')) - 2])

			elif _name == 'rawcss':
				log('adding raw css')
				byte.add('css',line.split('(\'')[1].split('\')')[len(line.split('(\'')[1].split('\')')) - 2])

			elif _name == 'log':
				log('adding console statement')
				byte.add('log',join(_args))


			else:
				error('Define','An item on this line is not defined in file: %s, in word: %s' % (path, _name), linum)
				
		
		if words[0] in VAR_TYPES:
			log('Getting variable')
			_type = words[0]
			_val = 'undefined'
			if not '$' in words[1]:
				error('Name','Invalid variable name',linum)
				
			_name = words[1].split('$')[1]
			if not _type in VAR_TYPES:
				error('Type','Not a valid variable type',linum,time)
			elif words[2] != '=':
				error('Syntax','Invalid syntax.',linum)

			elif _type == 'int':
				log('type is int')
				try:
					_val = words[3]

				except ValueError:
					error('Type','Not of type: int',linum,time)

			elif _type == "str":
				log('type str')
				if hasChar(line,"'"):
					word = words[3]
					strStart = word.index("'")
					_val = ' '.join(words[(words.index(word) + strStart):])

				else:
					error('String','Invalid str.',linum)

			elif _type == 'bool':
				bool_types = ['true', 'false']
				if not words[3] in bool_types:
					error('Bool','invalid bool',linum)

			log('setting variable')
			log('variable data:','ANONY')
			varz[_name] = _val

		
		elif hasChar(line,'$') and line[0] == '$' and '[' in line and ']' in line:
			log('Creating function')
			i = linum 
			_name = line.split('[')[0][1:]
			_args = line.split('[')[1].split(']')[0].split(',')

			for x in _args:
				if len(x) > 0:
					if x[0] != '$':
						error('Syntax','Invalid variable',linum)

			content = []
			skipLines = 0
			while True:
				if err(lines[i]):
					i += 1
					continue

				if lines[i][0] == '}':
					skipLines = i - linum
					break

				content.append(lines[i])
				i += 1

			fin = ''
			for x in content:
				fin = fin + '\n' + x

			linum = i + 1

			funs.add(_name,fin,_args)
			log('function created')

		if words[0] == '#inc':
			log('importing')
			try:
				if len(words) > 2:
					if not words[2] == 'from':
						error('Syntax','Invalid syntax.',linum,time)
					else:
						_path = words[3] + line.split('<')[1].split('>')[0] + '.expd'

				else:
					_path = './Lib/' + line.split('<')[1].split('>')[0] + '.expd'

				byte.add(EXEC(_path,'MODULE',funs,varz,itera + 1))

			except IndexError as e:
				raise e
				error('Syntax','Invalid syntax.l',linum,time)

	if MODE == 'MAIN':
		#byte.byte()

		byte.finish() # finish_as_home for non-dev purposes

		compileHTML(byte.get(),path)
	elif MODE == 'MODULE' or MODE == 'FUNCTION':
		print('returned script')
		return byte.get()

	else:
		error('Compile','Unable to compile at this time.')

	return 0


def err(line):
	if line == '' or line == '\n':
		return True
	
	return False

def strip(line):
	fin = line.strip()
	fin = fin.replace('${VERSION}$',VERSION)
	return fin

def replaceSP(line):
	return line.replace('${TABS}$','\t\t')

def wordsLen(words,num):
	if len(words) < num:
		error('Argument','Insufficint arguments',-1)

def compileHTML(code,path):

	#code = bytes.decode(code,'utf8')

	class compiled:
		"""this class is for making """
		def __init__(self):
			html = open('./html_compile/start_html.txt','r')
			self.html = html.read()
			html.close()

		js = """"""

		css = """"""

		htmlPlus = """"""

		def addHtml(self,*html):
			html = replaceSP(' '.join(html))
			self.htmlPlus += '\n\t' + html

		def addJs(self,*js):
			js = replaceSP(' '.join(js))
			self.js += '\n\t\t' + js
		
		def addCss(self,*css):
			css = replaceSP(' '.join(css))
			self.css += '\n\t\t' + css

		def bind(self):
			binded = self.html.replace('${HTML}$',self.htmlPlus).replace('${JS}$',self.js,1).replace('${CSS}$',self.css,1).replace('${VERSION}$',VERSION,1)
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
			wordsLen(words,2)
			html.addJs('console.log(' + ', '.join(words[1:]) + ');')

		elif words[0] == 'js':
			wordsLen(words,2)
			html.addJs(join(words[1:]))

		elif words[0] == 'html':
			wordsLen(words,2)
			html.addHtml(join(words[1:]))

		elif words[0] == 'css':
			wordsLen(words,2)
			html.addCss(join(words[1:]))


	with open(os.path.dirname(path) + '/ExpandScript_Output_/' + os.path.basename(path) + '.html','w') as output:
		output.write(html.bind())
		log('Succesfully compiled',path.replace('\\','/'))


VERSION = '1.0.5.0'

"""
name (current release {b:beta,a:alpha}) planned release version
Features to be added:
	return (b2) 1.1.0.0
	do-loop () 1.3.0.0
	for-loop () 1.3.0.0
	while-loop () 1.3.0.0
	if statement () 1.3.0.0
	else statement () 1.3.0.0

bug (status {0:active,1:in progress}) (planned release fix OP)
bugs:
	functions inside calling function as argument (0)
	the error system outputs incorrect line number (1)	
"""


#EXEC( os.path.dirname(os.path.realpath(__file__)) + '/game1.expd')

#EXEC canvas module
print(EXEC('./lib/canvas.expd','MODULE'))