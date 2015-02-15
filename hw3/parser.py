#Jason Cross
#Winter 2015
#CS 480
#Milestone 3

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

class Token:
	def __init__(self, token_type, token_value):
		self.token_type = token_type
		self.token_value = token_value

input = 0
parse_token = 0
read_flag = 0

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
							return_token.token_type = 'Float'
							return_token.token_value = cur_token
							return return_token	
				
				elif ((cur_ascii == 69) or (cur_ascii == 101)):
					#add on e
					cur_token = cur_token + cur_char

					cur_char = input.read(1)
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
							return_token.token_type = 'Float'
							return_token.token_value = cur_token
							return return_token	


				#we found something else, so token just the int
				else:
					if (cur_token[0] == '.'):
						#a decimal w/o a proceding value (b/t 0 and 1)
						input.seek(-1, 1)
						return_token.token_type = 'Float'
						return_token.token_value = cur_token
						return return_token
					else:
						#an integer
						input.seek(-1, 1)
						return_token.token_type = 'Integer'
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
						return_token.token_type = 'strings'
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
						return_token.token_type = 'strings'
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
	#valid characters for function names, variables names, and other keywords include:
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
				print parse_token.token_value
				parse1()

			#const/names
			elif (parse_token.token_type == 'strings') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'Integer') or (parse_token.token_type == 'Float'):
				read_flag = 0
				print parse_token.token_value
				parse2()

			#else error and break
			else:
				print "Invalid0 Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
				sys.exit(0)

def parse1():

	global parse_token
	global read_flag

	if read_flag == 0:
		parse_token = lex()

	if (parse_token.token_type == 'none'):
		#No more tokens when we expected more
		print "No more tokens; Production Unfinished"
		sys.exit(0)

	else:

		#next token is )
		if (parse_token.token_value == ')'):
			read_flag = 0
			print parse_token.token_value + "hmmm"
			parse2()

		#next token is (
		elif (parse_token.token_value == '('):
			read_flag = 0
			print parse_token.token_value
			parse1()
			match(')')
			parse2()

		#const/names
		elif (parse_token.token_type == 'strings') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'Integer') or (parse_token.token_type == 'Float'):
			read_flag = 0
			print parse_token.token_value
			parse2()
			match(')')
			parse2()

		#match the proper statement
		elif (parse_token.token_type == 'stmts'):
			read_flag = 0
			#statement match code or function call
			match(')')
			
			parse2()

		#match the proper operator
		elif (parse_token.token_type == 'oper') or (parse_token.token_type == 'unops') or (parse_token.token_type == 'binops'):
			read_flag = 0
			match_oper()
			match(')')
			parse2()

		#else error and break
		else:
			print "Invalid1 Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
			sys.exit(0)

def parse2():

	global parse_token
	global read_flag

	if read_flag == 0:
		parse_token = lex()

	if (parse_token.token_type == 'none'):
		return

	elif (parse_token.token_value == '('):
		read_flag = 0
		print parse_token.token_value
		parse1()
		parse2()

	elif (parse_token.token_type == 'strings') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'Integer') or (parse_token.token_type == 'Float'):
		read_flag = 0
		print parse_token.token_value
		parse2()
		parse2()

	#else fall through
	else:
		#print "INVALID Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		#sys.exit(0)
		read_flag = 1
		return

def match(terminal):
	global parse_token
	global read_flag

	if read_flag == 0:
		parse_token = lex()

	if (parse_token.token_value == terminal):
		read_flag = 0
		print parse_token.token_value
		return

	else:
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

def match_oper():
	global parse_token

	if (parse_token.token_type == 'binops'):
		#match oper and oper
		print parse_token.token_value
		match_nested_oper()
		match_nested_oper()

	elif (parse_token.token_type == 'unops'):
		#match oper
		print parse_token.token_value
		match_nested_oper()

	elif (parse_token.token_type == 'oper'):
		#is a :=
		#match name oper
		print parse_token.token_value
		match_type('name')
		match_nested_oper()

	else:
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)		

def match_nested_oper():
	parse_token = lex()

	if (parse_token.token_type == 'strings') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'name') or (parse_token.token_type == 'Integer') or (parse_token.token_type == 'Float'):
		#found a valid oper, return
		print parse_token.token_value
		return

	#the rest must start with ( and end with a )
	if (parse_token.token_value != '('):
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	print parse_token.token_value

	parse_token = lex()

	if (parse_token.token_type == 'binops'):
		print parse_token.token_value
		match_nested_oper()
		match_nested_oper()

	elif (parse_token.token_type == 'unops'):
		print parse_token.token_value
		match_nested_oper()

	elif (parse_token.token_type == 'oper'):
		print parse_token.token_value
		match_type('name')
		match_nested_oper()

	else:
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	#end if a )
	parse_token = lex()

	if (parse_token.token_value != ')'):
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

	print parse_token.token_value


def match_type(terminal):
	parse_token = lex()

	if (parse_token.token_type == terminal):
		#good, just fall through
		print parse_token.token_value
		return

	else:
		print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)
		sys.exit(0)

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

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif o in ("-s"):
        	global input
        	input = open(a, 'r+')
        	parse()
        	input.close()

        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()