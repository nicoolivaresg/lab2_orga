def EXEC():
	init = PC
	for x in xrange(init, (len(lines)) - 1):
		if (x == -1):
			print "X is"
			print x
			eval(PIPELINE[0])
		elif (x == 0):
			print "X is"
			print x
			eval(PIPELINE[1])
			eval(PIPELINE[0])
		elif (x == 1):
			print "X is"
			print x
			eval(PIPELINE[2])
			eval(PIPELINE[1])
			eval(PIPELINE[0])
		elif (x == 2):
			print "X is"
			print x
			eval(PIPELINE[3])
			eval(PIPELINE[2])
			eval(PIPELINE[1])
			eval(PIPELINE[0])
		elif (x == (len(lines)-2)):
			print "X is"
			print x
			for i in xrange(4,-1,-1):
				eval(PIPELINE[i])
			for i in xrange(4,0,-1):
				eval(PIPELINE[i])
			for i in xrange(4,1,-1):
				eval(PIPELINE[i])
			for i in xrange(4,2,-1):
				eval(PIPELINE[i])
			eval(PIPELINE[4])
		else:
			print "X is"
			print x
			for i in xrange(4,-1, -1):
				eval(PIPELINE[i])
