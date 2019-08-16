from socket import *

while True:
    command = input("Enter your command:\n")

    # initial port number
    port = 20000

    # initial host IP
    host = '127.0.0.1'

    # make TCP socket
    senderSocket = socket(AF_INET, SOCK_STREAM)

    senderSocket.connect((host, port))

    # send message
    senderSocket.send(bytes(command, 'utf-8'))

    myIp = senderSocket.recv(1024).decode('utf-8')
    print(myIp)
