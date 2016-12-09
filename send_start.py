from socket import *

IP_ports = [("18.111.50.194", 11000), ("18.111.50.194", 13000), 
            ("18.111.50.194", 15000), ("18.111.43.90", 11000),
            ("18.111.51.183", 11000), ("18.189.16.43", 11000)]
def start():
    for pair in IP_ports:
        addr = (pair[0], pair[1])    
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        data = b"Start"
        UDPSock.sendto(data, addr)
        UDPSock.close()
        print("Sent to <%s, %s>" % (pair[0], pair[1]))

start()
