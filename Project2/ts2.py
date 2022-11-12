import socket
import sys

def ts(tsListenPort):
	
	try:
		#Create Socket
		tsSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("[TS2]: TS2 Socket Created")
	except socket.error as err:
		#Error
		print('socket open error: {} \n'.format(err))
		exit()

	server_binding = ("", tsListenPort)
	tsSocket.bind(server_binding)
	tsSocket.listen(2)
	
	host = socket.gethostname()
	localhost_ip = (socket.gethostbyname(host))
	cs, addr = tsSocket.accept()
	
	while True:

		#Receive data from client, remove spaces at the beginning and end, and convert to upper case
		data = cs.recv(200).decode('utf-8').strip().upper()
		
		#Pointer for text file to read		
		readFilePtr = open('PROJ2-DNSTS2.txt', 'r')

		for line in readFilePtr:
			if data in line.upper():
				#Found domain name in TS2
				finalLine = line.strip() + ' IN'
				cs.send(finalLine.encode('utf-8'))
				break

	cs.close()
	tsSocket.close()
	exit()

if __name__ == "__main__":
    ts(int(sys.argv[1]))
    print("Done.")