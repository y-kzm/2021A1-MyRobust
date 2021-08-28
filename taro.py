#!/usr/bin/python3
import socket
import os
import time
from concurrent.futures import ThreadPoolExecutor

### Define. ###
FILE_SIZE = 102400
FRAG_SIZE = 1400
MTU = 1500
FILENO_SIZE = 2 # byte
PKTNO_SIZE = 2  # byte
DATA_PATH = "~/data/"

# Src param.
# SrcIP = "127.0.0.2"           # Loopback.
SrcIP = "169.254.155.219"       # Taro.
SrcPort = 8080
SrcAddr = (SrcIP, SrcPort)
# Dst param.
# DstIP = "127.0.0.1"           # Loopback.
DstIP = "169.254.299.153"       # Hanko.
DstPort = 8080
DstAddr = (DstIP, DstPort)

### Functions. ###
def send_data(file_no, pkt_no, offset):
    # Make header.
    hdr = file_no.to_bytes(FILENO_SIZE, "big") + pkt_no.to_bytes(PKTNO_SIZE, "big")
    # Make send data.
    send_data = hdr + file_data[offset:FRAG_SIZE+offset].encode("ascii")

    soc.sendto(send_data, DstAddr)

    print("---------------")
    print("Send: ", file_no, pkt_no) 

def recv_ack():
    # Receive the file number as ack.
    ack, addr = soc.recvfrom(FILENO_SIZE+PKTNO_SIZE)
    ack_file_no = int.from_bytes(ack[:2], "big")
    ack_pkt_no = int.from_bytes(ack[2:], "big")
    print("ACK File No: " , ack_file_no)
    print("ACK Pkt No: ", ack_pkt_no) 

    return ack_pkt_no

### miain. ###
# Socket.
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(SrcAddr)

files_list = os.listdir(DATA_PATH)
# ["data0", "data1", "data2", "data3", ...]

# File no loop.
for  file_no, file_name in enumerate(files_list):
    fp = open(DATA_PATH+file_name, "r")
    file_data = fp.read()
    fp.close()

    ### Packet fragmeent. ###
    offset = 0 
    pkt_no = 0
    # Pkt no loop.
    while True:
        with ThreadPoolExecutor(max_workers=2) as executor:
            send_data(file_no, pkt_no, offset)
            ack = executor.submit(recv_ack)
            if ack.result() == pkt_no:
                pkt_no += 1
                offset += FRAG_SIZE

        if ack.result() == FILE_SIZE//FRAG_SIZE+1:
            break

soc.close()


