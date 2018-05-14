#!/usr/bin/python3

import sys, json, datetime, argparse
from tabulate import tabulate

parser = argparse.ArgumentParser(description='Analyze your friends telegram usage behavior')
parser.add_argument('file', help='path to the log file') # type=argparse.FileType('r')
parser.add_argument('--debug', action='store_true', help='prints debug stuff')
parser.add_argument('--fullname', action='store_true', help='prints the full name of all users (instead of the 1st 50 chars)')
parser.add_argument('-d', '--details', metavar='name', help='show hourly usage details of a particular person. (-d all for hourly details of all tracked users)')
parser.add_argument('--username', metavar='name', help='prints the username of a specific person.')
parser.add_argument('-s', '--sort', type=int, choices=range(6), default=1, help='sort list by [0: name, 1: duration, 2: frequency, ...]')
parser.add_argument('-i', '--info', action='store_true', help='Prints only the info')
parser.add_argument('--ignore', metavar='name', nargs='+', help='Ignores specific users.')
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


num_lines = sum(1 for line in open(args.file))
count_lines = 0

with open(args.file) as f:
	for line in f:
		if (count_lines % (num_lines/1000.) > (count_lines+1) % (num_lines/1000.)):
			if 'progress' in globals(): sys.stdout.write('\b' * (len(progress) + 1))
			else: sys.stdout.write('Loading: ')
			progress = str(round(count_lines / float(num_lines) * 100, 2))
			sys.stdout.write(progress + '%')
			sys.stdout.flush()
		count_lines += 1
		line = line.replace('\n','')
		if line[-1:] == '}' and line[:1] == '{':
			try:
				data = json.loads(line)
				if data['event'] == 'online-status':
					if args.debug: print(data['when'], ':', data['user']['print_name'], 'ist nun', 'online' if data['online'] else 'offline')

					name = data['user']['print_name']
					if args.username != None: #
						if name == args.username:
							print('\n\nName:\t\t' + args.username)
							print('Username:\t' + data['user']['username'])
							sys.exit()
					if args.ignore != None and name in args.ignore: continue
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


			except Exception as e:
				pass

if not 'start' in globals():
	print("Keine Online Daten erfasst.")
	exit()

if args.username != None:
	print('\n\nNo username for ' + args.username + ' found.')
	exit()

for name in [x for x in onlinesince if onlinesince[x] != None]:
	dotw = datetime.datetime.strftime(end, '%w')
	hotd = datetime.datetime.strftime(end, '%H')
	addOnlineTime(name, end - onlinesince[name], dotw, hotd) 

print('\n\n\033[4mStart:\033[0m\t\t', start)
print('\033[4mEnd:\033[0m\t\t', end)
print('\033[4mDuration:\033[0m\t', end-start)


botdays = (end-start).total_seconds()/60/60/24
headers = ['Name', 'Duration', 'Frequency', 'Duration average', 'Duration / Day', 'Frequency / Day', 'Online']
rows = []
for name in onlinetime:
	freq = sum([sum(x.values()) for x in onlinefrequency[name].values()])
	time = datetime.timedelta()
	for dotw in onlinetime[name]:
		for hotd in onlinetime[name][dotw]:
			time += onlinetime[name][dotw][hotd]
	rows.append([name if args.fullname else name[:50],time,freq,time/freq,time/botdays,freq/botdays,name in onlinesince and onlinesince[name] is not None])
print('\033[4mUsers:\033[0m\t\t', len(rows))
print('\033[4mOnline:\033[0m\t\t', len([x for x in onlinesince if onlinesince[x] is not None]), '\n')
rows = sorted(rows, key=lambda x: x[args.sort])
rows.append([])
rows.append(headers)
if not args.info: print(tabulate(rows, headers=headers, tablefmt='simple'))

def getIndicator(percentage):
	indicatorPart = ['2;32m░','2;32m▒','2;32m▓','2;32m█','0;32m▒','0;32m▓','0;32m█','0;92m▒','0;92m▓','0;92m█']
	i = int(percentage*10)
	return '\033['+indicatorPart[i if i < 10 else 9]+'\033[0m'

if args.details:
	name = args.details
	print('\nDetails of', name+':')

	freq = [[0]*24 for i in range(7)]
	time = [[datetime.timedelta()]*24 for i in range(7)]
	if name == 'all':
		for name in onlinefrequency:
			for dotw in onlinefrequency[name]:
				for hotd in onlinefrequency[name][dotw]:
					freq[int(dotw)][int(hotd)] += onlinefrequency[name][dotw][hotd] #/ len(rows)
		for name in onlinetime:
			for dotw in onlinetime[name]:
				for hotd in onlinetime[name][dotw]:
					time[int(dotw)][int(hotd)] += onlinetime[name][dotw][hotd] #/ len(rows)
	else:
		if name in onlinefrequency:
			for dotw in onlinefrequency[name]:
				for hotd in onlinefrequency[name][dotw]:
					freq[int(dotw)][int(hotd)] += onlinefrequency[name][dotw][hotd]
		if name in onlinetime:
			for dotw in onlinetime[name]:
				for hotd in onlinetime[name][dotw]:
					time[int(dotw)][int(hotd)] += onlinetime[name][dotw][hotd]


	if (sum(sum(x) for x in freq) == 0 and sum([sum(y.total_seconds() for y in x) for x in time]) == 0.):
		print('Kein Eintrag von', name, 'vorhanden.')
		exit()


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

	headers = ['Hour of the day','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Total']
	print(tabulate(rows, headers=headers, tablefmt='pipe'))
