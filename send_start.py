from socket import *


def start(listOfIPs):
  for host in listOfIPs:
    #host = "127.0.0.1" # set to IP address of target computer
    ports = [13000, 15000]
    for port in ports:
        addr = (host, port)
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        data = b"Start"
        UDPSock.sendto(data, addr)
        UDPSock.close()
        print("Sent to <%s>" % (host))

start(["18.111.49.49", "18.111.109.12"])
