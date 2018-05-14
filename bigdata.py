import socket, time, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=3731, help='the port on which the telegram-cli is listening on')
parser.add_argument('groups', metavar='group', nargs='+', help='')#, required=True)
parser.add_argument('--sleep', type=int, default=1)
args = parser.parse_args()



#als arg die channel zum sniffen angeben

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(('localhost',3731))

i = 0

while True:
	for id in args.groups:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('localhost',args.port))
#		s.send('channel_get_members Nucleus_Vision_(Official) 100000\n')
		s.send('channel_get_members $' + id + ' 100000\n')

#		s.recv(2**30)

		s.close()
		time.sleep(args.sleep)
	print i
	i += 1
