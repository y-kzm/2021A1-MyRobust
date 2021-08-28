#!/usr/bin/python3
import socket
import os

### Define. ###
FILE_SIZE = 102400
MTU = 1500
FRAG_SIZE = 1400
FILENO_SIZE = 2 # byte
PKTNO_SIZE = 2  # byte
# DATA_PATH = "./data_rcv/"     # Loopback.
DATA_PATH = "~/data/"

# Src param.
# SrcIP = "127.0.0.1"           # Loopback.
SrcIP = "169.254.299.153"       # Hanko.
SrcPort = 8080
SrcAddr = (SrcIP, SrcPort)
# Dst param.
# DstIP = "127.0.0.1"
# DstIP = "169.254.155.219"     # Taro.
# DstPort = 8080
# DstAddr = (DstIP, DstPort)

### main. ###
# Socket.
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# soc = socket(AF_INET, SOCK_DGRAM)
soc.bind(SrcAddr)

# File number loop.
while True:
    try: 
        data_list = []
        pkt_no = 0
        # Packet number loop.
        while True:       
            recv_data, addr = soc.recvfrom(MTU)

            # The first 4 bytes are the header.
            hdr = recv_data[:4]   
            # [File No. (2)] [Packet No. (2)] [PayLoad...]
            file_no = int.from_bytes(hdr[:2], "big")
            pkt_no = int.from_bytes(hdr[2:], "big")
            data_list.append(recv_data[4:].decode("ascii"))

            # Return the header as ack.
            soc.sendto(hdr, addr)

            print("Recv: ", file_no, pkt_no)
            # print(data_list)

            # It's not "+1" because it's the end of the loop.
            if pkt_no == (FILE_SIZE//FRAG_SIZE):
                break

        file = "".join(data_list)
        # print("-----File Data.-----")
        # print(file)
        fp = open(os.path.join(DATA_PATH, "data"+str(file_no)), "w")
        fp.write(file)
        fp.close()     

    except KeyboardInterrupt: 
        print("\nEND.")
        soc.close()
        break
