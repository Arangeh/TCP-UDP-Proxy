from socket import *
import dns.resolver

cache = {}
# initial port number
port = 20000

# initial host IP
host = "0.0.0.0"

# make TCP socket
receiverSocket = socket(AF_INET, SOCK_STREAM)

receiverSocket.bind((host, port))

receiverSocket.listen(1)

print("The server is ready to receive")

while True:
    connectionSocket, sender_Address = receiverSocket.accept()
    message = connectionSocket.recv(1024).decode('utf-8')
    print(message)

    parsed = message.split()
    type = parsed[2]
    server = parsed[5]
    target = parsed[8]
    for key, value in cache.items():
        if key == target:
            connectionSocket.send(bytes(str(value), 'utf-8'))
            continue
    myresolver = dns.resolver.Resolver()
    myresolver.nameservers = [server]
    test = []
    try:
        dns_response = (myresolver.query(target, type))
        aut = bin(dns_response.response.flags)[7]
        print("Authority: " + aut)
        test = dns_response
        cache.update({target: test[0]})
        for item in dns_response:
            print(item)

    except:
        print("Query failed!")
        connectionSocket.send(bytes("Query failed!"), 'utf-8')
    if len(test) != 0:
        connectionSocket.send(bytes(str(test[0]), 'utf-8'))
