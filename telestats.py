#!/usr/bin/python

import sys, json, datetime


onlinesince = {}
onlinetime = {}
onlinefrequency = {}

debug = False
if "--debug" in sys.argv: debug = True

def addOnlineTime(name,time,hour):
#	if name in onlinetime:
#		onlinetime[name] += time
#	else:
#		onlinetime[name] = time

	if not name in onlinetime: onlinetime[name] = {}
	if hour in onlinetime[name]:
		onlinetime[name][hour] += time
	else:
		onlinetime[name][hour] = time	

def addOnlineFreq(name,hour):
#	if name in onlinefrequency:
#		onlinefrequency[name] += 1
#	else:
#		onlinefrequency[name] = 1

	if not name in onlinefrequency: onlinefrequency[name] = {}
	if hour in onlinefrequency[name]:
		onlinefrequency[name][hour] += 1
	else:
		onlinefrequency[name][hour] = 1




def getTime(time):
	return datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

with open(sys.argv[1]) as f:
	for line in f:
		line = line.replace('\n','')
		if line[-1:] == '}' and line[:1] == '{':
			try:
				data = json.loads(line)
				if data['event'] == 'online-status':
					if debug: print data['when'], ':', data['user']['print_name'], 'ist nun', 'online' if data['online'] else 'offline'

					name = data['user']['print_name']
					online = data['online']
					when = getTime(data['when'])
					hour = datetime.datetime.strftime(when,'%H')

					if online:
						when -= datetime.timedelta(minutes=5) #for some reason the timestamp when someone is online is exactly 5 minutes in the future.

					if not 'start' in globals():
						start = when
					end = when

					if online:
						addOnlineFreq(name,hour)
						onlinesince[name] = when
					else:
						if name in onlinesince and onlinesince[name] is not None:
							newTime = when-onlinesince[name]
							addOnlineTime(name,when-onlinesince[name],hour)
							onlinesince[name] = None


			except:
				pass

if not 'start' in globals():
	print "Keine Online Daten erfasst,"
	exit()

print
print '\033[4mStart:\033[0m\t\t', start
print '\033[4mEnd:\033[0m\t\t', end
print '\033[4mDuration:\033[0m\t',end-start
print


print '\033[4mName\t\t\tDuration\tFrequency\tDuration average\033[0m'

for name in onlinetime:
	freq = sum(onlinefrequency[name].values())
	time = datetime.timedelta()
	for hour in onlinetime[name]:
		time += onlinetime[name][hour]
	tabs = ""
	for k in range(3-(len(name)+1)/8): tabs += '\t'
	print name, tabs, time, '\t', freq, '\t\t', time/freq


try:
	name = sys.argv[2]
	print '\nDetails of', name+':'
	print '\033[4mTime\t\tDuration\tFrequency:\033[0m'
	for hour in onlinetime[name]:
		print hour, 'o\'clock\t', onlinetime[name][hour], '\t', onlinefrequency[name][hour]
except:
	pass
