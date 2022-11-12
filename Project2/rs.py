import select
import socket
import sys

def rs(rsListenPort, ts1Hostname, ts1ListenPort, ts2Hostname, ts2ListenPort):
    
    try:
        #Create Sockets
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts2Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[RS]: RS Socket Created")

    except socket.error as err:
        #Error
        print('socket open error: {} \n'.format(err))
        exit()

    server_binding = ("", rsListenPort)
    ss.bind(server_binding)
    ss.listen(2)

    ts1Socket.connect((ts1Hostname, ts1ListenPort))
    ts2Socket.connect((ts2Hostname, ts2ListenPort))

    message_buffer = {}
    inputs = [ts1Socket, ts2Socket]
    outputs = []

    csockid, add = ss.accept()

    while True:
        
        #Receive data from client and get rid of spaces at the beginning and end
        data_from_client = csockid.recv(200).decode('utf-8').strip()
        
        #Send data received from client to both TS1 and TS2
        ts1Socket.send(data_from_client)
        ts2Socket.send(data_from_client)

        readable, writable, errors = select.select(inputs, outputs, [], 20)

        if readable:
            #Received response from either TS1 or TS2
            data_from_ts = readable[0].recv(200).decode('utf-8')
            csockid.send(data_from_ts)
            
        else:
            #Received no reponse from either TS1 or TS2
            if data_from_client == "":
                #No response because there is an empty line in the input file
                line = " "
                csockid.send(line.encode('utf-8'))
            
            else:
                #No response because domain name was not found
                line = data_from_client + " - TIMED OUT"
                csockid.send(line.encode('utf-8'))

    ts1Socket.close()
    ts2Socket.close()
    ss.close()
    exit()
                
if __name__ == "__main__":
    rs(int(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]), str(sys.argv[4]), int(sys.argv[5]))
    print("Done.")