#Jason Cross
#Winter 2015
#CS 480
#Milestone 5

import sys
import getopt
import math

intops = [60,61,62,33,37,42,43,45,47,44,94]
intops2 = [60,62]
miscstates = [40,41,58]

keywords = dict()

keywords.update(true='bool')
keywords.update(false='bool')
keywords.update({'and':'binops'})
keywords.update({'or':'binops'})
keywords.update({'not':'unops'})
keywords.update(sin='unops')
keywords.update(cos='unops')
keywords.update(tan='unops')
keywords.update(bool='type')
keywords.update(int='type')
keywords.update(real='type')
keywords.update(string='type')
keywords.update(let='stmts')
keywords.update({'if':'stmts'})
keywords.update({'while':'stmts'})
keywords.update(stdout='stmts')

variables = dict()

class Token:
	def __init__(self, token_type, token_value):
		self.token_type = token_type
		self.token_value = token_value

input = 0
output = 0
parse_token = 0
read_flag = 0
depth = 0

def lex():

	return_token = Token('none', 'none')

	while True:
		cur_token = ''
		peek = ''

		cur_char = input.read(1)

		if not cur_char:
			#EOF
			#print "End of file"
			return_token.token_type = 'none'
			return return_token

		#lex code
		if (' ' == cur_char) or ('\t' == cur_char) or ('\r' == cur_char) or ('\n' == cur_char):
			continue

		cur_ascii = ord(cur_char)

		#if integer operator
		if (cur_ascii in intops):
			if (cur_ascii in intops2):
				peek = input.read(1)
				#is a < or > followed by =
				if (ord(peek) == 61):
					cur_token = cur_char + peek
				#is just a plain int operator
				else:
					cur_token = cur_char
					input.seek(-1, 1)
			
			elif (cur_ascii == 33):
				#! must be followed by =, if not we error
				peek = input.read(1)
				if (ord(peek) == 61):
					cur_token = cur_char + peek
				else:
					input.seek(-1, 1)
					print "Invalid Character: " + cur_char
					sys.exit(1)

			else:
				cur_token = cur_char

			return_token.token_type = 'binops'
			return_token.token_value = cur_token
			return return_token

		#if number: int or real/float
		elif (cur_char.isdigit() or cur_ascii == 46):
			cur_token = cur_char

			while True:
				cur_char = input.read(1)
				if not cur_char:
					return_token.token_type = 'int'
					return_token.token_value = cur_token
					return return_token

				cur_ascii = ord(cur_char)

				if cur_char.isdigit():
					cur_token = cur_token + cur_char
					continue

				#floating point
				elif (cur_ascii == 46):
					#add on decimal
					cur_token = cur_token + cur_char

					while True:
						cur_char = input.read(1)
						if not cur_char:
							return_token.token_type = 'real'
							return_token.token_value = cur_token
							return return_token	

						#digits after decimal
						if cur_char.isdigit():
							cur_token = cur_token + cur_char
							continue

						elif ((cur_ascii == 69) or (cur_ascii == 101)):
							#add on e
							cur_token = cur_token + cur_char

							cur_char = input.read(1)
							cur_ascii = ord(cur_char)

							if ((cur_ascii == 43) or (cur_ascii == 45)):
								#add on + or -
								cur_token = cur_token + cur_char
								continue

						#as soon as we find a non digit after a decimal, we stop
						else:
							input.seek(-1, 1)
							return_token.token_type = 'real'
							return_token.token_value = cur_token
							return return_token	
				
				elif ((cur_ascii == 69) or (cur_ascii == 101)):
					#add on e
					cur_token = cur_token + cur_char

					cur_char = input.read(1)
					if not cur_char:
						return_token.token_type = 'real'
						return_token.token_value = cur_token
						return return_token	
					
					cur_ascii = ord(cur_char)

					if ((cur_ascii == 43) or (cur_ascii == 45)):
						#add on + or -
						cur_token = cur_token + cur_char

					while True:
						cur_char = input.read(1)

						#digits after e
						if cur_char.isdigit():
							cur_token = cur_token + cur_char
							continue

						#as soon as we find a non digit after an e, we stop
						else:
							input.seek(-1, 1)
							return_token.token_type = 'real'
							return_token.token_value = cur_token
							return return_token	


				#we found something else, so token just the int
				else:
					if (cur_token[0] == '.'):
						#a decimal w/o a proceding value (b/t 0 and 1)
						input.seek(-1, 1)
						return_token.token_type = 'real'
						return_token.token_value = cur_token
						return return_token
					else:
						#an integer
						input.seek(-1, 1)
						return_token.token_type = 'int'
						return_token.token_value = cur_token
						return return_token

		#misc statement characters
		elif (cur_ascii in miscstates):
			#left paren
			if (cur_ascii == 40):
				cur_token = cur_char
				return_token.token_type = 'Statement Character'
				return_token.token_value = cur_token
				return return_token

			#right paren
			if (cur_ascii == 41):
				cur_token = cur_char
				return_token.token_type = 'Statement Character'
				return_token.token_value = cur_token
				return return_token

			#assign op :=
			if (cur_ascii == 58):
				peek = input.read(1)
				#found :=
				if (ord(peek) == 61):
					cur_token = cur_char + peek
					return_token.token_type = 'oper'
					return_token.token_value = cur_token
					return return_token

				else:
					input.seek(-1, 1)
					print "Invalid Character: " + cur_char
					sys.exit(1)

		#string literals
		elif (cur_ascii == 34) or (cur_ascii == 39):
			cur_token = cur_char

			#double quote, read till another
			if (cur_ascii == 34):

				while True:
					cur_char = input.read(1)
					#found the matching double quote
					if (ord(cur_char) == 34):
						cur_token = cur_token + cur_char
						return_token.token_type = 'string'
						return_token.token_value = cur_token
						return return_token

					#add to the string
					else:
						cur_token = cur_token + cur_char

			#single quote, read till another
			if (cur_ascii == 39):

				while True:
					cur_char = input.read(1)
					#found the matching single quote
					if (ord(cur_char) == 39):
						cur_token = cur_token + cur_char
						return_token.token_type = 'string'
						return_token.token_value = cur_token
						return return_token

					#add to the string
					else:
						cur_token = cur_token + cur_char

		#first char is a character, look for keywords or identifiers
		elif (cur_ascii >= 65) and (cur_ascii <= 90) or (cur_ascii >= 97) and (cur_ascii <= 122):

			cur_token = cur_char

			while True:
				cur_char = input.read(1)

				#next character is valid
				if (isvalidchar(cur_char)):
					cur_token = cur_token + cur_char

				#we hit something that isn't a valid character
				else:
					#lseek back
					input.seek(-1,1)

					#now we need to find out if our current token is:
					#a keywords
					if cur_token in keywords:
						return_token.token_type = keywords[cur_token]
						return_token.token_value = cur_token
						return return_token

					#some identifier
					else:
						return_token.token_type = 'name'
						return_token.token_value = cur_token
						return return_token

		else:
			print "Invalid Character: " + cur_char
			sys.exit(0)

