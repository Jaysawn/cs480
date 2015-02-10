#Jason Cross
#Winter 2015
#CS 480
#Milestone 2

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




def lex(inputfile):
	input = open(inputfile, 'r+')


	while True:
		cur_token = ''
		peek = ''

		cur_char = input.read(1)

		if not cur_char:
			#EOF
			print "End of file"
			break

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
					continue

			else:
				cur_token = cur_char

			print_token('Integer Operator', cur_token)

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

						#as soon as we find a non digit after a decimal, we stop
						else:
							print_token('Float', cur_token)
							input.seek(-1, 1)
							break
					break	
				#we found something else, so token just the int
				else:
					if (cur_token[0] == '.'):
						#a decimal w/o a proceding value (b/t 0 and 1)
						print_token("Float", cur_token)
					else:
						#an integer
						print_token('Integer', cur_token)
					input.seek(-1, 1)
					break

		#misc statement characters
		elif (cur_ascii in miscstates):
			#left paren
			if (cur_ascii == 40):
				cur_token = cur_char
				print_token('Statement Character', cur_token)

			#right paren
			if (cur_ascii == 41):
				cur_token = cur_char
				print_token('Statement Character', cur_token)

			#assign op :=
			if (cur_ascii == 58):
				peek = input.read(1)
				#found :=
				if (ord(peek) == 61):
					cur_token = cur_char + peek
					print_token('Statement Character', cur_token)

				else:
					input.seek(-1, 1)
					print "Invalid Character: " + cur_char

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
						print_token('String', cur_token)
						break

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
						print_token('String', cur_token)
						break

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
						print_token(keywords[cur_token], cur_token)
						break

					#some identifier
					else:
						print_token('Identifier', cur_token)
						break

		else:
			print "Invalid Character: " + cur_char

	input.close()

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

def usage():
	print"\n Call python lex.py -s <input_file_name>\n"

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
        	lex(a)

        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()

#scientific notation
# elif (cur_ascii == 69) or (cur_ascii == 101):
# 	#add on the e/E
# 	cur_token = cur_token + cur_char

# 	#valid chars to follow are + or - followed by digits or just digits(implied +)
# 	cur_char = input.read(1)

# 	#add the +
# 	if (cur_char == 43):
# 		cur_token = cur_token + cur_char

# 	#add the -
# 	else if (cur_char == 45):
# 		cur_token = cur_token + cur_char

# 	#if we get an e/E followed by anything that isn't a number, +, or -
# 	#we need to tokenize the number before the e/E
# 	else if (not cur_char.isdigit)