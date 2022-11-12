import threading
import time
import random

import socket

def client():
    try:
        # Client socket created
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())
    
    # Connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Read the input file and send each line one 
    # by one to the server to reverse 
    while True:   
        readFilePtr = open("in-proj.txt", "r")
        for line in readFilePtr:
            cs.send(str(line).encode('utf-8'))
            time.sleep(2)

        # Close the client socket
        cs.close()
        exit()

if __name__ == "__main__":
    
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)