def print_token(token_type, token_value):
	token_len = len(token_value)
	print "Token Type: " + token_type + "; Token Value: " + token_value + "; Token Length: " + str(token_len)

def isvalidchar(test_char):
	#valid characters for function names, variable names, and other keywords include:
	#characters ex: a-z & A-Z
	#underscores ex: _
	#numbers ex: 0-9

	test_ascii = ord(test_char)

	if (test_char.isdigit()):
		return True

	elif (test_char == ' '):
		return False

	elif (test_ascii >= 65) and (test_ascii <= 90) or (test_ascii >= 97) and (test_ascii <= 122):
		return True

	elif (test_ascii == 95):
		return True

	else:
		return False

def parse():
	global parse_token
	global read_flag

	while True:
		if read_flag == 0:
			parse_token = lex()

		if (parse_token.token_type == 'none'):
			#No more tokens
			print "No more tokens; Productions complete."
			break

		else:
			
			#if (
			if (parse_token.token_value == '('):
				read_flag = 0
				#print parse_token.token_value
				print_node()
				parse1()

			#const/names
			elif (parse_token.token_type == 'string') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'int') or (parse_token.token_type == 'real'):
				read_flag = 0
				#print parse_token.token_value
				print_node()
				parse2()

			#else error and break
			else:
				print "Invalid Token5 - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
				sys.exit(0)

