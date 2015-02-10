import sys
import getopt
import math

#keywords = dict(true='bool', false='bool', int='type', if='statement')
#keywords = dict()

keywords = {'true':bool}

keywords.update({'if':'statement'})
#keywords.update(**{'if':'statement'})

#keywords.update(true='bool')
#keywords.update(int='type')


print keywords


# extra code:
# input = open(a, 'r')

# for line in input:
#     if(line != "\n"):
#         lineArray = reduceWhiteSpace(line).split(' ')
#         dict[lineArray[0]] = [lineArray[1], lineArray[2]]

# input.close()

# output = open(a + ".out", 'w')
# output.write(tsp(dict))
# output.close()
