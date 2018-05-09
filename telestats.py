#!/usr/bin/python3

import sys, json, datetime
from tabulate import tabulate

if len(sys.argv) < 2:
	print('Usage:\tpython '+sys.argv[0]+' FILE [NAME | DEBUG]')
	print('E.g.:\tpython '+sys.argv[0]+' path/to/your/capture.file Marcel')
	print('Or:\tpython '+sys.argv[0]+' path/to/your/capture.file DEBUG')
	exit()

onlinesince = {}
onlinetime = {}			# onlinetime[name][dotw][hotd] (dotw = day of the week, hotd = hour of the day)
onlinefrequency = {}	# onlinefrequency[name][dotw][hotd]

debug = False
if len(sys.argv) > 2 and sys.argv[2] == 'DEBUG': debug = True

def addOnlineTime(name,time,dotw,hotd):
	if not name in onlinetime: onlinetime[name] = {}
	if not dotw in onlinetime[name]: onlinetime[name][dotw] = {}
	if hotd in onlinetime[name][dotw]:
		onlinetime[name][dotw][hotd] += time
	else:
		onlinetime[name][dotw][hotd] = time	

def addOnlineFreq(name,dotw,hotd):
	if not name in onlinefrequency: onlinefrequency[name] = {}
	if not dotw in onlinefrequency[name]: onlinefrequency[name][dotw] = {}
	if hotd in onlinefrequency[name][dotw]:
		onlinefrequency[name][dotw][hotd] += 1
	else:
		onlinefrequency[name][dotw][hotd] = 1




def getTime(time):
	return datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

with open(sys.argv[1]) as f:
	for line in f:
		line = line.replace('\n','')
		if line[-1:] == '}' and line[:1] == '{':
			try:
				data = json.loads(line)
				if data['event'] == 'online-status':
					if debug: print(data['when'], ':', data['user']['print_name'], 'ist nun', 'online' if data['online'] else 'offline')

					name = data['user']['print_name']
					online = data['online']
					when = getTime(data['when'])
					dotw = datetime.datetime.strftime(when,'%w')
					hotd = datetime.datetime.strftime(when,'%H')

					if online:
						when -= datetime.timedelta(minutes=5) #for some reason the timestamp when someone is online is exactly 5 minutes in the future.

					if not 'start' in globals():
						start = when
					end = when

					if online:
						addOnlineFreq(name,dotw,hotd)
						onlinesince[name] = when
					else:
						if name in onlinesince and onlinesince[name] is not None:
							newTime = when-onlinesince[name]
							addOnlineTime(name,when-onlinesince[name],dotw,hotd)
							onlinesince[name] = None


			except:
				pass

if not 'start' in globals():
	print("Keine Online Daten erfasst.")
	exit()

print('\n\033[4mStart:\033[0m\t\t', start)
print('\033[4mEnd:\033[0m\t\t', end)
print('\033[4mDuration:\033[0m\t', end-start, '\n')


botdays = (end-start).total_seconds()/60/60/24
headers = ['Name', 'Duration', 'Frequency', 'Duration average', 'Duration / Day', 'Frequency / Day']
rows = []
for name in onlinetime:
	freq = sum([sum(x.values()) for x in onlinefrequency[name].values()])
	time = datetime.timedelta()
	for dotw in onlinetime[name]:
		for hotd in onlinetime[name][dotw]:
			time += onlinetime[name][dotw][hotd]
	rows.append([name,time,freq,time/freq,time/botdays,freq/botdays])
rows = sorted(rows, key=lambda x: x[1])
print(tabulate(rows, headers=headers, tablefmt='simple'))


if len(sys.argv) < 3 or sys.argv[2] == 'DEBUG': exit()

def getIndicator(percentage):
	if percentage < 1/10: return '\033[2;32m░\033[0m'
	if percentage < 2/10: return '\033[2;32m▒\033[0m'
	if percentage < 3/10: return '\033[2;32m▓\033[0m'
	if percentage < 4/10: return '\033[2;32m█\033[0m'
	if percentage < 5/10: return '\033[0;32m▒\033[0m'
	if percentage < 6/10: return '\033[0;32m▓\033[0m'
	if percentage < 7/10: return '\033[0;32m█\033[0m'
	if percentage < 8/10: return '\033[0;92m▒\033[0m'
	if percentage < 9/10: return '\033[0;92m▓\033[0m'
	return '\033[0;92m█\033[0m'

try:
	name = sys.argv[2]
	print('\nDetails of', name+':')

	freq = [[0]*24 for i in range(7)]
	for dotw in onlinefrequency[name]:
		for hotd in onlinefrequency[name][dotw]:
			freq[int(dotw)][int(hotd)] = onlinefrequency[name][dotw][hotd]

	time = [[datetime.timedelta()]*24 for i in range(7)]
	for dotw in onlinetime[name]:
		for hotd in onlinetime[name][dotw]:
			time[int(dotw)][int(hotd)] = onlinetime[name][dotw][hotd]

	totalTotalFreq = sum([sum(x) for x in freq])
	totalTotalTime = datetime.timedelta()
	for i in time:
		for j in i:
			totalTotalTime += j

	rows = []
	for hotd in range(24):
		row = [hotd]
		for dotw in range(7):
			row.append(str(time[dotw][hotd]) + ' ' + getIndicator(time[dotw][hotd]/(totalTotalTime/15)) + ' ' + getIndicator(freq[dotw][hotd]/(totalTotalFreq/15)) + ' ' + str(freq[dotw][hotd]))
		totalFreq = sum([x[hotd] for x in freq])
		totalTime = datetime.timedelta()
		for i in [x[hotd] for x in time]:
			totalTime += i
		row.append(str(totalTime) + '     ' + str(totalFreq))
		rows.append(row)
	row = ['Total']
	for dotw in range(7):
		totalFreq = sum(freq[dotw])
		totalTime = datetime.timedelta()
		for i in time[dotw]:
			totalTime += i
		row.append(str(totalTime) + '     ' + str(totalFreq))
	
	row.append(str(totalTotalTime) + '     ' + str(totalTotalFreq)) 
	rows.append(row)

	headers = ['Hour of the day','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Total']
	print(tabulate(rows, headers=headers, tablefmt='pipe'))



except:
	pass
