import threading
import time
import random

import socket

def server():
    try:
        # Server socket created
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    localhost_ip = (socket.gethostbyname(host))
    csockid, addr = ss.accept()
    
    # Get the string from client
    data_from_client = csockid.recv(200)
    
    # Reverse the string received from client
    reversedString = data_from_client[::-1]

    # Send it back to client
    csockid.send(reversedString.encode('utf-8'))

    # Close the server socket
    ss.close()
    exit()

if __name__ == "__main__":
    
    t1 = threading.Thread(name='server', target=server)
    t1.start()

    #time.sleep(random.random() * 5)
    #t2 = threading.Thread(name='client', target=client)
    #t2.start()

    time.sleep(5)
