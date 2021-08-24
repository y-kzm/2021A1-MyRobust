import threading

def data_send(file_no, pkt_no, file_data, offset): 
    # Make header.
    hdr = file_no.to_bytes(FILENO_SIZE, "big") + pkt_no.to_bytes(PKTNO_SIZE, "big")
    # Make send data.
    send_data = hdr + file_data[offset:FRAG_SIZE+offset].encode("ascii")

def ack_recv():
    # Receive the file number as ack.
    ack, addr = soc.recvfrom(HEADER_SIZE)
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

    while True:
        thrd1 = threading.Thread(target = data_send, argd = (file_no, pkt_no, file_data, offset))
        thrd2 = threading.Thread(target = ack_recv)
        thr1.start()
        thrd2.start()
        if ack_recv() == file_no, pkt_no:
            offsrt += FRAG_SIZE
            pkt_no += 1




