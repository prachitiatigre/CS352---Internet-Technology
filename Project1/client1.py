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

    # Receive input from the user
    sentence = raw_input("Enter a String ")

    # Send the input from user to the server
    cs.send(sentence.encode('utf-8'))

    # Get the reversed string
    data_from_server = cs.recv(200)
    print("Reversed String: {}".format(data_from_server.decode('utf-8')))

    # Close the client socket
    cs.close()
    exit()

if __name__ == "__main__":
    
    #t1 = threading.Thread(name='server', target=server)
    #t1.start()

    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)
