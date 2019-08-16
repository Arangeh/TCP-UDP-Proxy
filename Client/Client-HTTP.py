from socket import *
import time

# initial port number
port = 10000

# initial host IP
host = '127.0.0.1'

# make UDP socket
sendertSocket = socket(AF_INET, SOCK_DGRAM)

sendertSocket.connect((host, port))

# shows message sequence
sequence_number = 0


# change sequence number / can have values 0 , 1
def seq_number_changer(sequence_number):
    return 0 if sequence_number == 1 else 1


while True:
    line1, line2 = input("Enter your command:\n").split(",")
    message = str(sequence_number) + line1 + "\n" + line2 + "\n" + "\n" + "/@#@$/"

    # send message by UDP socket
    sendertSocket.send(bytes(message, 'utf-8'))

    print("Message is sent")
    start_time = time.time()

    while True:

        if time.time() - start_time < 1:
            try:
                rcv_message = sendertSocket.recv(1024)

            except sendertSocket.timeout:
                print("Continue waiting")
                continue
            else:
                if rcv_message == "BAD ACK":
                    print("Sender received a corrupted ACK; keep waiting")
                    continue
                #ack = int.from_bytes(rcv_message, byteorder='big')
                ack =str(rcv_message,encoding='utf-8')
                ack = int(ack)
                print(ack)
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
                    sendertSocket.send(bytes(message, 'utf-8'))

    while True:


        message, sender_Address = sendertSocket.recvfrom(1024)
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


        packet = ""
        while True:
            received_sequence_number, data = parse_message(message)
            print(data)
            if data == "/@#@$/":
                f = open("index.html", 'w')
                f.write(packet)
                f.close()
                break
            else:
                if message != old_received_message:
                    if received_sequence_number == expected_sequence_number:
                        packet = packet + data
                        print("Received just correctly received a message: ")
                        sendertSocket.send(bytes(str(expected_sequence_number), 'utf-8'))

                else:
                    print("Received just correctly received a duplicated message: ")
                    sendertSocket.send(bytes(str(seq_number_changer(expected_sequence_number)), 'utf-8'))

                old_received_message = message
                expected_sequence_number = seq_number_changer(expected_sequence_number)

# GET /khers HTTP/1.1,Host: aut.ac.ir
# GET /uploads/066ebtc.jpg HTTP/1.1,Host: up2www.com
# GET /FGK0T HTTP/1.1,Host: yon.ir