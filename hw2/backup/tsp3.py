#Jason Cross & David Hoel
#TSP code for 3rd test instance

import sys
import getopt
import math
import numpy

cityMatrix = 0
lenDict = 0

#compute the distance between the 2 cities when using the dict from nearest neighbor
def NNdistance(city1, city2):
	return int(round(math.sqrt((float(city1[0])-float(city2[0]))**2+(float(city1[1])-float(city2[1]))**2)))

#compute the distance between the 2 cities in the cityMatrix when swapping.
def swapDistance(city1, city2):
	global cityMatrix

	return int(round(math.sqrt(((float(cityMatrix[city1][1])-float(cityMatrix[city2][1]))**2) + ((float(cityMatrix[city1][2])-float(cityMatrix[city2][2]))**2))))

def swap():
	global cityMatrix
	global lenDict

	improvements = 0

	while improvements < 5:
		for i in range(0, lenDict-2):
			j = i + 1
			originalD = 0
			swapD = 0
			tempCityId = 0
			tempX = 0
			tempY = 0

			originalD = swapDistance(i-1, i) + swapDistance(i, j) + swapDistance(j, j+1)
			swapD = swapDistance(i-1, j) + swapDistance(i, j) + swapDistance(i, j+1)

			if (swapD < originalD):
				improvements = 0
				#we do the swap
				tempCityId = cityMatrix[i][0]
				tempX = cityMatrix[i][1]
				tempY = cityMatrix[i][2]

				#replace i with j
				cityMatrix[i][0] = cityMatrix[j][0]
				cityMatrix[i][1] = cityMatrix[j][1]
				cityMatrix[i][2] = cityMatrix[j][2]

				#replace j with original i
				cityMatrix[j][0] = tempCityId
				cityMatrix[j][1] = tempX
				cityMatrix[j][2] = tempY

			else:
				continue

		improvements = improvements + 1

def tsp(dict):
	i = 0
	swapFinalD = 0
	global lenDict
	lenDict = len(dict)
	fileString = ""
	firstKey = dict.keys()[0]
	firstCity = currCity = dict[firstKey]
	global cityMatrix
	cityMatrix = numpy.zeros((lenDict, 3), dtype=numpy.int)
	cityMatrix[lenDict-1][0] = firstKey
	cityMatrix[lenDict-1][1] = firstCity[0]
	cityMatrix[lenDict-1][2] = firstCity[1]
	
	#Use the nearest neighbor algorithm to generate a tour
	dict.pop(firstKey)

	while(len(dict) > 0):
		minDist = sys.maxint
		minCity = currCity
		minKey = ""

		for key in dict.keys():
			currDist = NNdistance(currCity, dict[key])
			if (currDist < minDist):
				minDist = currDist
				minKey = key
		currCity = dict[minKey]
		cityMatrix[i][0] = minKey
		cityMatrix[i][1] = currCity[0]
		cityMatrix[i][2] = currCity[1]
		dict.pop(minKey)
		i = i+1

	#Nearest neighbor has given us a tour and a total tour distance
	#We can now use swapping to try and improve the tour
	swap()

	#We have finished swapping
	for x in range(0, lenDict-1):
		swapFinalD = swapFinalD + swapDistance(x, x+1)

	for x in range(0, lenDict):
		fileString = fileString + str(cityMatrix[x][0]) + '\n'

	return str(int(swapFinalD)) + '\n' + fileString

def reduceWhiteSpace(line):
	line = line.strip('\t\n\r').lstrip()
	while("  " in line):
		line = line.replace("  ", " ")
	return line

def usage():
	print "\nHow to use tsp.py:"
	print "\nFor Regular Use:\ttsp.py -s <name of file with cities and distances>"
	print "For help:\t\ttsp.py -h\n"
	print "Example to run the file 'test.txt':"
	print "tsp.py -s test.txt\n"

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
			input = open(a, 'r')
			dict = {}

			for line in input:
				if(line != "\n"):
					lineArray = reduceWhiteSpace(line).split(' ')
					dict[lineArray[0]] = [lineArray[1], lineArray[2]]

			input.close()
			output = open(a + ".tour", 'w')
			output.write(tsp(dict))
			output.close()

		else:
			assert False, "unhandled option"

if __name__ == "__main__":
	main()
