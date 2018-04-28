#!/urs/bin/python
#rdsg - rohdaten sind geil!

import sys, json

i = 0
data = {}

with open(sys.argv[1]) as f:
	for line in f:
		line = line.replace('\n','')
		if line[-1:] == ']':
			try:
				data[i] = json.loads(line)
				i+=1
			except:
				pass

print len(data)
