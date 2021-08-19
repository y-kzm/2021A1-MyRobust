#!/usr/bin/python3

import socket
import os

FILE_SIZE = 102400
FRAG_SIZE = 1400
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

# Socket.
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(SrcAddr)

files_list = os.listdir(DATA_PATH)
# ["data0", "data1", "data2", "data3", ...]
for  file_no, file_name in enumerate(files_list):
    fp = open(DATA_PATH+file_name, "r")
    file_data = fp.read()
    fp.close()

    ### Packet fragmeent. ###
    offset = 0 
    for pkt_no in range(FILE_SIZE//FRAG_SIZE+1):
        # Make header.
        hdr = file_no.to_bytes(FILENO_SIZE, "big") + pkt_no.to_bytes(PKTNO_SIZE, "big")
        # Make send data.
        send_data = hdr + file_data[offset:FRAG_SIZE+offset].encode("ascii")
        # Proceed with file offset.
        offset += FRAG_SIZE

        soc.sendto(send_data, DstAddr)
    
        print("Send: ", file_no, pkt_no)
        # print(send_data)