def parse1():

	global parse_token
	global read_flag
	global depth

	if read_flag == 0:
		parse_token = lex()

	if (parse_token.token_type == 'none'):
		#No more tokens when we expected more
		print "No more tokens; Production Unfinished"
		sys.exit(0)

	else:

		#depth += 1

		#next token is )
		if (parse_token.token_value == ')'):
			read_flag = 0
			#print parse_token.token_value
			#depth -= 1
			print_node()
			parse2()

		#next token is (
		elif (parse_token.token_value == '('):
			read_flag = 0
			#print parse_token.token_value
			depth += 1
			print_node()
			#depth += 1
			parse1()
			depth -= 1
			match(')')
			parse2()

		#const/names
		elif (parse_token.token_type == 'string') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'int') or (parse_token.token_type == 'real'):
			read_flag = 0
			#print parse_token.token_value
			depth += 1
			print_node()
			parse2()
			depth -= 1
			match(')')
			parse2()

		#match the proper statement
		elif (parse_token.token_type == 'stmts'):
			read_flag = 0
			match_stmts()
			#match(')')
			parse2()

		#match the proper operator
		elif (parse_token.token_type == 'oper') or (parse_token.token_type == 'unops') or (parse_token.token_type == 'binops'):
			read_flag = 0
			match_oper()
			#depth -= 1
			match(')')
			parse2()

		#else error and break
		else:
			print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
			sys.exit(0)

		#depth -= 1

def parse2():

	global parse_token
	global read_flag
	global depth

	if read_flag == 0:
		parse_token = lex()

	#depth += 1

	if (parse_token.token_type == 'none'):
		return

	elif (parse_token.token_value == '('):
		read_flag = 0
		#print parse_token.token_value
		#depth += 1
		print_node()
		parse1()
		parse2()

	elif (parse_token.token_type == 'string') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'int') or (parse_token.token_type == 'real'):
		read_flag = 0
		#print parse_token.token_value
		#depth += 1
		print_node()
		#depth -= 1
		parse2()
		parse2()

	#else fall through
	else:
		read_flag = 1
		#depth -= 1
		return

	#depth -= 1

def match(terminal):
	global parse_token
	global read_flag

	if read_flag == 0:
		parse_token = lex()

	if (parse_token.token_value == terminal):
		read_flag = 0
		#print parse_token.token_value
		print_node()
		return

	else:
		print "Expected Terminal: " + str(terminal)
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

