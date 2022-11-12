import socket
import sys

def client(rsHostname, rsListenPort):
	
	try:
		#Create Socket
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("[C]: Client Socket Created")

	except socket.error as err:
		#Error
		print('socket open error: {} \n'.format(err))
		exit()

	server_binding = (rsHostname, rsListenPort)
	cs.connect(server_binding)
	
	#Pointer for input file
	readFilePtr = open('PROJ2-HNS.txt', 'r')

	#Pointer for the output file
	writeFilePtr = open('RESOLVED.txt', 'w+')
    
	for line in readFilePtr:
		cs.send(str(line).decode('utf-8'))
		finalAns = cs.recv(200).decode('utf-8')
		print(finalAns)
		writeFilePtr.write(finalAns + '\n')

	writeFilePtr.close()
	readFilePtr.close()
	cs.close()
	
if __name__ == "__main__":
    client(str(sys.argv[1]), int(sys.argv[2]))
    print("Done.")