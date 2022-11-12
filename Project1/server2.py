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
    writeFilePtr = open("out-proj.txt", "w")
    
    while True:
        data_from_client = csockid.recv(1024)
        if data_from_client == "":
            writeFilePtr.close()
            print('Done.')
            ss.close()
            exit()
        else:
            reversedString = data_from_client.rstrip()[::-1]
            writeFilePtr.write(reversedString + "\n")
    
if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()
    time.sleep(5)
    