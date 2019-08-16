import select
import time
from socket import *

cache = {}
# initial port number
port = 10000

# initial host IP
host = '0.0.0.0'

# make UDP socket
receiverSocket = socket(AF_INET, SOCK_DGRAM)

# binds to the port
receiverSocket.bind((host, port))

# established a connection
message, sender_Address = receiverSocket.recvfrom(1024)
message = str(message, encoding='utf-8')
expected_sequence_number = 0
old_received_message = ""


# seperate sequence number from data in received message
def parse_message(message):
    if message == "":
        print("Terminating the program due to time limitation.Thanks for watching!")
        exit()

    received_sequence_number = int(message[0])
    data = message[1:]
    return received_sequence_number, data


# change sequence number / can have values 0 , 1
def seq_number_changer(sequence_number):
    return 0 if sequence_number == 1 else 1

def get_location(message):
    splited_message = message.split()
    for key, value in enumerate(splited_message):
        if value == "Location:":
            location = splited_message[key + 1]
            location = location.split("http://")[1]
            print("locationooo: " + location )
            break
    temp = location.split("/")
    host = temp[0]
    redirect = ""
    for item in temp[1:]:
        redirect = redirect + "/" + item
    return host,redirect


while True:
    received_sequence_number, data = parse_message(message)
    # print(received_sequence_number)
    # print(data)
    if message != old_received_message:
        if expected_sequence_number == received_sequence_number:
            print("Received just correctly received a message: " + str(message))
            receiverSocket.sendto(bytes(str(expected_sequence_number), 'utf-8'), sender_Address)
            # print(message[len(message) - 6:len(message)])
            if (message[len(message) - 6:len(message)] == "/@#@$/"):
                # print("here")
                data = data[:len(data) - 6]
                break
    else:
        print("Received just correctly received a duplicated message: " + str(message))
        receiverSocket.sendto(bytes(str(seq_number_changer(expected_sequence_number)), 'utf-8'), sender_Address)
        # break

    old_received_message = message
    expected_sequence_number = seq_number_changer(expected_sequence_number)

parsed = data.split()
host = ""
for key, value in enumerate(parsed):
    if value == "Host:":
        host = parsed[key + 1]

print("myHost:" + host)
while True:
    tcp_port = 80
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect((host, tcp_port))
    print(";", data, ";")
    tcp_socket.send(bytes(data, 'utf-8'))
    while True:
        inout = [tcp_socket]
        object_file = ""
        r = [tcp_socket]
        buf = b''
        while r:
            r, w, e = select.select(inout, [], [], 5)
            if not r:
                break
            temp = tcp_socket.recv(1024)
            if not temp:
                break
            buf = buf + temp
        object_file = str(buf,encoding='utf-8')
        f = open(host + ".html", 'w')
        f.write(object_file)
        f.flush()
        f.close()

        cache.update({host: host + ".html"})

        status = object_file.split(" ")[1]
        print(status)

        if status == "200":
            print("200 OK")
            break

        elif status == "404":
            print("404 PAGE NOT FOUND")
            break


        elif status == "301":
            print("301 MOVED_PERMANENTLY")
            host,redirect = get_location(object_file)
            message = "GET " +redirect + "/ " + "HTTP/1.1" + "\n" + "Host: " + host + "\n" + "\n"
            tcp_socket.send(bytes(message,'utf-8'))
            continue


        elif status == "302":
            print("302 MOVED_PERMANENTLY")
            host, redirect = get_location(object_file)
            message = "GET " + redirect + "/ " + "HTTP/1.1" + "\n" + "Host: " + host + "\n" + "\n"
            print(host)
            print(redirect)
            print(message)
            tcp_socket.send(bytes(message, 'utf-8'))
            continue
        packet = []
        f = open(host + ".html", 'rb')
        for chunk in iter(lambda: f.read(800), b""):
            packet.append(chunk)
        if len(packet) % 2 == 0:
            packet.append(b'/0@#@$/')
        else:
            packet.append(b'/1@#@$/')
        print(packet)
        sequence_number = 0
        for item in packet:
            receiverSocket.sendto(bytes(str(sequence_number) + str(item), 'utf-8'), sender_Address)
            start_time = time.time()

            while True:

                if time.time() - start_time < 1:
                    try:
                        rcv_message = receiverSocket.recv(1024)
                    except receiverSocket.timeout:
                        print("Continue waiting")
                        continue
                    else:
                        ack = str(rcv_message, encoding='utf-8')
                        ack = int(ack)
                        if ack == sequence_number:
                            print("Sender received a valid ACK for " + str(sequence_number))
                            sequence_number = seq_number_changer(sequence_number)
                            break
                        elif ack == seq_number_changer(sequence_number):
                            print("Sender received an ACK with wrong sequence number;keep waiting ...")
                            continue
                        else:
                            print("Timeout.Sending the message again.")
                            start_time = time.time()
                            receiverSocket.sendto(bytes(str(sequence_number) + str(item), 'utf-8'), sender_Address)
    break

