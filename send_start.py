from socket import *

###IP_ports = [("18.62.21.200", 11000), ("18.62.28.133", 11000), 
###            ("18.62.23.61", 11000), ("18.62.23.62", 11000),
###            ("18.62.23.63", 11000)]

IP_ports = [("localhost", 11000), ("localhost", 12000), 
            ("localhost", 13000), ("localhost", 14000),
            ("localhost", 15000), ("localhost", 16000)]
def start():
    for pair in IP_ports:
        addr = (pair[0], pair[1])    
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        data = b"Start"
        UDPSock.sendto(data, addr)
        UDPSock.close()
        print("Sent to <%s, %s>" % (pair[0], pair[1]))

start()
