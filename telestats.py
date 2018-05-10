#!/usr/bin/python3

import sys, json, datetime, argparse
from tabulate import tabulate

parser = argparse.ArgumentParser(description='Analyze your friends telegram usage behavior')
parser.add_argument('file', help='path to the log file')
parser.add_argument('-D', '--debug', action='store_true', help='prints debug stuff')
parser.add_argument('-d', '--details', metavar='name', help='show usage details of a particular person')
parser.add_argument('-s', '--sort', type=int, choices=range(6), default=1, help='sort list by [0: name, 1: duration, 2: frequency, ...]')
args = parser.parse_args()

onlinesince = {}
onlinetime = {}			# onlinetime[name][dotw][hotd] (dotw = day of the week, hotd = hour of the day)
onlinefrequency = {}	# onlinefrequency[name][dotw][hotd]

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

with open(args.file) as f:
	for line in f:
		line = line.replace('\n','')
		if line[-1:] == '}' and line[:1] == '{':
			try:
				data = json.loads(line)
				if data['event'] == 'online-status':
					if args.debug: print(data['when'], ':', data['user']['print_name'], 'ist nun', 'online' if data['online'] else 'offline')

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
rows = sorted(rows, key=lambda x: x[args.sort])
print(tabulate(rows, headers=headers, tablefmt='simple'))

def getIndicator(percentage):
	indicatorPart = ['2;32m░','2;32m▒','2;32m▓','2;32m█','0;32m▒','0;32m▓','0;32m█','0;92m▒','0;92m▓','0;92m█']
	i = int(percentage*10)
	return '\033['+indicatorPart[i if i < 10 else 9]+'\033[0m'

if args.details:
	name = args.details
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
