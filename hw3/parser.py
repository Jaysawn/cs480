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
keywords.update({'and':'bool operator'})
keywords.update({'or':'bool operator'})
keywords.update({'not':'bool operator'})
keywords.update(sin='trig function')
keywords.update(cos='trig function')
keywords.update(tan='trig function')
keywords.update(bool='primitive type')
keywords.update(int='primitive type')
keywords.update(real='primitive type')
keywords.update(string='primitive type')
keywords.update(let='statement keyword')
keywords.update({'if':'statement keyword'})
keywords.update({'while':'statement keyword'})
keywords.update(stdout='statement keyword')

class Token:
	def __init__(self, token_type, token_value):
		self.token_type = token_type
		self.token_value = token_value

input = 0

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
					sys.exit(0)

			else:
				cur_token = cur_char

			return_token.token_type = 'Integer Operator'
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
					return_token.token_type = 'Statement Character'
					return_token.token_value = cur_token
					return return_token

				else:
					input.seek(-1, 1)
					print "Invalid Character: " + cur_char
					sys.exit(0)

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
						return_token.token_type = 'String'
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
						return_token.token_type = 'String'
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
						return_token.token_type = 'Identifier'
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

	while True:
		parse_token = lex()

		if (parse_token.token_type == 'none'):
			#No more tokens
			print "No more tokens"
			break

		else:

			print parse_token.token_type
			print parse_token.token_value
			#if (
			if (parse_token.token_value == '('):
				print "Calling S'"

			#else if const/names
			elif (parse_token.token_type == 'String') or (parse_token.token_type == 'bool') or (parse_token.token_type == 'Identifier'):
				print "Calling O'"

			#else error and break
			else:
				print "Invalid Token - Type: " + str(parse_token.token_type) + "; Value: " + str(parse_token.token_value)

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
            sys.exit()
        elif o in ("-s"):
        	global input
        	input = open(a, 'r+')
        	parse()
        	input.close()

        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()