def match_oper():
	global parse_token
	global read_flag
	global depth
	global output

	typea = 0
	typeb = 0

	temp_token = 0

	depth += 1

	if (parse_token.token_type == 'binops'):
		#match oper and oper
		#print parse_token.token_value
		print_node()

		temp_token = parse_token

		if (parse_token.token_value == '-'):
			typea = match_nested_oper()

			parse_token = lex()
			if (parse_token.token_value == ')'):
				if (typea == 'real'):
					output.write('fnegate')
				else:
					output.write('negate')
				read_flag = 1

			else:
				read_flag = 1
				typeb = match_nested_oper()

		else:
			typea = match_nested_oper()
			typeb = match_nested_oper()

		#print typea
		#print typeb

		if (typea == 'real') and (typeb == 'real'):
			if (temp_token.token_value == '!='):
				output.write('<> ')
			elif (temp_token.token_value == '%'):
				output.write('fmod ')
			elif (temp_token.token_value == '^'):
				output.write('f** ')
			else:
				output.write('f' + temp_token.token_value + ' ')

		elif (typea == 'int') and (typeb == 'int'):
			if (temp_token.token_value == '!='):
				output.write('<> ')
			elif (temp_token.token_value == '%'):
				output.write('mod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f s>f fswap f** f>s ')
			else:
				output.write(temp_token.token_value + ' ')

		elif (typea == 'string') and (typeb == 'string'):
			if (temp_token.token_value == '+'):
				output.write('s+ ')
			else:
				print "Invalid string operation"
				sys.exit(0)
		#we have a float and something else or bad code
		#no fswap needed
		elif (typea == 'real') and (typeb == "int"):
			if (temp_token.token_value == '!='):
				output.write('s>f <> ')
			elif (temp_token.token_value == '%'):
				output.write('s>f fmod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f f** ')
			else:
				output.write('s>f f' + temp_token.token_value + ' ')
		#fswap needed
		else:
			if (temp_token.token_value == '!='):
				output.write('s>f fswap <> ')
			elif (temp_token.token_value == '%'):
				output.write('s>f fswap fmod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f fswap f** ')
			else:
				output.write('s>f fswap f' + temp_token.token_value + ' ')


	elif (parse_token.token_type == 'unops'):
		#match oper
		#print parse_token.token_value
		temp_token = parse_token
		print_node()
		typea = match_nested_oper()

		if (temp_token.token_value == 'not'):
			output.write('invert ')
		#sin cos or tan
		else:
			if (typea == 'real'):
				output.write('f' + temp_token.token_value + ' ')
			else:
				output.write(temp_token.token_value + ' ')


	elif (parse_token.token_type == 'oper'):
		#is a :=
		#match name oper
		#print parse_token.token_value
		print_node()
		variable_name = match_type('name')
		if variable_name not in variables:
			print "Variable: " + variable_name + " used before declared"
			sys.exit(0)
		match_nested_oper()
		output.write(variable_name + ' ! ')

	else:
		print "Expected Oper"
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	depth -= 1	

