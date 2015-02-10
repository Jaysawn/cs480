compiler:

clean:
	rm -f stutest.out proftest.out
	ls

stutest.out: compiler
	cat stutest.in
	gforth stutest.in > stutest.out 
	cat stutest.out

proftest.out: compiler
	cat proftest.in
	gforth proftest.in > proftest.out
	cat proftest.out
