
stutest:
	python parser.py -s stutest.in -s stutest1.in -s stutest2.in -s stutest3.in > stutest.out

bad:
	python parser.py -s badtests/stutestBad.in
	python parser.py -s badtests/stutestBad2.in
	python parser.py -s badtests/stutestBad3.in
	python parser.py -s badtests/stutestBad4.in
	python parser.py -s badtests/stutestBad5.in
	python parser.py -s badtests/stutestBad6.in
	python parser.py -s badtests/stutestBad7.in
	python parser.py -s badtests/stutestBad8.in
	python parser.py -s badtests/stutestBad9.in
	python parser.py -s badtests/stutestBad10.in

proftest:
	python parser.py -s proftest.in > proftest.out

clean:
	rm -rf stutest.out

all: stutest