def match_nested_oper():
	global parse_token
	global read_flag
	global depth
	global output

	#print "read Flag: " + str(read_flag)
	#print "parse token: " + str(parse_token.token_value)
	if (read_flag == 0):
		parse_token = lex()

	read_flag = 0

	#depth += 1

	if (parse_token.token_type == 'string') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'int') or (parse_token.token_type == 'real'):
		#found a valid oper, return
		#print parse_token.token_value
		print_node()
		if (parse_token.token_type == 'string'):
			parse_token.token_value = parse_token.token_value[1:-1]
			output.write('s" ' + parse_token.token_value + '" ')
		else:
			output.write(parse_token.token_value + ' ')
		#depth -= 1
		if (parse_token.token_type == 'name'):
			#return the variable's type
			if parse_token.token_value not in variables:
				print "Variable: " + parse_token.token_value + " used before declared"
				sys.exit(0)
			else:
				return variables[parse_token.token_value]
		else:
			#return the token's type, as it isn't a variable and the type is stored in the token
			return parse_token.token_type

	#depth += 1

	#the rest must start with ( and end with a )
	if (parse_token.token_value != '('):
		print "Expected ("
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	#print parse_token.token_value
	print_node()

	depth += 1

	parse_token = lex()

	return_type = 0
	typea = 0
	typeb = 0
	temp_token = parse_token

	if (parse_token.token_type == 'binops'):
		#match oper and oper
		#print parse_token.token_value
		print_node()

		if (parse_token.token_value == '-'):
			typea = match_nested_oper()

			parse_token = lex()
			if (parse_token.token_value == ')'):
				if (typea == 'real'):
					output.write('fnegate')
				else:
					output.write('negate')
				read_flag = 1

			else:
				read_flag = 1
				typeb = match_nested_oper()

		else:
			typea = match_nested_oper()
			typeb = match_nested_oper()

		if (typea == 'real') and (typeb == 'real'):
			return_type = 'real'
			if (temp_token.token_value == '!='):
				output.write('<> ')
			elif (temp_token.token_value == '%'):
				output.write('fmod ')
			elif (temp_token.token_value == '^'):
				output.write('f** ')
			else:
				output.write('f' + temp_token.token_value + ' ')

		elif (typea == 'int') and (typeb == 'int'):
			return_type = 'int'
			if (temp_token.token_value == '!='):
				output.write('<> ')
			elif (temp_token.token_value == '%'):
				output.write('mod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f s>f fswap f** f>s ')
			else:
				output.write(temp_token.token_value + ' ')

		elif (typea == 'string') and (typeb == 'string'):
			return_type = 'string'
			if (temp_token.token_value == '+'):
				output.write('s+ ')
			else:
				print "Invalid string operation"
				sys.exit(0)
		#we have a float and something else or bad code
		#no fswap needed
		elif (typea == 'real') and (typeb == "int"):
			if (temp_token.token_value == '!='):
				output.write('s>f <> ')
			elif (temp_token.token_value == '%'):
				output.write('s>f fmod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f f** ')
			else:
				output.write('s>f f' + temp_token.token_value + ' ')
		else:
			return_type = 'real'
			if (temp_token.token_value == '!='):
				output.write('s>f fswap <> ')
			elif (temp_token.token_value == '%'):
				output.write('s>f fswap fmod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f fswap f** ')
			else:
				output.write('s>f fswap f' + temp_token.token_value + ' ')

	elif (parse_token.token_type == 'unops'):
		#print parse_token.token_value
		print_node()
		typea = match_nested_oper()

		if (temp_token.token_value == 'not'):
			output.write('invert ')
		#sin cos or tan
		else:
			if (typea == 'real'):
				output.write('f' + temp_token.token_value + ' ')
				return_type = 'real'
			else:
				output.write(temp_token.token_value + ' ')
				return_type = 'int'

	elif (parse_token.token_type == 'oper'):
		#print parse_token.token_value
		print_node()
		variable_name = match_type('name')
		if variable_name not in variables:
			print "Variable: " + variable_name + " used before declared"
		match_nested_oper()
		output.write(variable_name + ' ! ')

	else:
		print "Expected Nested Oper"
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	depth -= 1

	#end if a )
	if (read_flag == 0):
		parse_token = lex()

	read_flag = 0

	if (parse_token.token_value != ')'):
		print "Expected ) to finish an oper"
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	#print parse_token.token_value
	print_node()
	return return_type

def match_stmts():
	global parse_token
	global read_flag
	global depth
	global output

	typea = 0
	typeb = 0
	typec = 0

	depth += 1

	if (parse_token.token_value == 'stdout'):
		#print parse_token.token_value
		print_node()
		typea = match_nested_oper()
		if (typea == 'string'):
			output.write('type ')
		elif (typea == 'real'):
			output.write('f. ')
		else:
			output.write('. ')
		depth -= 1
		match(')')

	elif (parse_token.token_value == 'let'):
		#print parse_token.token_value
		print_node()
		match('(')
		depth += 1
		match_varlist()
		depth -= 1
		#let stmt ends with 2 )'s, but the first of the 2 will get matched in match_varlist
		#if (read_flag == 0):
		#	match(')')
		match(')')

	elif (parse_token.token_value == 'if'):
		#print parse_token.token_value
		print_node()
		typea = match_expr()
		output.write('if ')
		typeb = match_expr()

		parse_token = lex()

		if (parse_token.token_value == ')'):
			#print parse_token.token_value
			depth -= 1
			print_node()
			output.write('then ')
			return

		else:
			output.write('else ')
			read_flag = 1
			typec = match_expr()
			read_flag = 0
			depth -= 1
			match(')')
			output.write('then ')


	elif (parse_token.token_value == 'while'):
		#print parse_token.token_value
		print_node()
		output.write('begin ')
		match_expr()
		output.write('while ')
		match_expr()
		while True:
			parse_token = lex()

			if (parse_token.token_value == ')'):
				#print parse_token.token_value
				depth -= 1
				print_node()
				break

			else:
				#print_node()
				read_flag = 1
				match_expr()

		output.write('repeat ')

	else:
		print "Expected stmt"
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)	

