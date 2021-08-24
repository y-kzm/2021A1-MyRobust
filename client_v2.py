#!/usr/bin/python3
import threading
import socket
import os

FILE_SIZE = 102400
FRAG_SIZE = 1400
MTU = 1500
FILENO_SIZE = 2 # byte
PKTNO_SIZE = 2  # byte
DATA_PATH = "./data/"

# Src param.
SrcIP = "127.0.0.2"
SrcPort = 8080
SrcAddr = (SrcIP, SrcPort)

# Dst param.
DstIP = "127.0.0.1"
DstPort = 8080
DstAddr = (DstIP, DstPort)


def data_send(file_no, pkt_no, file_data, offset): 
    # Make header.
    hdr = file_no.to_bytes(FILENO_SIZE, "big") + pkt_no.to_bytes(PKTNO_SIZE, "big")
    # Make send data.
    send_data = hdr + file_data[offset:FRAG_SIZE+offset].encode("ascii")

def ack_recv():
    # Receive the file number as ack.
    ack, addr = soc.recvfrom(FILENO_SIZE+PKTNO_SIZE)
    ack_f = int.from_bytes(ack[:2], "big")
    ack_p = int.from_bytes(ack[2:], "big")
    print("Successful: " ,ack_f, ack_p)

    return ack_f, ack_p


# Socket.
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(SrcAddr)

files_list = os.listdir(DATA_PATH)
# ["data0", "data1", "data2", "data3", ...]
for  file_no, file_name in enumerate(files_list):
    fp = open(DATA_PATH+file_name, "r")
    file_data = fp.read()
    fp.close()
    pkt_no = 0
    offset = 0

    while True:
        thrd1 = threading.Thread(target = data_send, args = (file_no, pkt_no, file_data, offset))
        thrd2 = threading.Thread(target = ack_recv)
        thrd1.start()
        thrd2.start()
        if thrd2 == (file_no, pkt_no):
            offsrt += FRAG_SIZE
            pkt_no += 1