def match_expr():
	global parse_token
	global read_flag
	global depth
	global output

	typea = 0

	if (read_flag == 0):
		parse_token = lex()

	read_flag = 0

	if (parse_token.token_type == 'string') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'int') or (parse_token.token_type == 'real'):
		#found a valid oper, return
		#print parse_token.token_value
		print_node()
		if (parse_token.token_type == 'string'):
			parse_token.token_value = parse_token.token_value[1:-1]
			output.write('s" ' + parse_token.token_value + '" ')
		else:
			output.write(parse_token.token_value + ' ')
		#depth -= 1
		if (parse_token.token_type == 'name'):
			#return the variable's type
			if parse_token.token_value not in variables:
				print "Variable: " + parse_token.token_value + " used before declared"
				sys.exit(0)
			else:
				return variables[parse_token.token_value]
		else:
			#return the token's type, as it isn't a variable and the type is stored in the token
			return parse_token.token_type

	#the rest must start with ( and end with a )
	if (parse_token.token_value != '('):
		print "Invalid Token2 - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	#print parse_token.token_value
	print_node()

	depth += 1

	parse_token = lex()

	return_type = 0
	typea = 0
	typeb = 0
	typec = 0
	temp_token = parse_token

	if (parse_token.token_type == 'binops'):
		#match oper and oper
		#print parse_token.token_value
		print_node()

		if (parse_token.token_value == '-'):
			typea = match_nested_oper()

			parse_token = lex()
			if (parse_token.token_value == ')'):
				if (typea == 'real'):
					output.write('fnegate')
				else:
					output.write('negate')
				read_flag = 1

			else:
				read_flag = 1
				typeb = match_nested_oper()

		else:
			typea = match_nested_oper()
			typeb = match_nested_oper()

		if (typea == 'real') and (typeb == 'real'):
			return_type = 'real'
			if (temp_token.token_value == '!='):
				output.write('<> ')
			elif (temp_token.token_value == '%'):
				output.write('fmod ')
			elif (temp_token.token_value == '^'):
				output.write('f** ')
			else:
				output.write('f' + temp_token.token_value + ' ')

		elif (typea == 'int') and (typeb == 'int'):
			return_type = 'int'
			if (temp_token.token_value == '!='):
				output.write('<> ')
			elif (temp_token.token_value == '%'):
				output.write('mod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f s>f fswap f** f>s ')
			else:
				output.write(temp_token.token_value + ' ')

		elif (typea == 'string') and (typeb == 'string'):
			return_type = 'string'
			if (temp_token.token_value == '+'):
				output.write('s+ ')
			else:
				print "Invalid string operation"
				sys.exit(0)
		#we have a float and something else or bad code
		#no fswap needed
		elif (typea == 'real') and (typeb == "int"):
			if (temp_token.token_value == '!='):
				output.write('s>f <> ')
			elif (temp_token.token_value == '%'):
				output.write('s>f fmod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f f** ')
			else:
				output.write('s>f f' + temp_token.token_value + ' ')
		else:
			return_type = 'real'
			if (temp_token.token_value == '!='):
				output.write('s>f fswap <> ')
			elif (temp_token.token_value == '%'):
				output.write('s>f fswap fmod ')
			elif (temp_token.token_value == '^'):
				output.write('s>f fswap f** ')
			else:
				output.write('s>f fswap f' + temp_token.token_value + ' ')

	elif (parse_token.token_type == 'unops'):
		#print parse_token.token_value
		print_node()
		typea = match_nested_oper()

		if (temp_token.token_value == 'not'):
			output.write('invert ')
		#sin cos or tan
		else:
			if (typea == 'real'):
				output.write('f' + temp_token.token_value + ' ')
				return_type = 'real'
			else:
				output.write(temp_token.token_value + ' ')
				return_type = 'int'

	elif (parse_token.token_type == 'oper'):
		#print parse_token.token_value
		print_node()
		variable_name = match_type('name')
		if variable_name not in variables:
			print "Variable: " + variable_name + " used before declared"
		match_nested_oper()
		output.write(variable_name + ' ! ')

	#handle stmts w/ parens removed
	elif (parse_token.token_value == 'stdout'):
		#print parse_token.token_value
		print_node()
		typea = match_nested_oper()
		if (typea == 'string'):
			output.write('type ')
		elif (typea == 'real'):
			output.write('f. ')
		else:
			output.write('. ')
		#depth -= 1

	elif (parse_token.token_value == 'let'):
		#print parse_token.token_value
		print_node()
		match('(')
		depth += 1
		match_varlist()
		depth -= 1
		#let stmt ends with 2 )'s, but the first of the 2 will get matched in match_varlist
		#if (read_flag == 0):
		#	match(')')

	elif (parse_token.token_value == 'if'):
		#print parse_token.token_value
		print_node()
		typea = match_expr()
		output.write('if ')
		typeb = match_expr()

		parse_token = lex()

		if (parse_token.token_value == ')'):
			#print parse_token.token_value
			depth -= 1
			print_node()
			output.write('then ')
			return

		else:
			output.write('else ')
			read_flag = 1
			typec = match_expr()
			read_flag = 0
			#depth -= 1
			output.write('then ')


	elif (parse_token.token_value == 'while'):
		#print parse_token.token_value
		print_node()
		output.write('begin ')
		match_expr()
		output.write('while ')
		match_expr()
		while True:
			parse_token = lex()
			#print 'asdf' + parse_token.token_value

			if (parse_token.token_value == ')'):
				#print parse_token.token_value
				depth -= 1
				print_node()
				break

			else:
				#print_node()
				read_flag = 1
				match_expr()

		output.write('repeat ')

	else:
		print "Invalid Token3 - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	depth -= 1

	#end if a )
	parse_token = lex()

	if (parse_token.token_value != ')'):
		print "Invalid Token4 - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	#print parse_token.token_value
	print_node()

def match_varlist():
	global parse_token
	global read_flag
	global depth

	variable_name = 0
	variable_type = 0

	if (read_flag == 0):
		match('(')
	read_flag = 0
	variable_name = match_type('name')
	output.write('variable ' + variable_name + ' ')
	variable_type = match_type('type')
	#print variables.items()
	#if variable already declared, error
	if variable_name in variables:
		print "Error, variable: " + variable_name + " already declared."
		sys.exit(0)
	variables.update({variable_name:variable_type})
	#depth -= 1
	match(')')

	#print variables.items()

	parse_token = lex()

	if (parse_token.token_value == ')'):
		#print parse_token.token_value
		depth -= 1
		print_node()
		return

	elif (parse_token.token_value == '('):
		#print parse_token.token_value
		print_node()
		read_flag = 1
		match_varlist()

	else:
		print "ERROR"

def match_type(terminal):
	global parse_token

	parse_token = lex()

	if (parse_token.token_type == terminal):
		#good, just fall through
		#print parse_token.token_value
		print_node()
		return parse_token.token_value

	else:
		print "Expected terminal of type: " + str(terminal)
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

def print_node():
	print "\t" * depth + str(parse_token.token_value)

def usage():
	print"\n Call python parser.py -s <input_file_name>\n"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:c:", ["help"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(2)

    if len(opts)== 0:
        usage()

    global output
    output = open('gforth.in', 'w')

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif o in ("-s"):
        	global input
        	#global output
        	#output_file = a + 
        	print '====' + str(a) + '===='
        	input = open(a, 'r+')
        	#output = open(a+'.out', 'w')
        	parse()
        	output.write('\n')
        	input.close()
        	#output.close()
        	variables.clear()
        	print '==============='

        else:
            assert False, "unhandled option"

    output.close()

if __name__ == "__main__":
    main()